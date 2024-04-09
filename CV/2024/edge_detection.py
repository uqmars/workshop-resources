import cv2
 
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.imshow('Original', frame)
 
    # Convert to graycsale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=50, threshold2=200) # Canny Edge Detection
    # Display Canny Edge Detection Image
    cv2.imshow('Canny Edge Detection', edges)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break