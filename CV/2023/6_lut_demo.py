import cv2
import numpy as np
import matplotlib.pyplot as plt


# Load the image
img = cv2.imread('birb.png', cv2.IMREAD_COLOR)

gamma = 0.3

i = np.arange(0, 256, 1)
hist_r = cv2.calcHist([img[:, :, 2]], [0], None, [256], [0,256])
hist_g = cv2.calcHist([img[:, :, 1]], [0], None, [256], [0,256])
hist_b = cv2.calcHist([img[:, :, 0]], [0], None, [256], [0,256])

get_red = lambda i: i
get_green = lambda i: i
get_blue = lambda i: i

red_curve = np.clip(get_red(i), 0, 255).astype(np.uint8)
green_curve = np.clip(get_green(i), 0, 255).astype(np.uint8)
blue_curve = np.clip(get_blue(i), 0, 255).astype(np.uint8)

# Apply the color curve LUTs to the image
img_out = np.zeros_like(img)
img_out[:, :, 0] = cv2.LUT(img[:, :, 0], blue_curve.flatten())
img_out[:, :, 1] = cv2.LUT(img[:, :, 1], green_curve.flatten())
img_out[:, :, 2] = cv2.LUT(img[:, :, 2], red_curve.flatten())


hist_out_r = cv2.calcHist([img_out[:, :, 2]], [0], None, [256], [0,256])
hist_out_g = cv2.calcHist([img_out[:, :, 1]], [0], None, [256], [0,256])
hist_out_b = cv2.calcHist([img_out[:, :, 0]], [0], None, [256], [0,256])

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)
ax0.plot(i / 255, hist_r, color='r')
ax0.plot(i / 255, hist_g, color='g')
ax0.plot(i / 255, hist_b, color='b')
ax0.set_ylim([0, 4096])

ax1.plot(i / 255, hist_out_r, color='r')
ax1.plot(i / 255, hist_out_g, color='g')
ax1.plot(i / 255, hist_out_b, color='b')
ax1.set_ylim([0, 4096])
plt.subplot(223)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.subplot(224)
plt.imshow(cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB))
plt.show()
