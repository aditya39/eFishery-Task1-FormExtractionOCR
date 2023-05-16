
import cv2
import numpy as np

img = cv2.imread('12.jpeg')

# Define the source points
src = np.float32([[470, 206], [1479, 198], [32, 1122], [1980, 1125]])

# Draw the source points on the input image
for point in src:
    cv2.circle(img, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)


# Define the source points
src = np.float32([[70, 30], [221, 29], [5, 166], [294, 166]])

# Define the destination points
dst = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])

# Compute the perspective transformation matrix
M = cv2.getPerspectiveTransform(src, dst)

# Apply the transformation to the input image
warped_img = cv2.warpPerspective(img, M, (500, 600))

# Draw the destination points on the output image
for point in dst:
    cv2.circle(warped_img, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)

cv2.imshow("ori", img)

cv2.imshow('Warped Image', warped_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

def perspectiveWarp(img):
        # Define the source points
    src = np.float32([[470, 206], [1479, 198], [32, 1122], [1980, 1125]])

    # Draw the source points on the input image
    for point in src:
        cv2.circle(img, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)


    # Define the source points
    src = np.float32([[70, 30], [221, 29], [5, 166], [294, 166]])

    # Define the destination points
    dst = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])

    # Compute the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src, dst)

    # Apply the transformation to the input image
    warped_img = cv2.warpPerspective(img, M, (500, 600))

    # Draw the destination points on the output image
    for point in dst:
        cv2.circle(warped_img, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)