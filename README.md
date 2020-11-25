# Kiosk People Tracker & Counter 

## The State University of New York (SUNY) College at Oswego - CS 380 Fall 2020 Team D
### Team: Gregory Maldonado, William Bowling, Christian MarLett, Robert Netti & CJ Chiasson
### Stakeholder: Prof. Bastian Tenbergen

The goal of this project was to perform object detection and object tracking to count how many people enter and leave the Richard S. Shineman Center. This is done by detecting if a body is in the frame of the RASPI Camera, and then start recording. Once there are no more bodies detected, the Raspberry Pi sends the footage to the CS Department servers for processing. The server does the heavy lifting of accuracy tracking and counting each person captured in the frame. This data can now be analyzed used Python's MatPlotLib module.

<hr /> 
The system implements facial detection and recognition. If the user registers for facial recognition on our website <a href="http://pi.cs.oswego.edu:2770/">KIOSK-People-Counter</a> and upload a photo, the robot will greet you as you walk by !    






