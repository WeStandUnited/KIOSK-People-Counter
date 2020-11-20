import cv2
import imutils
import time
from enum import Enum
import glob
import face_recognition
import os
import numpy as np
import SCPInitSender 
from datetime import datetime

def greeting():
    currentTime = datetime.now()

    if currentTime.hour < 12:
        return 'Good Morning, '
    elif 12 <= currentTime.hour < 18:
        return 'Good Afternoon, '
    else:
        return 'Good Evening, '

# Possible states for the system
class State(Enum):
    BODY_PROCESS = 1
    FACE_PROCESS = 2

# Global Variables
capture = cv2.VideoCapture(0)
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH);
height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT);  

state = State.BODY_PROCESS

end = False
# Might differ on the raspi just to keep that in mind
FPS = 30

# Counter for the FPS 
elapsedFrames = FPS

# Body Detection Variables
HOG = cv2.HOGDescriptor()
HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Face Detection Variables
FACE_CASCADE = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_alt2.xml')

isRecording = False
# File type
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# Video output
output = None
#Video name
video_name = ''
#Timeout for video output
videoTimeout = FPS * 5


faces_encodings = []
faces_names = []
number_of_faces = 0


def updateFaces():
    
    global faces_encodings
    global faces_names
    global number_of_faces
    
    cur_direc = os.getcwd()
    path = os.path.join(cur_direc, 'Website/Photos/')
    print(path)
    list_of_files = [f for f in glob.glob(path+'*.jpg')]
    number_files = len(list_of_files)
    names = list_of_files.copy()
    print(number_files)
    
    # Checks if a face has been added to the file directory
    if number_files > number_of_faces:
        # train program to associate names with images
        for i in range(number_files):
            globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
            faces_encodings.append(globals()['image_encoding_{}'.format(i)])
            
            faces_names.append(names[i])

"""
A method for the Body Detection process

...

Description:
---------------------------------------

+ If the state of the script is State.BODY_PROCESS, then this method will be called. 
+ The method grabs each frame and uses SVM Dectector to detect a full human body in the frame.
    |
    ----> winStride, padding, and scale all effect the accuracy of the detection

+  If a body is detection, the method will iterate over each object with this respective (x, y, w, h)
    and draws a rectangle around the Region of Interest (ROI)
+  To force quit the script, the admin can hit 'q' to break the loop

"""
def bodyDetection():
    global capture
    global end
    global videoTimeout
    global isRecording
    global output
    global video_name
    
    # Each frame from the video capture
    frameReturned, frame = capture.read()
    frame = cv2.flip(frame, 0)
    if frameReturned:
        if isRecording and videoTimeout > 0: 
            
            output.write(frame)
        if videoTimeout == 0:
            output.release()
            '''
            Sending to server
             
            WIP
            '''
            SCPInitSender.sendFile('Videos/{}.avi'.format(video_name), 'cchiass2', 'pi.cs.oswego.edu', '/home/cchiass2/KIOSK-People-Counter/Videos/')
            os.system('cd Videos/; rm {}.avi; cd ..'.format(video_name))
            isRecording = False
        # Converts the frame to grey
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #
        # Resizes frame
        frame = imutils.resize(frame, width=min(300, frame.shape[1]))
        # Body Detection
        (regions, _) = HOG.detectMultiScale(frame, winStride=(8,8), padding=(8,8), scale=1.04)
        # Iterates over each body object
        if len(regions) > 0:
            if isRecording == False:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                video_name = current_time
                output = cv2.VideoWriter('Videos/{}.avi'.format(current_time), fourcc, 20.0, (int(width), int(height)))
                isRecording = True
            #else:
                #videoutTime = FPS * 5
        if len(regions) == 0 and isRecording:
            videoTimeout = videoTimeout - 1
        for (x, y, w, h) in regions:
            # Draws rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
        # Shows frame   
        cv2.imshow("BODY DETECTION", frame)
        # Admin exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            end = True
            if output != None:
                output.release()
            '''
            Sending to server
             
            WIP
            '''
            SCPInitSender.sendFile('Videos/{}.avi'.format(video_name), 'cchiass2', 'pi.cs.oswego.edu', '/home/cchiass2/KIOSK-People-Counter/Videos/')
            os.system('cd Videos/; rm {}.avi; cd ..'.format(video_name))
            
