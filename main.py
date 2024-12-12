import cv2
import pytesseract
from PIL import Image
import re

# Path to the image
image_path = '/Users/parishibhange/Desktop/WhatsApp.jpeg'

# Step 1: Load the image
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Unable to load image at path '{image_path}'. Ensure the file exists.")
else:
    # Step 2: Preprocess the image
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to clean the image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Save the processed image (optional, for debugging)
    cv2.imwrite('processed_image.jpg', thresh)

    # Convert the image to a PIL Image object for Tesseract
    pil_img = Image.fromarray(thresh)

    # Step 3: Extract text using Tesseract OCR
    # Ensure Tesseract is installed and accessible via the system path
    text = pytesseract.image_to_string(pil_img, lang='eng')

    # Step 4: Print the extracted text (optional, for debugging)
    print("Extracted text: ", text)

    # Step 5: Extract specific information
    # Regular expression for Aadhar number (12-digit format)
    aadhar_number = re.search(r'\d{4}\s?\d{4}\s?\d{4}', text)

    if aadhar_number:
        print("Aadhar Number: ", aadhar_number.group())
    else:
        print("Aadhar number not found.")

    # Regular expression for Date of Birth (DOB)
    dob_match = re.search(r'(DOB|D.O.B|Date of Birth|जन्म तिथि)[\s:]+(\d{2}/\d{2}/\d{4})', text)
    if dob_match:
        print("Date of Birth (DOB):", dob_match.group(2))
    else:
        print("Date of Birth not found.")

    # Regular expression for Father's Name
    father_name_match = re.search(r'(Father\s?:|पिता\s?:)[\s]*([A-Za-z\s]+)', text)
    if father_name_match:
        print("Father's Name:", father_name_match.group(2).strip())
    else:
        print("Father's Name not found.")
