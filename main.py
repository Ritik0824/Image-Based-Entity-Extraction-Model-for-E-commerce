import pandas as pd
import os
from src.utils import download_images, perform_ocr  # Assuming perform_ocr is implemented for OCR functionality
from src.constants import ALLOWED_UNITS
from src.sanity import run_sanity_check

# Load train and test data
train_data = pd.read_csv('dataset/train.csv')
test_data = pd.read_csv('dataset/test.csv')

# Directory where downloaded images will be stored
images_dir = 'images/'
os.makedirs(images_dir, exist_ok=True)

# Function to process image and extract entity value
def extract_entity_from_image(image_url):
    image_path = download_images(image_url, images_dir)
    extracted_text = perform_ocr(image_path)
    # Implement logic to parse text and extract value + unit
    value, unit = parse_entity(extracted_text)
    return value, unit

# Main function to generate predictions for the test set
def predict_entity(test_data):
    predictions = []
    for index, row in test_data.iterrows():
        image_url = row['image_link']
        value, unit = extract_entity_from_image(image_url)
        if value and unit in ALLOWED_UNITS:
            predictions.append(f"{value} {unit}")
        else:
            predictions.append("")
    return predictions

# Parse extracted text to find numeric values and valid units
def parse_entity(text):
    # Use regex or pattern matching to extract numbers and units
    import re
    # Simple regex for demonstration, you can make it more sophisticated
    pattern = r"(\d+(\.\d+)?)\s?(\w+)"
    match = re.search(pattern, text)
    if match:
        value = match.group(1)
        unit = match.group(3).lower()
        if unit in ALLOWED_UNITS:
            return value, unit
    return None, None

# Generate output in the required format
def generate_output():
    predictions = predict_entity(test_data)
    test_data['prediction'] = predictions
    test_data[['index', 'prediction']].to_csv('test_out.csv', index=False)

    # Run sanity check to validate output format
    run_sanity_check('test_out.csv')

if __name__ == "__main__":
    generate_output()