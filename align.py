import cv2
import numpy as np

# Load the image
img = cv2.imread('12.jpeg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Detect lines using Hough transform
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

# Filter lines to keep only vertical lines
vertical_lines = []
for line in lines:
    rho, theta = line[0]
    if np.abs(theta - np.pi/2) < np.pi/6:
        vertical_lines.append(line)

# Sort vertical lines by their x-coordinates
vertical_lines = sorted(vertical_lines, key=lambda x: x[0][0])

# Calculate angle of first vertical line
rho, theta = vertical_lines[0][0]
angle = theta * 180 / np.pi

# Create rotation matrix to deskew image
rows, cols = img.shape[:2]
M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)

# Apply rotation matrix to image
deskewed = cv2.warpAffine(img, M, (cols, rows))

# Display original and deskewed images
cv2.imshow('Original', img)
cv2.imshow('Deskewed', deskewed)
cv2.waitKey(0)
cv2.destroyAllWindows()