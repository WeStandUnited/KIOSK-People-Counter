import cv2
import pynput.keyboard as Keyboard

faceCascade = cv2.CascadeClassifier("harrcascade_defaultface.xml")
eye = cv2.CascadeClassifier("haarcascade_eye.xml")
cap = cv2.VideoCapture(0)


def Take_Picture(frame):

    cv2.imwrite('c1.png',frame)



while True:
    ret,img = cap.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,1.3,5)#change these at will

    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        roi_grey = gray[y:y+h,x:x+w]
        roi_color = img[y:y+h,x:x+w]


        eyes = eye.detectMultiScale(roi_grey)#change at will
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow("img",img)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        _,i = cap.read()
        cv2.imwrite('c1.png',i)#Face with no detection
        cv2.imwrite('c2.png',img)#with rectangles

        break

