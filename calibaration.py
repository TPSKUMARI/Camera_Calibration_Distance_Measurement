import cv2
import numpy as np

def calibrate_camera_with_ruler(camera_index=0, reference_length_mm=1):
    """
    Calibrate camera by marking a 1 mm distance on a ruler in a captured image.
    reference_length_mm: length of the marked distance in millimeters (default 1 mm)
    """
    # Open camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")

    print("Camera calibration started...")
    print("Place a ruler in the camera's view.")
    print("Press 'c' to capture the image, then click and drag to mark a 1 mm distance.")
    print("Press 's' to save measurement, 'r' to reset, 'q' to quit.")

    # Variables for drawing
    captured = False
    drawing = False
    start_point = (-1, -1)
    end_point = (-1, -1)
    frame = None
    captured_frame = None
    display_frame = None

    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing, start_point, end_point, display_frame, captured_frame
        if captured:
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                start_point = (x, y)
                display_frame = captured_frame.copy()
            elif event == cv2.EVENT_MOUSEMOVE and drawing:
                display_frame = captured_frame.copy()
                end_point = (x, y)
                cv2.line(display_frame, start_point, end_point, (0, 255, 0), 2)
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                end_point = (x, y)
                cv2.line(display_frame, start_point, end_point, (0, 255, 0), 2)

    # Set up window and mouse callback
    cv2.namedWindow('Calibration')
    cv2.setMouseCallback('Calibration', mouse_callback)

    while True:
        if not captured:
            ret, frame = cap.read()
            if not ret:
                break
            display_frame = frame
        else:
            display_frame = display_frame if display_frame is not None else captured_frame

        # Display current frame
        cv2.imshow('Calibration', display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') and not captured:
            # Capture the frame
            captured_frame = frame.copy()
            captured = True
            print("Image captured. Now click and drag to mark a 1 mm distance on the ruler.")
        elif key == ord('s') and captured and start_point != (-1, -1) and end_point != (-1, -1):
            # Calculate pixel length
            pixel_length = np.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)
            if pixel_length > 0:
                pixels_per_mm = pixel_length / reference_length_mm
                print(f"Calibration result: {pixels_per_mm:.2f} pixels per mm")
                print(f"Conversion factor: {1/pixels_per_mm:.4f} mm per pixel")
                break
        elif key == ord('r') and captured:
            # Reset to capture a new frame
            captured = False
            start_point = (-1, -1)
            end_point = (-1, -1)
            display_frame = None
            print("Reset. Press 'c' to capture a new image.")
        elif key == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    return pixels_per_mm if 'pixels_per_mm' in locals() else None

if __name__ == "__main__":
    # Calibrate with a 1 mm reference distance
    pixels_per_mm = calibrate_camera_with_ruler(camera_index=1, reference_length_mm=1)
    if pixels_per_mm:
        print(f"Calibration complete. Use {1/pixels_per_mm:.4f} mm/pixel for measurements")
    else:
        print("Calibration failed or was cancelled")