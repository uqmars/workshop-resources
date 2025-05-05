import cv2

img = cv2.imread('HSVopenCV.png')


print(img)
print(img.shape)  # (height, width, channels)
print(img.size)   # total number of pixels (height * width * channels)
print(img.dtype)  # data type of the pixel values (e.g., uint8)

imshow = cv2.imshow('Image', img)
cv2.waitKey(0)  # Wait for a key press to close the window