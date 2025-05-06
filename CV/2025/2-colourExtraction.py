import cv2

hsvImg = cv2.imread('HSVopenCV.png')
appleImg = cv2.imread('apples.jpg')

### 1: convert the image to HSV colour space
hsv_apple = cv2.cvtColor(appleImg, cv2.COLOR_BGR2HSV)
hsv_hsvImg = cv2.cvtColor(hsvImg, cv2.COLOR_BGR2HSV)


### 2: define colour mask for red apples
lower_red = (0, 10, 100)  # lower bound for red in HSV
upper_red = (20, 255, 255)  # upper bound for red in HSV

lower_purple = (170, 10, 100)
upper_purple = (180, 255, 255)  # upper bound for red in HSV

### 3: create a binary mask for red apples
appleMask = cv2.inRange(hsv_apple, lower_red, upper_red) + cv2.inRange(hsv_apple, lower_purple, upper_purple)
coneMask = cv2.inRange(hsv_hsvImg, lower_red, upper_red) + cv2.inRange(hsv_hsvImg, lower_purple, upper_purple)
print(coneMask)

### 4: apply the mask to the image
appleResult = cv2.bitwise_and(appleImg, appleImg, mask=appleMask)
coneResult = cv2.bitwise_and(hsvImg, hsvImg, mask=coneMask)

cv2.imshow('apple', appleResult)
cv2.imshow('cone', coneResult)
cv2.waitKey(0)  # Wait for a key press to close the window