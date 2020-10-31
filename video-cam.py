import cv2


from main import detector

cap = cv2.VideoCapture("Resources/one_person_walking_by.avi")


while True:
    ret, frame = cap.read()
    frame = detector(frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
