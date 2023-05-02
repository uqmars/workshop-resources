import numpy as np
import cv2 as cv

#! pip3 install git+https://github.com/pvigier/perlin-numpy

from perlin_numpy import generate_fractal_noise_2d

cap = cv.VideoCapture(1)

# https://en.wikipedia.org/wiki/Kernel_(image_processing)

SHARPEN_KERNEL = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

UNSHARP_KERNEL = np.array([
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, -476, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1]
]) / -256


BOX_BLUR_KERNEL = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]) / 9.0

GAUSSIAN_3x3_KERNEL = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]) / 16

GAUSSIAN_5x5_KERNEL = np.array([
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1]
]) / 256


SOBEL_X_KERNEL = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1],
])

SOBEL_Y_KERNEL = np.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1],
])

filter_type = 0

if not cap.isOpened():
    print("Cannot open camera")
    exit()

cv.namedWindow('frame', cv.WINDOW_NORMAL)



def sepia(img):
    # Transforms the BGR value of an image to match a sepia filter
    img_sepia = np.array(img, dtype=np.float64) / 255.0
    sepia_matrix = np.matrix([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])
    img_sepia = cv.transform(img_sepia, sepia_matrix)
    img_sepia = np.clip(img_sepia, 0.0, 1.0)
    return np.array(img_sepia * 255.0, dtype=np.uint8)

perlin_noise = generate_fractal_noise_2d((1024, 1024), (128, 128), 4) * 0.1 - 0.5

while True:
    ret, img = cap.read()

    if not ret:
        break

    cv.resizeWindow('frame', (img.shape[1] // 2, img.shape[0] // 2))

    img_resized = cv.resize(img, (img.shape[1] // 4, img.shape[0] // 4))
    img_sharpen = cv.filter2D(img_resized, -1, SHARPEN_KERNEL)
    img_unsharp = cv.filter2D(img_resized, -1, UNSHARP_KERNEL)
    img_box_blur = cv.filter2D(img_resized, -1, BOX_BLUR_KERNEL)
    img_gaussian_3x3 = cv.filter2D(img_resized, -1, GAUSSIAN_3x3_KERNEL)
    img_gaussian_5x5 = cv.filter2D(img_resized, -1, GAUSSIAN_5x5_KERNEL)
    img_sobel_x = cv.filter2D(img_resized, -1, SOBEL_X_KERNEL).astype(np.float64) / 255.0
    img_sobel_y = cv.filter2D(img_resized, -1, SOBEL_Y_KERNEL).astype(np.float64) / 255.0
    img_sobel = (255 * np.sqrt(img_sobel_x ** 2 + img_sobel_y ** 2)).astype(np.uint8)

    img_sepia = sepia(img_resized)
    img_sepia_hsv = cv.cvtColor(img_sepia, cv.COLOR_BGR2HSV)


    img_perlin = np.array(255.0 * 0.5 * (perlin_noise[:img_resized.shape[0], :img_resized.shape[1]]), dtype=np.int64)
    img_sepia_hsv[:, :, 2] = cv.add(img_sepia_hsv[:, :, 2], img_perlin, dtype=cv.CV_8U)
    img_grainy = cv.cvtColor(img_sepia_hsv, cv.COLOR_HSV2BGR)
    img_hsv = cv.cvtColor(img_resized, cv.COLOR_BGR2HSV)
    img_h = img_hsv[:, :, 0].copy()
    img_s = img_hsv[:, :, 1].copy()
    img_v = img_hsv[:, :, 2].copy()
    
    thresh_val = 50
    _, img_thresh_upper = cv.threshold(img_h, thresh_val, 255, cv.THRESH_BINARY_INV)
    _, img_thresh_lower = cv.threshold(img_h, 255 - thresh_val, 255, cv.THRESH_BINARY)
    _, img_thresh_sat = cv.threshold(img_h, 64, 255, cv.THRESH_BINARY)
    _, img_thresh_val = cv.threshold(img_v, 64, 255, cv.THRESH_BINARY)

    img_thresh = (img_thresh_upper | img_thresh_lower)

    filter_names = ['Unfiltered', 'Sharpen', 'Unsharp', 'Box Blur', 'Gaussian 3x3', 'Gaussian 5x5', 'Sobel', 'Sepia', 'Grainy', 'Threshold']
    cv.imshow('original', img_resized)
    if filter_type == 0:
        cv.imshow('frame', img_resized)
    elif filter_type == 1:
        cv.imshow('frame', img_sharpen)
    elif filter_type == 2:
        cv.imshow('frame', img_unsharp)
    elif filter_type == 3:
        cv.imshow('frame', img_box_blur)
    elif filter_type == 4:
        cv.imshow('frame', img_gaussian_3x3)
    elif filter_type == 5:
        cv.imshow('frame', img_gaussian_5x5)
    elif filter_type == 6:
        cv.imshow('frame', img_sobel)
    elif filter_type == 7:
        cv.imshow('frame', img_sepia)
    elif filter_type == 8:
        cv.imshow('frame', img_grainy)
    elif filter_type == 9:
        cv.imshow('frame', img_thresh)
    c = cv.waitKey(1)
    if c == ord('q'):
        break
    elif c == ord(' '):
        filter_type = ((filter_type + 1) % 10)
        print(filter_names[filter_type])


cap.release()
cv.destroyAllWindows()
