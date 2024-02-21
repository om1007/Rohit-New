import cv2
import matplotlib.pyplot as plt
import easyocr
from deep_translator import GoogleTranslator

# Read the image (ensure correct format)
img = cv2.imread("C:/Users/ARNAV/OneDrive/Desktop/om/Screenshot 2024-02-21 135935.png", cv2.IMREAD_COLOR)

# Function to detect and return text
def detect_language():
    global text_  # Indicate modification of global variable
    for reader in reader_array:
        try:
            text_ = reader.readtext(img)
            return text_  # Return detected text
        except Exception as e:  # Handle any exceptions
            print("Error in reader:", reader, e)

    return None  # Return None if no text detected

# Language readers, adjust languages as needed
reader_array = [
    easyocr.Reader(['hi', 'mr', 'ne'], gpu=False),
    easyocr.Reader(['ar', 'fa', 'ur'], gpu=False),
    easyocr.Reader(['fr', 'es', 'ga', 'de'], gpu=False),
    easyocr.Reader(['ru', 'rs_cyrillic', 'bg', 'uk', 'mn', 'be'], gpu=False),
]

# Detect text and return translated text if available
text_ = detect_language()

# Create GoogleTranslator instance
translator = GoogleTranslator(source='auto', target='en')

# Initialize empty list for translated text
translated_text = []

# Translate and store if text is detected
if text_:
    for bbox, text, score in text_:
        try:  # Handle potential translation errors
            translated = translator.translate(text)
            translated_text.append((bbox, translated, score))
        except Exception as e:
            print("Error in translation:", text, e)

# Draw bounding boxes and text
for bbox, text_to_display, score in translated_text:
    # Extract coordinates and ensure data types
    x1, y1 = int(bbox[0][0]), int(bbox[0][1])
    x2, y2 = int(bbox[2][0]), int(bbox[2][1])

    # Print coordinates for debugging (optional)
    # print("Coordinates:", x1, y1, x2, y2)

    # Draw rectangle and text
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.putText(img, text_to_display, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 0, 0), 3)

# Display the image with results
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
