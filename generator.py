import os
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Define directories
fonts_dir = 'fonts'
output_dir = 'output_word_images'
json_dir = 'hywiktionary'

# Define parameters
font_sizes = [14, 20, 24, 30]
font_colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
bg_colors = [(255, 255, 255), (200, 200, 200), (220, 220, 220), (240, 240, 240)]
rotations = [-10, -5, 0, 5, 10]

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load fonts
fonts = [os.path.join(fonts_dir, font) for font in os.listdir(fonts_dir) if font.endswith('.ttf') or font.endswith('.otf')]

def create_word_image(word, font_path, font_size, font_color, bg_color, output_path):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (300, 300), color=bg_color) # 300x300 is the size of the image, change it if you want to reduce the size of the images
    draw = ImageDraw.Draw(image)

    # Calculate text size and position to center it
    bbox = draw.textbbox((0, 0), word, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Apply random rotation
    angle = random.choice(rotations)
    
    # Random position with slight jitter
    jitter_x, jitter_y = random.randint(-3, 3), random.randint(-3, 3)
    position = ((300 - text_width) // 2 + jitter_x, (300 - text_height) // 2 + jitter_y)

    # Draw the word on the image
    draw.text(position, word, fill=font_color, font=font)

    # Apply random noise/distortion
    if random.random() > 0.7:
        image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.1, 1.5)))
    
    # Rotate the image
    image = image.rotate(angle, expand=1, fillcolor=bg_color)
    
    # Save the image
    font_name = os.path.splitext(os.path.basename(font_path))[0]
    color_name = f"{font_color[0]}_{font_color[1]}_{font_color[2]}"
    image_name = f"{word}_{font_name}_{font_size}_{color_name}_rot{angle}.png"
    image_path = os.path.join(output_path, image_name)
    image.save(image_path, 'JPEG', quality=85)

# Organize output folders by case (lowercase, uppercase, capitalized)
cases = {
    'lowercase': 'armenian_words.json',
    'uppercase': 'armenian_words_uppercase.json',
    'capitalized': 'armenian_words_capitalized.json'
}

for case, json_file in cases.items():
    with open(os.path.join(json_dir, json_file), 'r', encoding='utf-8') as file:
        words_dict = json.load(file)

    # Create directory for each case (lowercase, uppercase, capitalized)
    case_dir = os.path.join(output_dir, case)
    if not os.path.exists(case_dir):
        os.makedirs(case_dir)

    for letter, words in words_dict.items():
        # Create directory for each letter within the case folder
        letter_dir = os.path.join(case_dir, letter)
        if not os.path.exists(letter_dir):
            os.makedirs(letter_dir)
        
        for word in words:
            for font in fonts:
                font_size = random.choice(font_sizes)
                font_color = random.choice(font_colors)
                bg_color = random.choice(bg_colors)
                create_word_image(word, font, font_size, font_color, bg_color, letter_dir)

# Add numbers (0-9) generation
numbers = [str(i) for i in range(10)]
numbers_dir = os.path.join(output_dir, 'numbers')

# Create numbers directory if it doesn't exist
if not os.path.exists(numbers_dir):
    os.makedirs(numbers_dir)

for number in numbers:
    # Create a folder for each number (0, 1, 2, ..., 9)
    number_folder = os.path.join(numbers_dir, number)
    if not os.path.exists(number_folder):
        os.makedirs(number_folder)

    for font in fonts:
        font_size = random.choice(font_sizes)
        font_color = random.choice(font_colors)
        bg_color = random.choice(bg_colors)
        create_word_image(number, font, font_size, font_color, bg_color, number_folder)

print("Image generation complete.")
