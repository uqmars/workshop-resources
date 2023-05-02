import cv2 as cv
import numpy as np



def callback(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Print the BGR values of the image
        print(param[y, x])

        
def demo():
    cv.namedWindow('img', cv.WINDOW_NORMAL)
    cv.namedWindow('birb', cv.WINDOW_NORMAL)
    # Read the image as a png
    img = cv.imread('birb.png', cv.IMREAD_COLOR)
    cv.setMouseCallback('img', callback, img)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)

    # Copy the image data and set all channels to zero except the BLUE channel
    img_b = img.copy()
    img_b[:, :, 1] = 0
    img_b[:, :, 2] = 0
    img_b_gray = img[:, :, 0]

    # Copy the image data and set all channels to zero except the GREEN channel
    img_g = img.copy()
    img_g[:, :, 2] = 0
    img_g[:, :, 0] = 0
    img_g_gray = img[:, :, 1]

    # Copy the image data and set all channels to zero except the RED channel
    img_r = img.copy()
    img_r[:, :, 0] = 0
    img_r[:, :, 1] = 0
    img_r_gray = img[:, :, 2]

    # Convert the single channel images to BGR so it can be combined later
    img_b_gray = cv.cvtColor(img_b_gray, cv.COLOR_GRAY2BGR)
    img_g_gray = cv.cvtColor(img_g_gray, cv.COLOR_GRAY2BGR)
    img_r_gray = cv.cvtColor(img_r_gray, cv.COLOR_GRAY2BGR)

    # Combine the images together into one seamless image

    img_stack = np.vstack([
        np.hstack([img, img_b, img_g, img_r]),
        np.hstack([img_gray, img_b_gray, img_g_gray, img_r_gray])]
    )
    
    cv.imshow('birb', img_stack)
    cv.imshow('img', img)
    cv.waitKey()

if __name__ == "__main__":
    demo()
