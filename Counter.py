import cv2
import os
import glob
import imutils
import imagehash
from PIL import Image 
from random import randint
import csv
from datetime import datetime

countArray = []

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
 
def addToDay():
    global countArray
    
    with open('data/counter/counter.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(countArray)
        
def newDay():
    global countArray
    
    countArray = []

def main():
    peopleEntered = 0
    peopleLeft = 0   

    HOG = cv2.HOGDescriptor()
    HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    cur_direc = os.getcwd()
    path = os.path.join(cur_direc, 'videos/')

    list_of_files = [f for f in glob.glob(path+'*.avi')]
    number_of_files = len(list_of_files)
    video_index = 0


    while number_of_files > 0:
        capture = cv2.VideoCapture(list_of_files[video_index])
        directories = list_of_files[video_index].split('/')
        video_name = directories[len(directories) - 1]
        previous_ROIs = {}
        index = 1
        peopleDetected = []
        peopleEntered = 0
        peopleLeft = 0
        
        while capture.isOpened():
            
            frameReturned, frame = capture.read()
            
            if frameReturned:
                
                frame_height, frame_width, _ = frame.shape
                frame_resized = cv2.resize(frame, (int(frame_width / 4), int(frame_height / 4)))
                
                (regions, _) = HOG.detectMultiScale(frame_resized, winStride=(2,2), padding=(8,8), scale=1.04)
                ROIs = []
                for (x, y, w, h) in regions:
                    x = x * 4
                    y = y * 4
                    w = w * 4
                    h = h * 4
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
                    centroid = (int(x + (w/2)), int(y + (h/2)))
                    ROI = (frame[y:y+h, x:x+w], centroid)
                    ROIs.append(ROI)
                
                if len(peopleDetected) > 0:
                    for person in peopleDetected:
                        for ROI in ROIs:
                            hash0 = imagehash.average_hash(Image.fromarray(ROI[0]))
                            hash1 = imagehash.average_hash(Image.fromarray(person.ROI))
                            cutoff = 50
                            
                            if hash0 - hash1 < cutoff:
                                person.setROI(ROI[0])
                                person.setCentroid(ROI[1])
                            else:
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
                
                for person in peopleDetected:
                    #cv2.putText(frame, person.id, person.centroid, font, 1.0, (0,255,0), 1)
                    cv2.circle(frame, person.centroid, 5, person.color, 2)
                cv2.line(frame, (30, 0), (30, frame_height), (0,255,0), 1)
                cv2.line(frame, (frame_width - 30, 0), (frame_width - 30, frame_height), (0,0,255), 1)
                cv2.line(frame, (int(frame_width / 2), 0), (int(frame_width / 2), frame_height), (0,0,0), 3)
                cv2.putText(frame, 'People Entered: {}'.format(peopleEntered), (50, 50), font, 2, (0,225,0), 1)
                cv2.putText(frame, 'People Left: {}'.format(peopleLeft), (frame_width - 290, 50), font, 2, (0,0,255), 1)
            
                cv2.imshow("Frame", frame)
            
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    number_of_files = number_of_files - 1 
                    video_index = video_index + 1
                    time = video_name.split(':')
                    hour = time[0]
                    countArray.append('{}:{}'.format(hour, peopleEntered))
                    countArray.append('{}:{}'.format(hour, peopleLeft * -1))
                    break
                    
                
            else:
                number_of_files = number_of_files - 1
                video_index = video_index + 1
                time = video_name.split(':')
                hour = time[0]
                countArray.append('{}:{}'.format(hour, peopleEntered))
                countArray.append('{}:{}'.format(hour, peopleLeft * -1))
                break
                
if __name__ == '__main__':
    main()
    #addToTotal(5)
    addToDay()
        