import cv2
import numpy as np

appleImg = cv2.imread('apples.jpg')

# convert the image to HSV colour space
hsv_apple = cv2.cvtColor(appleImg, cv2.COLOR_BGR2HSV)

# define colour mask for red apples
lower_red = (0, 10, 100)  # lower bound for red in HSV
upper_red = (20, 255, 255)  # upper bound for red in HSV

lower_purple = (170, 10, 100)
upper_purple = (180, 255, 255)  # upper bound for red in HSV

# create a mask for red apples
appleMask = cv2.inRange(hsv_apple, lower_red, upper_red) + cv2.inRange(hsv_apple, lower_purple, upper_purple)

# Find contours in the mask
contours, _ = cv2.findContours(appleMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a new empty mask for filtered contours
filtered_mask = np.zeros_like(appleMask)

# Filter contours by area and draw only the large ones
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 2000:  # Only include contours with area > 2000 pixels
        cv2.drawContours(filtered_mask, [contour], 0, 255, -1)  # Fill the contour

# apply the filtered mask to the image
appleResult = cv2.bitwise_and(appleImg, appleImg, mask=filtered_mask)

# Display original mask and filtered mask for comparison
cv2.imshow('Original Mask', appleMask)
cv2.imshow('Filtered Mask', filtered_mask)
cv2.imshow('Filtered Apple Result', appleResult)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()