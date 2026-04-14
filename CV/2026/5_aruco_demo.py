import numpy as np
import cv2 as cv


# ----------------------------
# User settings
# ----------------------------
MARKER_LENGTH_M = 0.050   # 50 mm
CAMERA_INDEX = 0
WINDOW_NAME = "frame"


def marker_object_points(marker_length: float) -> np.ndarray:
    """
    3D object points for one square marker, centered at the marker center.
    Corner order must match ArUco's detected corner order:
    top-left, top-right, bottom-right, bottom-left.
    """
    half = marker_length / 2.0
    return np.array(
        [
            [-half,  half, 0.0],  # top-left
            [ half,  half, 0.0],  # top-right
            [ half, -half, 0.0],  # bottom-right
            [-half, -half, 0.0],  # bottom-left
        ],
        dtype=np.float32,
    )


def estimate_marker_pose(
    corners: np.ndarray,
    marker_length: float,
    camera_matrix: np.ndarray,
    dist_coeffs: np.ndarray,
):
    """
    Estimate pose for a single detected marker using solvePnP.
    corners: shape typically (1, 4, 2) from ArUco detector
    Returns:
        success, rvec, tvec
    """
    obj_points = marker_object_points(marker_length)

    # ArUco returns corners with shape (1, 4, 2) for one marker
    img_points = np.asarray(corners, dtype=np.float32).reshape(4, 2)

    success, rvec, tvec = cv.solvePnP(
        obj_points,
        img_points,
        camera_matrix,
        dist_coeffs,
        flags=cv.SOLVEPNP_IPPE_SQUARE,  # good choice for planar square markers
    )
    return success, rvec, tvec


def main():
    cap = cv.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")

    camera_matrix = np.load("mtx.npy")
    dist_coeffs = np.load("dist.npy")

    aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_100)
    aruco_params = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(aruco_dict, aruco_params)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        corners_list, ids, rejected = detector.detectMarkers(img)

        tvecs = []
        centers = []

        if ids is not None and len(corners_list) > 0:
            # Draw marker borders and ids
            cv.aruco.drawDetectedMarkers(img, corners_list, ids)

            for corners, marker_id in zip(corners_list, ids.flatten()):
                success, rvec, tvec = estimate_marker_pose(
                    corners,
                    MARKER_LENGTH_M,
                    camera_matrix,
                    dist_coeffs,
                )

                if not success:
                    continue

                tvecs.append(tvec.reshape(3))
                center = np.mean(corners.reshape(4, 2), axis=0).astype(np.int32)
                centers.append(tuple(center))

                # Draw pose axes
                cv.drawFrameAxes(
                    img,
                    camera_matrix,
                    dist_coeffs,
                    rvec,
                    tvec,
                    MARKER_LENGTH_M * 0.5,
                    2,
                )

                cx, cy = center
                cv.putText(
                    img,
                    f"id={marker_id}",
                    (cx + 10, cy - 10),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                    cv.LINE_AA,
                )

            if len(tvecs) == 2 and len(centers) == 2:
                p1 = tvecs[0]
                p2 = tvecs[1]
                dist_m = np.linalg.norm(p1 - p2)

                (x1, y1), (x2, y2) = centers
                xm, ym = (x1 + x2) // 2, (y1 + y2) // 2

                cv.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv.putText(
                    img,
                    f"{dist_m:.3f} m",
                    (xm, ym),
                    cv.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    2,
                    cv.LINE_AA,
                )

        cv.imshow(WINDOW_NAME, img)
        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()