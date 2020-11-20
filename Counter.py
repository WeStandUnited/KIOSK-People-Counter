import cv2
import os
import glob
import imutils
import imagehash
from PIL import Image 
from random import randint
import csv
from datetime import datetime
import time

countArray = []
previous_number_of_files = 0
number_of_files = 0

'''
Person Class

...

Description:
---------------------------------------

+ Each unique person Identified gets their own instance of a person object
+ Each person object has 
    -> The initial position location first detected
    -> The position location last detected
    -> The last ROI found (image)
    -> Their own unique color for object tracking
'''
class Person:
    
    ROI = []
    centroid = (0, 0)
    def __init__(self, id, starting_centroid): 
        self.id = str(id) 
        self.starting_centroid = starting_centroid
    
    def setROI(self, ROI):
        self.ROI = ROI
    
    def setCentroid(self, centroid):
        self.centroid = centroid    
        
    def setColor(self, color: (int, int, int)):
        self.color = color
 
'''
AddToDay() Method

...

Description:
---------------------------------------

+ This method is called at the end of the day once all the counting has been finialized and will add the counts to the csv file
ready for graphing and emailing 
'''
def addToDay():
    global countArray
    
    with open('data/counter/counter.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(countArray)
        
'''
newDay() Method

...

Description:
---------------------------------------

+ This method sets the count array back to empty ready for a new day of counting
'''
def newDay():
    global countArray
    
    countArray = []

'''
Main Method

...

Description:
---------------------------------------

+ The main method is where the counting is done
+ The method cycles through each video found in the directory
+ The method detects the bodies in each frame. If there was no frame before, then the system initializes all points and bodies detected
+ The method checks the current frame with the past frame and checks to see if there are any similarities.
+ The similarities are where that person translated to
+ If two frames have similar ROI's then that class associated with that ROI will become the class for the new ROI and repeat
+ The count is added to a total 
'''
def main():
    global number_of_files
    global previous_number_of_files
    
    # Counters
    peopleEntered = 0
    peopleLeft = 0   

    # Body detection
    HOG = cv2.HOGDescriptor()
    HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    cur_direc = os.getcwd()
    path = os.path.join(cur_direc, 'Videos/')
    # Finds videos in the directory
    list_of_files = [f for f in glob.glob(path+'*.avi')]
    number_of_files = len(list_of_files)
    previous_number_of_files = number_of_files
    video_index = 0

    # Loops through each video
    while number_of_files > 0:
        capture = cv2.VideoCapture(list_of_files[video_index])
        directories = list_of_files[video_index].split('/')
        video_name = directories[len(directories) - 1]
        # Dictionary that contains each ROI and the class associated with that ROI
        previous_ROIs = {}
        index = 1
        peopleDetected = []
        peopleEntered = 0
        peopleLeft = 0
        
        # Runs while the capture is still running
        while capture.isOpened():
            
            frameReturned, frame = capture.read()
            # If the video didn't end
            if frameReturned:
                
                frame_height, frame_width, _ = frame.shape
                # Resizes for better performance
                frame_resized = cv2.resize(frame, (int(frame_width / 4), int(frame_height / 4)))
                
                # Body detection
                (regions, _) = HOG.detectMultiScale(frame_resized, winStride=(2,2), padding=(8,8), scale=1.04)
                # array for all ROIs detected
                ROIs = []
                # Loops through each body detected
                for (x, y, w, h) in regions:
                    # Scaling
                    x = x * 4
                    y = y * 4
                    w = w * 4
                    h = h * 4
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
                    # Finds centroid of the bounding box
                    centroid = (int(x + (w/2)), int(y + (h/2)))
                    # Image of the ROI
                    ROI = (frame[y:y+h, x:x+w], centroid)
                    # Add ROI to list
                    ROIs.append(ROI)
                
                # If there were people detected in the past 
                if len(peopleDetected) > 0:
                    # Loops through each person detected in the past
                    for person in peopleDetected:
                        # Loops through current people detected
                        for ROI in ROIs:
                            hash0 = imagehash.average_hash(Image.fromarray(ROI[0]))
                            hash1 = imagehash.average_hash(Image.fromarray(person.ROI))
                            cutoff = 50
                            # Compares each ROI to the past
                            if hash0 - hash1 < cutoff:
                                # If similiar then that ROI has a pervious class associated with it
                                person.setROI(ROI[0])
                                person.setCentroid(ROI[1])
                            # If not similar then make a new class to associate with that ROI
                            else:
                                person = Person(index, ROI[1])
                                person.setROI(ROI[0])
                                index = index + 1
                                person.setCentroid(ROI[1])
                                person.setColor((randint(0, 255), randint(0, 255), randint(0, 255)))
                                # Depending on where the person was first detected, that we can assume that the opposite side is where the person is going
                                if person.starting_centroid[0] <= frame_width / 2:
                                    peopleLeft = peopleLeft + 1
                                else:
                                    peopleEntered = peopleEntered + 1
                                peopleDetected.append(person)
                                   
                # If no person was detected in the past     
                else:
                    for ROI in ROIs:
                        person = Person(index, ROI[1])
                        person.setROI(ROI[0])
                        index = index + 1
                        person.setCentroid(ROI[1])
                        person.setColor((randint(0, 255), randint(0, 255), randint(0, 255)))
                        if person.starting_centroid[0] <= frame_width / 2:
                            peopleLeft = peopleLeft + 1
                        else:
                            peopleEntered = peopleEntered + 1
                        peopleDetected.append(person)
                
                font = cv2.FONT_HERSHEY_PLAIN
                index = 1
                
                # For each person detected place their tracking dot on their centroid
                for person in peopleDetected:
                    cv2.circle(frame, person.centroid, 5, person.color, 2)
                cv2.line(frame, (30, 0), (30, frame_height), (0,255,0), 1)
                cv2.line(frame, (frame_width - 30, 0), (frame_width - 30, frame_height), (0,0,255), 1)
                cv2.line(frame, (int(frame_width / 2), 0), (int(frame_width / 2), frame_height), (0,0,0), 3)
                cv2.putText(frame, 'People Entered: {}'.format(peopleEntered), (50, 50), font, 2, (0,225,0), 1)
                cv2.putText(frame, 'People Left: {}'.format(peopleLeft), (frame_width - 290, 50), font, 2, (0,0,255), 1)
            
                cv2.imshow("Frame", frame)
            
                # For debugging purposes
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # End the video and switch to the next video
                    number_of_files = number_of_files - 1 
                    video_index = video_index + 1
                    time = video_name.split(':')
                    hour = time[0]
                    # Add the count
                    print("People Entered: {}".format(peopleEntered))
                    print("People Left: {}".format(peopleLeft))
                    countArray.append('{}:{}'.format(hour, peopleEntered))
                    countArray.append('{}:{}'.format(hour, peopleLeft * -1))
                    capture.release()
                    cv2.destroyAllWindows()
                    break
                    
            # If the video ended, then move onto the next video    
            else:
                number_of_files = number_of_files - 1
                video_index = video_index + 1
                time = video_name.split(':')
                hour = time[0]
                print("People Entered: {}".format(peopleEntered))
                print("People Left: {}".format(peopleLeft))
                countArray.append('{}:{}'.format(hour, peopleEntered))
                countArray.append('{}:{}'.format(hour, peopleLeft * -1))
                capture.release()
                cv2.destroyAllWindows()
                break
            
        capture.release()
        cv2.destroyAllWindows()
    
                
if __name__ == '__main__':
    
    while True:
        print("checking")
        cur_direc = os.getcwd()
        path = os.path.join(cur_direc, 'Videos/')
        # Finds videos in the directory
        list_of_files = [f for f in glob.glob(path+'*.avi')]
        number_of_files = len(list_of_files)
        
        if number_of_files > previous_number_of_files: 
            main()
            
        currentTime = datetime.now()
        
        if currentTime.hour == 18: 
            addToDay()
            
        time.sleep(5)