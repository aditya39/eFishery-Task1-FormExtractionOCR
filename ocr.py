import pytesseract
from PIL import Image
import cv2

image = cv2.imread("1.jpg")
text = pytesseract.image_to_string(image)
print(text)