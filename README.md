# Project Overview

## What is this project about?
This project let's you create a dataset of Armenian words for OCR (Optical Character Recognition) purposes. You can use the dataset to train an OCR model to recognize Armenian text in images.
You can generate the image dataset yourself by running the scripts in the repository, the instructions are already provided in this file.
You can also use the scraped words dataset as a lexicon for your OCR model.

## \hywiktionary

This folder contains the result of one full operation of all the scripts in the repository (Except for the generateor.py). You have access to the dataset of words in lowercase, uppercase, and capitalized forms, along with the corresponding reports in the `hywiktionary` folder. 

## Note on Images:
If you need the images, you will have to run the `generator` script. Due to the large size of the images dataset, the images are not included in the repository. If you need direct access to the images, feel free to contact me. 
Samples of what you'll get by running the script: 
![Տեխնոլոգիա_Emin_Script_14_0_0_0_rot0](https://github.com/user-attachments/assets/86fd538c-fbd9-47e8-8881-ca472e75ec8c)
![Տեխնոլոգիա_FreeSans_20_255_0_0_rot-5](https://github.com/user-attachments/assets/0d1c8e8d-10db-402e-8865-b19293e3e998)
![Տեխնոլոգիա_poqrik_24_0_255_0_rot-5](https://github.com/user-attachments/assets/18ea247f-0df1-4d3c-931b-8e9020b98bc3)


### Instructions:
1. Make sure to install the dependencies by running:
   ```bash
   pip install -r requirements.txt

## Scraper
You can use this script to scrape Armenian Wiktionary's newest updates. The script will start by filtering the words by each Armenian letter, then it will iterate over each page of the Wiktionary, collecting Armenian words that start with the specific letter of the iteration. 

### Result:
You'll get two output files:
- `armenian_words.json`
- `armenian_words_report.xlsx`

These will be saved in the `hywiktionary` directory.

## Modifier
If you're going to use this dataset as a training sample for your OCR model, you need to account for all cases – lowercase words, uppercase words, and capitalized words. This script will take your `armenian_words.json` file and add uppercase and capitalized versions of the words to the same `hywiktionary` directory.

## Generator
This script will generate a labeled image for each scraped word in each category (lowercase, uppercase, capitalized) and for each font available in the `fonts` folder. Additionally, it applies random transformations such as effects, colors, and other augmentations to the images. The final result will be a large dataset (over 20 GB) of labeled pictures of Armenian words.

## Notes for Future Improvements
There are many potential improvements for making the dataset more robust. For example:
- Add plural forms of words (e.g., "ներ").
- Introduce more fonts and backgrounds.
- Apply more variations to the transformations.

However, keep in mind that these improvements will likely increase the image dataset size, requiring more storage and training resources. You can also reduce the image quality and resolution to save space.
