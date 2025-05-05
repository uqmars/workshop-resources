import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('flyingapple.mp4')

positions = [] 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV colour space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define colour mask for red apples
    lower_red = (0, 150, 10)  # lower bound for red in HSV
    upper_red = (20, 255, 255)  # upper bound for red in HSV

    lower_purple = (165, 150, 10)
    upper_purple = (180, 255, 255)  # upper bound for red in HSV

    # Create a binary mask for red apples
    appleMask = cv2.inRange(hsv_frame, lower_red, upper_red) + cv2.inRange(hsv_frame, lower_purple, upper_purple)
    
    # Filter small objects (optional, for better tracking)
    contours, _ = cv2.findContours(appleMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_mask = np.zeros_like(appleMask)
    for contour in contours:
        if cv2.contourArea(contour) > 10:  # Only include contours with area > 2000 pixels
            cv2.drawContours(filtered_mask, [contour], 0, 255, -1)
    
    # Use the filtered mask for tracking
    appleMask = filtered_mask

    # Apply the mask to the frame
    appleResult = cv2.bitwise_and(frame, frame, mask=appleMask)

    # Calculate the average location of the apples using moments
    M = cv2.moments(appleMask)
    
    # Check if any white pixels are in the mask
    if M["m00"] != 0:
        # Calculate the centroid coordinates
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        # Draw a circle at the centroid
        cv2.circle(frame, (cX, cY), 20, (0, 255, 0), 2)
        cv2.circle(appleResult, (cX, cY), 20, (0, 255, 0), 2)
        
        # Add text label
        cv2.putText(frame, f"Center: ({cX}, {cY})", (cX - 70, cY - 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        positions.append((cX, cY))

    # Display the original frame with tracking and the masked result
    cv2.imshow('Apple Tracking', frame)
    cv2.imshow('Apple Detection', appleResult)
    
    #time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# calculate velocity and acceleration
velocities = []
for i in range(1, len(positions)):
    dy = positions[i][1] - positions[i-1][1]
    velocities.append(dy)
print("Velocity:", velocities)

# plot the trajectory of the apple
plt.figure(figsize=(10, 6))
plt.plot([pos[0] for pos in positions], [pos[1] for pos in positions], marker='o', markersize=5, linestyle='-', color='b')
plt.title('Apple Trajectory')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.xlim(0, 400)  # Adjust according to your video resolution
plt.ylim(0, 480)  # Adjust according to your video resolution
plt.gca().invert_yaxis()  # Invert y-axis to match the video coordinate system
plt.grid()

plt.figure(figsize=(10, 6))
plt.plot([vel for vel in velocities[:-1]], marker='o', markersize=5, linestyle='-', color='r')
plt.title('Apple Velocity')
plt.xlabel('X Velocity')
plt.ylabel('Y Velocity')
plt.xlim(0, 80)  # Adjust according to your velocity range
plt.ylim(-100, 100)  # Adjust according to your velocity range


plt.show()