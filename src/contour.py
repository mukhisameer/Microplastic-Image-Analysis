"""
Author: Sameer M.
"""

import numpy as np
import cv2

# NOTE: REPLACE with relevant path
filterPath = r"path\to\filter\image.jpeg"

img = cv2.imread(filterPath)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print("Number of contours = " + str(len(contours)))
print(contours[0])

cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)

cv2.imshow("imgray", imgray)
cv2.namedWindow('imgray', cv2.WINDOW_NORMAL)
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# img = cv2.imread(r"C:\Users\Sameer\Desktop\image analysis\sample.jpg", 0)
# cv2.imshow('sample', img)