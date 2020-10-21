# line_detector_opencv
Line detection module. OpenCV approaches and Hough transform.

Dependencies: numpy, opencv-python 3.4.11.

Use module:
```python
import cv2
from line_detector_opencv import detect_lines

im = cv2.imread('yourimage.jpg')
lines = detect_lines(im)
```
