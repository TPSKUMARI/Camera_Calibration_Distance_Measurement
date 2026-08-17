# Camera Calibration and Distance Measurement

This project is a simple Python tool for calibrating a camera and then measuring real-world distances from images.

## What it does

- Calibrates the camera using a known reference length on a ruler
- Saves the calibration result in a JSON file
- Uses that calibration to measure distances between two selected points in an image

## Project files

- `calibaration.py` - camera calibration script
- `test.py` - image distance measurement script
- `calibration.json` - saved calibration values such as `mm_per_pixel`

## How it works

1. Run the calibration script.
2. Place a ruler or known-length object in front of the camera.
3. Capture the frame and click/drag to mark a known distance.
4. The script calculates the conversion factor and saves it.
5. Use the measurement script to click two points in an image and get the real distance in millimeters.

## Requirements

- Python 3
- OpenCV (`cv2`)
- NumPy

## Example usage

```bash
python calibaration.py
python test.py
```

## Notes

- The calibration result is stored in `calibration.json`.
- Make sure the image path in the measurement script is correct before running it.
- This is a lightweight project intended for basic camera-based measuring tasks.


