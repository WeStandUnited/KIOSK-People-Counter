import cv2
import numpy as np
import face_recognition
import os
import glob
import datetime


def greeting():
    currentTime = datetime.datetime.now()

    if currentTime.hour < 12:
        return 'Good Morning, '
    elif 12 <= currentTime.hour < 18:
        return 'Good Afternoon, '
    else:
        return 'Good Evening, '


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

    # get webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # get the current frame
        ret, frame = video_capture.read()

        # Resize the frame of video to 1/4 size for faster facial recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert image from BGR to RGB for facial_recognition
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # find all the faces and face encodings in the current frame of video
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

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (39, 85, 55), 2)

            # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (39, 85, 55), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            text = greeting() + os.path.splitext(os.path.basename(name))[0] + '!'

            cv2.putText(frame, text, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

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