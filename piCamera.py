import cv2
import imutils
import time
import multiprocessing
import threading
from multiprocessing.pool import ThreadPool

timeout = False
cap = cv2.VideoCapture(0)

def detectPerson():
    global timeout
    global cap
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    face_cascade = cv2.CascadeClassifier('Cascades/Face_Cascades/haarcascade_frontalface_alt2.xml')



    while cap.isOpened():

        ret, frame = cap.read()
        #frame = cv2.rotate(frame, cv2.ROTATE_180)

        if ret:

            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = imutils.resize(frame, width=min(300, frame.shape[1]))

            (regions, _) = hog.detectMultiScale(frame,
                                                winStride=(2, 2),
                                                padding=(12, 12),
                                                scale=1.04
                                                )

            for (x, y, w, h) in regions:

                cv2.rectangle(frame, (x, y),
                              (x + w, y + h),
                              (0, 0, 255), 2
                              )

            faces = face_cascade.detectMultiScale(
                grey, scaleFactor=2, minNeighbors=6)

            if len(faces) > 0:
                cv2.destroyAllWindows()
                cap.release()
                cap = None
                p2 = multiprocessing.Process(target=detectFace)
                #p1 = multiprocessing.Process(target=timeoutAfter)
                p2.start()

                #p1.start()

                while timeout != None:
                    continue

                cap = cv2.VideoCapture()




            cv2.imshow("Detection", frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


def detectFace():
    global timeout
    global cap
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        print(type(frame))
        if ret:
            #frame = imutils.resize(frame, width=min(300, frame.shape[1]))

            cv2.imshow("hello", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                cap = None
                timeout = None
                break

def timeoutAfter():
    global timeout
    seconds = 5
    while seconds > 0:
        if timeout == None:
            break
        time.sleep(1)
        seconds = seconds - 1
        print(2)
    timeout = True

def record():
    return 0




if __name__ == "__main__":
    # thread = threading.Thread(target=detectPerson(), args=(10,))
    # thread.start()
    detectPerson()
