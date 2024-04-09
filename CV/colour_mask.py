import cv2
import numpy as np

img = cv2.imread('plane2.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_yellow = np.array([5, 150, 50])
upper_yellow = np.array([25, 255, 255])

mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

res = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('image', img)

cv2.imshow('mask', mask)

cv2.imshow('res', res)

cv2.waitKey(0)
