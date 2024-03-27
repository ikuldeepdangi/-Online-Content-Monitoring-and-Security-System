import pytesseract
from PIL import Image

def ocr_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

# Test OCR
if __name__ == '__main__':
    image_path = 'test_image.png'
    ocr_text = ocr_image(image_path)
    print(ocr_text)
