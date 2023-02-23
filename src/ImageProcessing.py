"""
Author: Vahid K.
"""

import cv2
import os
import numpy as np


class ImageProcessing:
    def __init__(self, imageAddress) -> None:
        self.image = cv2.imread(imageAddress)

    def __resizedImage(self, img):
        return cv2.resize(img, (0, 0), fx=0.50, fy=0.50)

    def showImage(self, img):
        # cv2.imshow('Image', self.image)
        cv2.imshow('ImageContour', self.__resizedImage(img))
        cv2.waitKey(0)

    def saveImage(self, img, fileName, directory):
        os.chdir(directory)
        cv2.imwrite(fileName, img)

    def getContours(self):
        # contours, hierarchy = cv2.findContours(
        #     self.__prepareImgUsingCanny(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
       # ret, thresh = cv2.threshold(self.__prepareImgUsingCanny(), 127, 255, 0)
        contours, hier = cv2.findContours(
            self.__prepareImgUsingCanny(), cv2.RETR_EXTERNAL, 2)

        # contours, hierarchy = cv2.findContours(self.__prepareImgUsingCanny(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        unified = self.mergeContours(contours)
        imgContour = self.image.copy()
        cv2.drawContours(imgContour, unified, -1, (0, 255, 0), 2)
        # cv2.drawContours(thresh, unified, -1, 255, -1)

        for i, cnt in enumerate(unified):
            # area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.1*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(imgContour, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(imgContour, "P"+str(i), (x+(w//2)+15, y+(h//2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

        return imgContour

    def mergeContours(self, contours):
        def find_if_close(cnt1, cnt2):
            row1, row2 = cnt1.shape[0], cnt2.shape[0]
            for i in range(row1):
                for j in range(row2):
                    dist = np.linalg.norm(cnt1[i]-cnt2[j])
                    if abs(dist) < 50:
                        return True
                    elif i == row1-1 and j == row2-1:
                        return False

        LENGTH = len(contours)
        status = np.zeros((LENGTH, 1))

        for i, cnt1 in enumerate(contours):
            x = i
            if i != LENGTH-1:
                for j, cnt2 in enumerate(contours[i+1:]):
                    x = x+1
                    dist = find_if_close(cnt1, cnt2)
                    if dist == True:
                        val = min(status[i], status[x])
                        status[x] = status[i] = val
                    else:
                        if status[x] == status[i]:
                            status[x] = i+1

        unified = []
        maximum = int(status.max())+1
        for i in range(maximum):
            pos = np.where(status == i)[0]
            if pos.size != 0:
                cont = np.vstack(contours[i] for i in pos)
                hull = cv2.convexHull(cont)
                unified.append(hull)
        return unified

    def __prepareImgUsingCanny(self):
        imgray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # imblurred = cv2.GaussianBlur(imgray, (5, 5), 0)
        # bilateral = cv2.bilateralFilter(imgray, None, 10, 20, 5)
        # imgbilateral = cv2.bilateralFilter(imgray, None, 9, 75, 75)
        # nlm = cv2.fastNlMeansDenoising(imgray, None, 10, 13, 39)
        nlm = cv2.fastNlMeansDenoising(imgray, None, 30, 7, 21)
        imCanny = cv2.Canny(nlm, 85, 155)
        return imCanny


# NOTE: This file is also used in the "web/app.py". To test this code use "ImageProcessingTest.py"