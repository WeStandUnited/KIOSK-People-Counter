import cv2
import csv
import numpy as np
import face_recognition
import os
import glob
import datetime
import random


def greeting():
    currentTime = datetime.datetime.now()

    if currentTime.hour < 12:
        return 'Good Morning, '
    elif 12 <= currentTime.hour < 18:
        return 'Good Afternoon, '
    else:
        return 'Good Evening, '


def generate_new_pin():
    """
    Generate a new pin by finding a random number between 10000->99999
    While checking pin.csv to make sure it hasn't already been used
    """
    new_pin = random.randint(10000, 99999)
    file = os.path.join(os.getcwd(), 'data/pins/pins.csv')
    with open(file, 'r') as r_file:
        reader = csv.reader(r_file)
        for row in reader:
            for pin in row:
                if str(new_pin) == pin:
                    new_pin = generate_new_pin()
                break
    r_file.close()
    return new_pin


def write_pin_to_csv(new_pin):
    """
    Given a unique pin, add it to the csv
    """
    file = os.path.join(os.getcwd(), 'data/pins/pins.csv')
    with open(file, 'a', newline='') as w_file:
        writer = csv.writer(w_file)
        writer.writerow([new_pin])

    w_file.close()


def main():
    faces_encodings = []
    faces_names = []
    face_locations = []
    process_this_frame = True

    cur_direc = os.getcwd()
    path = os.path.join(cur_direc, 'data/faces/')
    list_of_files = [f for f in glob.glob(path+'*.jpg')]
    number_files = len(list_of_files)
    names = list_of_files.copy()

    # train program to associate names with images
    for i in range(number_files):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        faces_encodings.append(globals()['image_encoding_{}'.format(i)])

        # Create array of known names
        names[i] = names[i].replace(cur_direc, "")
        faces_names.append(names[i])

    # Get webcam
    video_capture = cv2.VideoCapture(0)

    # Initialize HOG Detector for body detection
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    while True:
        # Get the current frame from the webcam
        ret, frame = video_capture.read()

        # Resize the frame to 1/4 size for faster facial/body detection
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the frame from BGR to RGB for facial_recognition
        rgb_small_frame = small_frame[:, :, ::-1]

        # Process every other frame
        if process_this_frame:
            # Find all the faces and face encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # see if the face is a match for the known faces
                matches = face_recognition.compare_faces(faces_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = faces_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Detect people in the frame
        (rects, weights) = hog.detectMultiScale(small_frame, winStride=(8, 8),
                                                padding=(8, 8), scale=1.04)

        # Display the results for face detection
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (39, 85, 55), 2)

            # Input text label with a name and greeting below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (39, 85, 55), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            text = greeting() + os.path.splitext(os.path.basename(name))[0] + '!'

            cv2.putText(frame, text, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the results for body detection
        for (x, y, w, h) in rects:
            x *= 4
            y *= 4
            w *= 4
            h *= 4

            # draw rectangle around body
            cv2.rectangle(frame, (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

        # Display the resulting image
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # free up memory
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
