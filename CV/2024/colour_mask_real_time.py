import cv2
import numpy as np


# do this in real time
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([0, 50, 50])
    upper_yellow = np.array([50, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('image', frame)

    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
