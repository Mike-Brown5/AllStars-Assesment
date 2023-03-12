import os
from bs4 import BeautifulSoup
from mstranslator import Translator

# Set the source and target languages
src_lang = 'en'
tgt_lang = 'hi'

# Create a translator object
translator = Translator('dcc464394a7b43038800f5b0f5311574')

# Define a function to translate text
def translate_text(text):
    translation = translator.translate(text, lang_from=src_lang, lang_to=tgt_lang)
    return translation

def translate_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Parse the HTML file using BeautifulSoup
        soup = BeautifulSoup(f, 'html.parser')
        text_nodes = soup.findAll(text=True)
        for text_node in text_nodes:
            if text_node.parent.name not in ['script', 'style', 'head', 'title']:
                text_node.replace_with(translate_text(text_node))

        # Write the translated HTML file to disk
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

# Define a function to recursively translate all HTML files in a directory and its sub-directories
def translate_html_files_in_directory(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f'Translating {file_path}...')
                translate_html_file(file_path)

# Call the function to translate all HTML files in the current directory and its sub-directories
translate_html_files_in_directory('./Files')
