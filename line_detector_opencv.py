import cv2
import numpy as np


def detect_lines(image):
    im = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    im = im[:, :, 2]
    kernel = np.ones((7, 7), np.uint8)
    opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
    im = im - opening
    im = cv2.adaptiveThreshold(im, 200, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -1)

    kernel = np.ones((3, 1), np.uint8)
    opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((5, 2), np.uint8)
    vertical_part = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((1, 3), np.uint8)
    opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((2, 5), np.uint8)
    horiz_part = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)

    vert_lines = cv2.HoughLines(vertical_part, 1, np.pi / 180, 200)
    horiz_lines = cv2.HoughLines(horiz_part, 1, np.pi / 180, 200)

    try:
        lines = horiz_lines[0]
    except TypeError:
        try:
            lines = vert_lines[0]
        except TypeError:
            return []
    else:
        try:
            lines = np.concatenate((np.array(lines), vert_lines[0]), axis=0)
        except TypeError:
            lines = horiz_lines[0]
    res = []
    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        res.append([x1, y1, x2, y2])
    return np.array(res)
