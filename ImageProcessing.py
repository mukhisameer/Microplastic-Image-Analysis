import cv2
import os


class ImageProcessing:
    def __init__(self, imageAddress) -> None:
        self.image = cv2.imread(imageAddress)

    def __resizedImage(self, img):
        return cv2.resize(img, (0, 0), fx=0.40, fy=0.40)

    def showImage(self, img):
        cv2.imshow('Image', self.image)
        cv2.imshow('ImageContour', self.__resizedImage(img))
        cv2.waitKey(0)

    def saveImage(self, img, fileName, directory):
        os.chdir(directory)
        cv2.imwrite(fileName, img)

    def getContours(self):
        contours, hierarchy = cv2.findContours(
            self.__prepareImgUsingCanny(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgContour = self.image.copy()
        counter = 1
        for cnt in contours:
            # area = cv2.contourArea(cnt)
            cv2.drawContours(imgContour, cnt, -1, (0, 255, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.1*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(imgContour, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(imgContour, "P"+str(counter), (x+(w//2)+15, y+(h//2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
            counter += 1

        return imgContour

    def __prepareImgUsingCanny(self):
        imgray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # imblurred = cv2.GaussianBlur(imgray, (7, 7), 1)
        # bilateral = cv2.bilateralFilter(imgray, None, 10, 20, 5)
        nlm = cv2.fastNlMeansDenoising(imgray, None, 10, 13, 39)
        imCanny = cv2.Canny(nlm, 85, 255)
        return imCanny


imgProc = ImageProcessing(r"MicroplasticAnalysis/RawImages/IMG_9913.jpg")
img = imgProc.getContours()
imgProc.showImage(img)
imgProc.saveImage(img, "ProcessedImg.jpg", "MicroplasticAnalysis/RawImages")