"""
A method for the Face Detection process

...

Description:
---------------------------------------

+ If the state of the script is State.FACE_PROCESS, then this method will be called
+ The method grabs each frame and tries to match the face(s) in the frame to a photo in the data/faces dir
+ If there is no face in the frame for the amount of time in timeoutFrames then the face detection will close and go back to body detection
+ When a face is detected, their name is placed at the bottom of their bounding box (FOR NOW)
"""
def faceDetection():
    global capture
    global state
    global faces_encodings
    global faces_names
    
    # Checks if the method timeout'ed
    timeout = False 
    # Amount of time before timing out
    timeoutFrames = FPS * 1 # 3 seconds
    face_locations = []
    process_this_frame = True
    
    frameReturned, frame = capture.read()
    frame = cv2.flip(frame, 0)
    # A frame must be returned and also checks if the method timeout'ed
    if frameReturned and timeout == False:
        small_frame = imutils.resize(frame, width=min(300, frame.shape[1]))
        # Convert image from BGR to RGB for facial_recognition
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_this_frame:
            # find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # Array to hold all the names associated with a face
            face_names = []
            for face_encoding in face_encodings:
                # see if the face is a match for the known faces
                matches = face_recognition.compare_faces(faces_encodings, face_encoding)
                # Default name
                name = "Unknown"

                # Face recoginition 
                face_distances = face_recognition.face_distance(faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = faces_names[best_match_index]

                # Adds the name to the list of all names
                face_names.append(name)
        
            # If there are no faces on the screen
            if len(face_names) == 0:
                # Start the timeout count down
                timeoutFrames = timeoutFrames - 1
            
            # If the timeout count down is 0 then the method has timed out 
            if timeoutFrames == 0:
                timeout = True

        # The current frame is done processing
        process_this_frame = not process_this_frame

        # Display the results - bounding boxes
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            print(top)

        # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (39, 85, 55), 2)

            # Input text label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (39, 85, 55), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX

            # Get name
            text = os.path.splitext(os.path.basename(name))[0] + '!'

            cv2.putText(frame, '{}{}'.format(greeting(), text), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
        # Display the resulting image
        cv2.imshow('FACE DETECTION', frame)
        
        # Admin -> if needs to break out press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            # Switches back to body processing
            state = State.BODY_PROCESS
    
    # If the method has timed out, then it switches back to body processing        
    else:
        cv2.destroyAllWindows()
        state = State.BODY_PROCESS

"""
Main Method

...

Description:
---------------------------------------

+ Main Method For Robot Standby Script
+ While the video capture is open, this script will run forever unless an admin presses the q key
+ This system works on a states
    - If the system detects that there is a body in the frame, then the system will switch into a BODY_PROCESS state
    - If the ststtem detects that there is a face in the frame, then the system will switch into a FACE_PROCESS state
+ When a state is called, their respective method is then called
+ The face detection state runs on a timeout system, if the system does not detect a frame in the frame, then a count down for a timeout will begin 
   After a certain amount of time of a face not being detected, the system will switch back to tracking body
   
NOTE: 
    + The system does not track bodies and records while there are faces on the screen
    + This was omitted by the stakeholder
"""     
def main(): 
    
    #Global Variables
    global state
    global FPS
    global elapsedFrames
    global capture
    global FACE_CASCADE
    global isRecording
    
    #Variables for timeouts
    face_detection_timeout = FPS * 10
    UPDATE_FACES_FRAMES = FPS * 180
    update_faces_counter = UPDATE_FACES_FRAMES
    elapsedFrames = FPS
    
    while capture.isOpened():
        
        # Checks to see if after a certain amount of time, if the system should try to refresh the faces from the directory
        if update_faces_counter == 0:
            updateFaces()
            update_faces_counter = UPDATE_FACES_FRAMES 
        else:
            update_faces_counter = update_faces_counter - 1
        
        #If state is body processing
        if state == State.BODY_PROCESS:
            bodyDetection()
            
            elapsedFrames = elapsedFrames - 1

            # Every second, it checks to see if there is a face in the frame
            if elapsedFrames == 0:
                frameReturned, frame = capture.read()
                frame = cv2.flip(frame, 0)
                # Tries to detect a face
                frame = imutils.resize(frame, width=min(300, frame.shape[1]))
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = FACE_CASCADE.detectMultiScale(grey, scaleFactor=1.50, minNeighbors=5)
                # If any face detected then change state
                if len(faces) > 0:
                    if isRecording:
                        isRecording = False
                        output.release()
                        '''
                        Sending to server
             
                        WIP
                        '''
                        #scpInitServer.sendVideo('output', 'cchiass2', 'pi.cs.oswego.edu', os.getcwd())
                            
                    state = State.FACE_PROCESS
                # Set the frame counter back to initial state
                elapsedFrames = FPS
        # If state is face processing       
        elif state == State.FACE_PROCESS:
            # Checks to see if there are no timeouts
            if face_detection_timeout > 0:
                faceDetection()
                face_detection_timeout = face_detection_timeout - 1
            # If timeout then switch state and destroy window
            else:
                face_detection_timeout = FPS * 10
                state = State.BODY_PROCESS
                cv2.destroyAllWindows()
           
        if end == True:
            break
    
    capture.release()
    cv2.destroyAllWindows()
        
if __name__ == '__main__':
    state = State.BODY_PROCESS
    updateFaces()
    main()