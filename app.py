from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from translate import Translator
from selenium.webdriver.chrome.options import Options
from requests.exceptions import RequestException, JSONDecodeError
from json.decoder import JSONDecodeError
import hashlib,time,os,requests,re
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import os, requests

base_url = "https://www.classcentral.com/"
base_dir = "Files/"

visited_links = set()
max_Depth = 1
1
def download_page(url, depth=0):
    if url in visited_links:
        return
    visited_links.add(url)

    driver.get(url)
    nav_bar = driver.find_element(By.CSS_SELECTOR,"nav")
    nav_links = nav_bar.find_elements(By.TAG_NAME,"a")
    links_to_download = []

  
    height = driver.execute_script("return document.body.scrollHeight")

    html = driver.find_element(By.TAG_NAME,"html")
    while True:
        driver.execute_script("window.scrollBy(0, 350)")
        time.sleep(0.02)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == height:
            break
        height = newHeight
    title_element = driver.find_element(By.TAG_NAME, "title")
    try:

        for i in range(7):
            body = driver.find_element(By.TAG_NAME,"body")
            body.send_keys(Keys.COMMAND, Keys.SUBTRACT)
        page_dir = base_dir + url.replace(base_url, "").split("/")[0]
        if not os.path.exists(page_dir):
            os.makedirs(page_dir, exist_ok=True)
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        if len(img_elements) ==0:
            print("No images found on page: ", url)
        else:
            for img in driver.find_elements(By.TAG_NAME, "img"):
                img_url = img.get_attribute("src")
                driver.implicitly_wait(8)
                try:
                    if img_url and "http" in img_url:
                        img_path = page_dir + "/" + img_url.split("/")[-1]
                        height = driver.execute_script("return document.body.scrollHeight")
                        while True:
                            driver.execute_script("window.scrollBy(0, 350)")
                            time.sleep(0.01)
                            newHeight = driver.execute_script("return document.body.scrollHeight")
                            if newHeight == height:
                                break
                            height = newHeight
                        img_hash = hashlib.md5(img_path.encode()).hexdigest()
                        if not os.path.exists(img_path):
                            with open(img_hash, "wb") as f:
                                f.write(requests.get(img_url).content)
                                time.sleep(0.03)
                        try:
                            img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
                            driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", img, "file://" + img_path)
                        except StaleElementReferenceException:
                            img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
                            driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", img, "file://" + img_path)

                except JSONDecodeError:
                    pass
    except RequestException:
        pass
    except JSONDecodeError:
        pass


    for css in driver.find_elements(By.XPATH, "//link[@rel='stylesheet']"):
        css_url = css.get_attribute("href")
        try:
            if css_url and "http" in css_url:
                
                css_path = page_dir + "/" + css_url.split("/")[-1]
                css_hash = hashlib.md5(css_path.encode()).hexdigest()
                if not os.path.exists(css_hash):
                    with open(css_path, "w") as f:
                        f.write(requests.get(css_url).text)

                driver.execute_script("arguments[0].setAttribute('href', arguments[1]);", css, "file://" + css_path)
        except JSONDecodeError:
            pass


    for js in driver.find_elements(By.TAG_NAME, "script"):
        js_url = js.get_attribute("src")
        try:
            if js_url and "http" in js_url:

                file_contents = requests.get(js_url).text
                file_hash = hashlib.md5(file_contents.encode()).hexdigest()
                js_path = page_dir + "/" + file_hash + ".js"
                if os.path.exists(js_path):
                    with open(js_path, "w") as f:
                        f.write(file_contents)
    
                driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", js, "file://" + js_path)
        except JSONDecodeError:
            pass

    
    with open(page_dir + "/index.html", "w") as f:
        f.write(driver.page_source)
    driver.implicitly_wait(1)
    if depth < max_Depth:
        for link in driver.find_elements(By.TAG_NAME, "a"):
            link_url = link.get_attribute("href")
            if link_url and "http" in link_url and base_url in link_url:
                if link_url.endswith('/'):
                    download_page(link_url, depth+1)
            else:
                download_page(link_url + '/',depth+1)
driver = webdriver.Firefox()

driver.get(base_url)

download_page(base_url)

driver.quit()




