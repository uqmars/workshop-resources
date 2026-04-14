import numpy as np
import cv2 as cv

# Camera Settings
CAMERA_INDEX = 0

# Chessboard settings
CHESSBOARD_SIZE = (9, 7)

# Termination criteria for corner refinement
criteria = (
    cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
    30,
    0.001,
)

# Prepare object points: (0,0,0), (1,0,0), (2,0,0), ...
objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)

# Arrays to store object points and image points
objpoints = []
imgpoints = []

cap = cv.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError("Cannot open camera")

print("Press SPACE to capture a calibration image")
print("Press C to calibrate once you have enough images")
print("Press Q to quit")

calibrated = False
mtx = None
dist = None
last_gray_shape = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    display = frame.copy()

    # Show how many valid captures have been collected
    cv.putText(
        display,
        f"Captured views: {len(objpoints)}",
        (20, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv.LINE_AA,
    )
    cv.putText(
        display,
        "SPACE: capture   C: calibrate   Q: quit",
        (20, 65),
        cv.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2,
        cv.LINE_AA,
    )

    cv.imshow("img", display)
    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    elif key == ord(" "):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        last_gray_shape = gray.shape[::-1]

        found, corners = cv.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

        preview = frame.copy()

        if found:
            refined_corners = cv.cornerSubPix(
                gray,
                corners,
                (11, 11),
                (-1, -1),
                criteria,
            )

            objpoints.append(objp.copy())
            imgpoints.append(refined_corners)

            cv.drawChessboardCorners(preview, CHESSBOARD_SIZE, refined_corners, found)
            print(f"Captured calibration frame {len(objpoints)}")
        else:
            print("Chessboard not found in this frame")

        cv.imshow("img", preview)
        cv.waitKey(500)

    elif key == ord("c"):
        if len(objpoints) < 3:
            print("Not enough calibration images yet. Capture a few more first.")
            continue

        if last_gray_shape is None:
            print("No valid grayscale image available for calibration.")
            continue

        ret_cal, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
            objpoints,
            imgpoints,
            last_gray_shape,
            None,
            None,
        )

        calibrated = True

        print("\nCalibration complete")
        print(f"RMS reprojection error: {ret_cal}")
        print("Camera matrix:")
        print(mtx)
        print("Distortion coefficients:")
        print(dist.ravel())

        # Save as separate .npy files
        np.save("ret.npy", ret_cal)
        np.save("mtx.npy", mtx)
        np.save("dist.npy", dist)
        np.save("rvecs.npy", np.array(rvecs, dtype=object))
        np.save("tvecs.npy", np.array(tvecs, dtype=object))

        print("Saved calibration to:")
        print("  ret.npy")
        print("  mtx.npy")
        print("  dist.npy")
        print("  rvecs.npy")
        print("  tvecs.npy")

        break

if calibrated:
    print("\nShowing live undistorted view. Press Q to quit.")

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        h, w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(
            mtx, dist, (w, h), 1, (w, h)
        )

        undistorted = cv.undistort(img, mtx, dist, None, newcameramtx)

        x, y, roi_w, roi_h = roi
        if roi_w > 0 and roi_h > 0:
            undistorted_cropped = undistorted[y:y + roi_h, x:x + roi_w]
        else:
            undistorted_cropped = undistorted

        cv.imshow("img", img)
        cv.imshow("img_undistorted", undistorted_cropped)

        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break

cap.release()
cv.destroyAllWindows()