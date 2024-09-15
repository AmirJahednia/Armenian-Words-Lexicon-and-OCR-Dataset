import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import os
from datetime import datetime

armenian_alphabet = ['ա', 'բ', 'գ', 'դ', 'ե', 'զ', 'է', 'ը', 'թ', 'ժ', 'ի', 'լ', 'խ', 'ծ', 'կ', 'հ', 'ձ', 'ղ', 'ճ', 'մ', 'յ', 'ն', 'շ', 'ո', 'չ', 'պ', 'ջ', 'ռ', 'ս', 'վ', 'տ', 'ր', 'ց', 'ու', 'փ', 'ք', 'և', 'օ', 'ֆ']

counter = 1  # Tracks pages scraped
overall_counter = 1 # keep track of the overall number of pages scraped
total_words = 0  # Tracks total number of words scraped

# Dictionary to store words for each letter for JSON output
words_dict = {}

# List to store report data for each letter
report_data = []

def scrape_armenian_words(soup, letter):
    # to find the armenian words in the html
    armenian_regex = re.compile(r'[\u0530-\u058F]+')
    words = []

    # at the moment in wiktionary the armenian words are in the <li> tags.
    for li in soup.find_all('li'):
        word = li.get_text().strip()
        # Ensure the word starts with the correct letter (don't scrape random words used in the page structure itself)
        if armenian_regex.fullmatch(word) and word.startswith(letter):
            words.append(word)
    return words

def get_next_page(soup, letter):
    global counter
    global overall_counter
    # currently the next page is in the <div> tag with the class 'mw-prefixindex-nav'
    next_div = soup.find('div', class_='mw-prefixindex-nav')
    if next_div:
        next_link = next_div.find('a')
        if next_link:
            counter += 1
            overall_counter += 1
            print(f'{letter} - Page {counter}')
            return 'https://hy.wiktionary.org' + next_link['href']
    return None

def scrape_all_words(url, letter):
    global counter
    counter = 1  # Reset counter for each letter
    all_words = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_words.extend(scrape_armenian_words(soup, letter))
        url = get_next_page(soup, letter)
    return all_words

def save_to_json(words_dict, json_filename):
    # Ensure the 'results' directory exists
    folder_path = os.path.join(os.getcwd(), 'hywiktionary')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save to JSON with the desired structure
    json_file_path = os.path.join(folder_path, json_filename)
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(words_dict, file, ensure_ascii=False, indent=4)

def save_report_to_xlsx(report_data, total_words, filename='report.xlsx'):
    # Create a DataFrame from report_data
    df = pd.DataFrame(report_data)
    
    # Add Date and Time and total words in the last row, under the same columns
    date_scraped = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total_row = pd.DataFrame([{'letter': 'Total', 'pages_scraped': f'{overall_counter} pages at {date_scraped}', 'words_scraped': total_words}])
    df = pd.concat([df, total_row], ignore_index=True)
    
    # Ensure the 'results' directory exists
    folder_path = os.path.join(os.getcwd(), 'hywiktionary')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save to .xlsx
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)

# Loop through the entire Armenian alphabet and scrape data for each prefix
for letter in armenian_alphabet:
    
    # the {letter} variable is the current letter of the iteration.
    url = f'https://hy.wiktionary.org/wiki/%D5%8D%D5%BA%D5%A1%D5%BD%D5%A1%D6%80%D5%AF%D5%B8%D5%B2:%D5%88%D6%80%D5%B8%D5%B6%D5%B8%D6%82%D5%B4%D5%B6%D5%A1%D5%AD%D5%A1%D5%AE%D5%A1%D5%B6%D6%81%D5%B8%D5%BE?prefix={letter}&namespace=0'
    
    # Scrape all words starting with the current letter
    all_words = scrape_all_words(url, letter)
    
    # Update the words_dict for JSON
    words_dict[letter] = all_words
    
    # Update report data
    total_words += len(all_words)
    report_data.append({
        'letter': letter,
        'pages_scraped': counter,
        'words_scraped': len(all_words)
    })
    
    print(f"Scraped and added words for '{letter}'. The prefix '{letter}' had {counter} pages and {len(all_words)} words.")

# Save the words dictionary to a single JSON file
save_to_json(words_dict, 'armenian_words.json')

# Save the report to a single .xlsx file
save_report_to_xlsx(report_data, total_words, 'armenian_words_report.xlsx')

print(f"Total words scraped: {total_words}")
