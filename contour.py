import cv2 
import numpy as np

image = cv2.imread("image0.jpg")
print(image.shape)
grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

thresholded_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
inverted_image = cv2.bitwise_not(thresholded_image)
dilated_image = inverted_image
img_copy = image.copy()

def find_contours(image):
    contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Below lines are added to show all contours
    # This is not needed, but it is useful for debugging
    image_with_all_contours = image.copy()
    cv2.drawContours(image_with_all_contours, contours, -1, (0, 255, 0), 3)

    return contours, image_with_all_contours


def filter_contours_and_leave_only_rectangles(contour, image):
    rectangular_contours = []
    for contour in contour:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            rectangular_contours.append(approx)
    # Below lines are added to show all rectangular contours
    # This is not needed, but it is useful for debugging
    image_with_only_rectangular_contours = image.copy()
    cv2.drawContours(image_with_only_rectangular_contours, rectangular_contours, -1, (0, 255, 0), 3)

    return rectangular_contours, image_with_only_rectangular_contours

def find_largest_contour_by_area(filter, image):
    max_area = 0
    contour_with_max_area = None
    for contour in filter:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            contour_with_max_area = contour
    # Below lines are added to show the contour with max area
    # This is not needed, but it is useful for debugging
    image_with_contour_with_max_area = image.copy()
    cv2.drawContours(image_with_contour_with_max_area, [contour_with_max_area], -1, (0, 255, 0), 3)

    return contour_with_max_area, image_with_contour_with_max_area

contour, img_contour = find_contours(img_copy)
filter, img_rect = filter_contours_and_leave_only_rectangles(contour,img_copy)
contourmax, img_large = find_largest_contour_by_area(filter, img_copy)

listContour = contourmax.tolist()

src =np.float32([listContour[0][0],listContour[3][0], listContour[1][0],listContour[2][0]])
# Define the destination points
dst = np.float32([[0, 0], [image.shape[1], 0], [0, image.shape[0]], [image.shape[1], image.shape[0]]])

# Compute the perspective transformation matrix
M = cv2.getPerspectiveTransform(src, dst)

# Apply the transformation to the input image
warped_img = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))
print(src)


cv2.imshow('deka', thresholded_image)
cv2.imshow('inv', inverted_image)
cv2.imshow('dist', dilated_image)
cv2.imshow("gray", img_large)
cv2.imshow("persp", warped_img)

cv2.waitKey(0)
cv2.destroyAllWindows