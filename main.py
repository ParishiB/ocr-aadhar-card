import cv2
import pytesseract
import re

image_path = '/Users/parishibhange/Desktop/WhatsApp.jpeg'

extracted_info = {
    "name": '',
    "aadhar_number": '',
    "father_name": '',
    "dob": '',
    "image": ''
}


img = cv2.imread(image_path)
if img is None:
    print(f"Error: Unable to load image at path '{image_path}'. Ensure the file exists.")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(blurred, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        x, y, w, h = faces[0]

        person_image = img[y:y+h, x:x+w]

        output_path = 'extracted_person_image.jpg'
        extracted_info['image'] = output_path
        cv2.imwrite(output_path, person_image)

    else:
        print("No faces detected in the image.")

    text = pytesseract.image_to_string(img, lang='eng')
    aadhar_number = re.search(r'\d{4}\s?\d{4}\s?\d{4}', text)

    if aadhar_number:
        extracted_info['aadhar_number'] = aadhar_number.group()
    else:
        print("Aadhar number not found.")

    name_match = re.search(r'([A-Za-z\s]+)\s*Father', text)
    if name_match:
        extracted_info['name'] = name_match.group(1).strip()
    else:
        print("Name not found.")

    dob_match = re.search(r'(DOB|D.O.B|Date of Birth|जन्म तिथि)[\s:]+(\d{2}/\d{2}/\d{4})', text)
    if dob_match:
        extracted_info['dob'] =  dob_match.group(2)
    else:
        print("Date of Birth not found.")

    father_name_match = None  
    try:
        father_name_match = re.search(r'Father(?:[\s:]+)([A-Za-z]+(?:\s[A-Za-z]+)+)', text)
    except Exception as e:
        print(f"Error during regex matching: {e}")

    if father_name_match:
        father_name = father_name_match.group(1).strip()

        cleaned_father_name = re.sub(r'\s*aie\s*FAP\s*', '', father_name)
        extracted_info['father_name'] = cleaned_father_name
    else:
        print("Father's Name not found.")

print("the user info" , extracted_info)

