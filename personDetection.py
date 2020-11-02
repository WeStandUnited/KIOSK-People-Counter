import cv2
import imutils

# Initializing the HOG person
# detector

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture("Resources/two_people_walking_sidebyside.mp4")

# cap = cv2.VideoCapture("Resources/two_people_walking.mp4")

# cap = cv2.VideoCapture("Resources/gesturing_and_walking.mp4")


# cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()

    # the smaller our image is, the faster it will be to process and detect people in it
    if ret:
        image = imutils.resize(image, width=min(300, image.shape[1]))

        # Detecting all the regions in the Image that has a pedestrians inside it
        # detect multiscale allows multiple pedestrians to be detected.
        (regions, _) = hog.detectMultiScale(image,
                                            # winstride effects the accuracy of the detector,
                                            # as well as the speed in which it runs
                                            # smaller the winstride the more computational power
                                            winStride=(8, 8),
                                            # adding padding around the images region of interest
                                            # could increase the accuracy
                                            padding=(8, 8),
                                            # a smaller scale will increase the number
                                            # of layers in the image pyramid.
                                            # this will increase the amount of time it takes
                                            # to process your image
                                            scale=1.04)

        # Drawing the regions(the rectangles) in the Image
        for (x, y, w, h) in regions:
            cv2.rectangle(image, (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

            # Showing the output Image
        cv2.imshow("Image", image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()