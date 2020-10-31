import cv2
import imutils
from main import detector

img = cv2.imread('Resources/download.jpg')
img = imutils.resize(img, width=500)
img = detector(img)
cv2.waitKey(0)
cv2.destroyAllWindows()
