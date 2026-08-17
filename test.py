import cv2
import numpy as np
import json
import os

def load_calibration(cal_file='calibration.json'):
    """
    Load calibration factor from file.
    """
    if not os.path.exists(cal_file):
        raise FileNotFoundError(f"Calibration file '{cal_file}' not found. Run calibration.py first!")
    with open(cal_file, 'r') as f:
        cal = json.load(f)
    print(f"Loaded calibration: {cal['mm_per_pixel']:.4f} mm/pixel")
    return cal['mm_per_pixel']

def measure_distance_in_image(image_path, cal_file='calibration.json'):
    """
    Load an image and measure distance between two clicked points using saved calibration.
    """
    mm_per_pixel = load_calibration(cal_file)
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not load image")
    
    drawing = False
    start_point = None
    end_point = None
    display_img = img.copy()
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing, start_point, end_point, display_img
        if event == cv2.EVENT_LBUTTONDOWN:
            if start_point is None:
                start_point = (x, y)
                drawing = True
                print("First point set. Click second point.")
            else:
                end_point = (x, y)
                drawing = False
                # Calculate and display distance
                pixel_dist = np.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)
                mm_dist = pixel_dist * mm_per_pixel
                print(f"Pixel distance: {pixel_dist:.2f} px")
                print(f"Real distance: {mm_dist:.2f} mm")
                # Draw line and points
                cv2.line(display_img, start_point, end_point, (0, 255, 0), 2)
                cv2.circle(display_img, start_point, 5, (0, 0, 255), -1)
                cv2.circle(display_img, end_point, 5, (0, 0, 255), -1)
                cv2.imshow('Measurement', display_img)
    
    cv2.namedWindow('Measurement')
    cv2.setMouseCallback('Measurement', mouse_callback)
    
    print("Click two points to measure distance. Press 'r' to reset, 'q' to quit.")
    while True:
        cv2.imshow('Measurement', display_img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            start_point = None
            end_point = None
            display_img = img.copy()
        elif key == ord('q'):
            break
    
    cv2.destroyAllWindows()

# Example usage: Replace with your image path
if __name__ == "__main__":
    measure_distance_in_image(r"C:\Users\samai\Pictures\Camera Roll\WIN_20251127_17_44_32_Pro.jpg")  # e.g., a photo with an object to measure