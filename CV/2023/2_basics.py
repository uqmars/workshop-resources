import cv2 as cv
import numpy as np



def callback(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        # Print the BGR values of the image
        print(param[y, x])

        
def demo():
    
    # Read the image as a png
    img = cv.imread('birb.png', cv.IMREAD_COLOR)
    cv.imshow('img', img)
    cv.waitKey()

    # Converting to grayscale
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow('img_gray', img_gray)
    cv.waitKey()

    # Cropping
    x, y, w, h = (50, 50, 400, 500)
    img_cropped = img[y:y+h,x:x+w, :]
    cv.imshow('img_cropped', img_cropped)
    cv.waitKey()

    # Resizing
    img_resized = cv.resize(img, (128, 128))
    cv.imshow('img_resized', img_resized)
    cv.waitKey()

    # Setting values
    x, y, w, h = (100, 100, 50, 50)
    img_set = img.copy()
    img_set[y:y+h,x:x+w, :] = np.array([128, 128, 128])
    cv.imshow('img_set', img_set)
    cv.waitKey()

    # Evaluating conditions (e.g. clipping)
    img_clipping = img.copy()
    img_clipping[np.mean(img_clipping, axis=2) == 255] = np.array([0, 0, 255])
    img_clipping[np.mean(img_clipping, axis=2) == 0] = np.array([255, 0, 0])
    cv.imshow('img_clipping', img_clipping)
    cv.waitKey()


    cv.destroyAllWindows()

if __name__ == "__main__":
    demo()