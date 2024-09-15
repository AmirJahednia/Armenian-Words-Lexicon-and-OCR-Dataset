import json
import os

# Get the current working directory
cwd = os.getcwd()

# Construct the full path to the input and output file
input_file = os.path.join(cwd, 'hywiktionary', 'armenian_words.json')
uppercase_output_file = os.path.join(cwd, 'hywiktionary', 'armenian_words_uppercase.json')
capitalized_output_file = os.path.join(cwd, 'hywiktionary', 'armenian_words_capitalized.json')


# Function to convert words to uppercase for each key
def convert_to_uppercase(data):
    # Loop through each key and convert associated words to uppercase
    for key in data:
        data[key] = [word.upper() for word in data[key]]
    return data

# Function to capitalize the first letter of each word for each key
def capitalize_first_letter(data):
    # Loop through each key and capitalize the first letter of associated words
    for key in data:
        data[key] = [word.capitalize() for word in data[key]]
    return data

# Load the JSON file
with open(input_file, 'r', encoding='utf-8') as file:
    armenian_words = json.load(file)

# Convert words to uppercase (create a copy to avoid overwriting)
armenian_words_uppercase = convert_to_uppercase(armenian_words.copy())


with open(input_file, 'r', encoding='utf-8') as file:
    armenian_words = json.load(file)  # Reload to ensure original data is intact

armenian_words_capitalized = capitalize_first_letter(armenian_words.copy())

# Save the new data to new JSON files
with open(uppercase_output_file, 'w', encoding='utf-8') as file:
    json.dump(armenian_words_uppercase, file, ensure_ascii=False, indent=4)

with open(capitalized_output_file, 'w', encoding='utf-8') as file:
    json.dump(armenian_words_capitalized, file, ensure_ascii=False, indent=4)

print(f"Uppercase words have been saved to {uppercase_output_file}")
print(f"Capitalized words have been saved to {capitalized_output_file}")
