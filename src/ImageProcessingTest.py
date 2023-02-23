import ImageProcessing as imgp

# NOTE: REPLACE with relevant path
filterPath = r"path\to\filter\image.jpeg"

imgProc = imgp.ImageProcessing(filterPath)
img = imgProc.getContours()
imgProc.showImage(img)
imgProc.saveImage(img, "ProcessedImg.jpg", "MicroplasticAnalysis/RawImages")