import cv2
import numpy as np

img = cv2.imread('plane2.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_yellow = np.array([5, 150, 50])
upper_yellow = np.array([25, 255, 255])

mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

cv2.imshow('mask', mask)

res = cv2.bitwise_and(img, img, mask=mask)

# only display largest area of mask
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cont = contours[max_index]
mask_cont = np.zeros_like(mask)
cv2.drawContours(mask_cont, [cont], -1, 255, -1)
mask = cv2.bitwise_and(mask, mask, mask=mask_cont)

# bitwise and with hsv image
res = cv2.bitwise_and(img, img, mask=mask)


cv2.imshow('image', img)

cv2.imshow('mask cont', mask)

cv2.imshow('res', res)

cv2.waitKey(0)
