# AllStars-Assesment

for the main app.py

It uses Selenium WebDriver and other Python libraries to download web pages from the Class Central website.

The script starts by importing necessary libraries such as Selenium, requests, and hashlib. It defines some global variables such as the base URL of the website, the directory where the downloaded files will be saved, the maximum depth of the recursion when downloading links, and a set to keep track of visited links.

Then the download_page function is defined, which takes a URL and an optional depth parameter. The function first checks whether the URL has been visited before, and if it has, it returns immediately. Otherwise, it visits the URL using a Firefox webdriver, finds all the links on the page, and extracts the HTML source code of the page.

The function then scrolls down the page to load all the images and extracts the title element of the page. It then creates a directory in the base_dir to store the downloaded files and downloads all the images, stylesheets, and scripts on the page. It saves the downloaded HTML source code in a file named "index.html" in the directory.

Finally, the function recursively calls itself on all the links on the page if the depth is less than "max_Depth".

The script then creates a Firefox webdriver, visits the "base_url", and calls the download_page function with the "base_url". After the function is finished, the webdriver is closed.

For the trasnlator script 

It translates HTML files in a directory and its subdirectories from English to Hindi using the Microsoft Translator API.

The script creates a Translator object with an API key and defines a function "translate_text" that takes a string of text as input and returns the translated text as output using the translate method of the Translator object.

The "translate_html_file()" function opens an HTML file, parses it using BeautifulSoup, and replaces all text nodes (except those inside script, style, head, and title tags) with their translations using the "translate_text()" function. The translated HTML is then written back to the file.

The "translate_html_files_in_directory()" function recursively walks through a directory and its subdirectories, finds all HTML files, and calls "translate_html_file()" on each file to translate its contents.
