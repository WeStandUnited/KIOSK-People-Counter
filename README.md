# Kiosk People Tracker & Counter 

## The State University of New York (SUNY) College at Oswego - CS 380 Fall 2020 Team D
### Team: Gregory Maldonado, William Bowling, Christian MarLett, Robert Netti & CJ Chiasson
### Stakeholder: Prof. Bastian Tenbergen

The goal of this project was to perform object detection and object tracking to count how many people enter and leave the Richard S. Shineman Center. This is done by detecting if a body is in the frame of the RASPI Camera, and then start recording. Once there are no more bodies detected, the Raspberry Pi sends the footage to the CS Department servers for processing. The server does the heavy lifting of accuracy tracking and counting each person captured in the frame. This data can now be analyzed used Python's MatPlotLib module.

<hr /> 
The system implements facial detection and recognition. If the user registers for facial recognition on our website <a href="http://pi.cs.oswego.edu:2770/">KIOSK-People-Counter</a> and upload a photo, the robot will greet you as you walk by !    


# Getting Started
<p>
Hardware Required: Raspberry Pi (Preferably Pi Gen 4) 
                   RPI Camera or USB Camera 
                   A offsite computer/ server for video computation
                   
Software Required: Python 3+
                   Raspbian ( or any debian based PI distro)
                   Offsite Computer running debian
                   
Python Dependencies: FlaskForm, werkzeug.utils , wtforms ,request, redirect, render_template , PIL , waitress , datetime , rand , os , imagehash , glob , cv2 ,paramiko ,scp ,imutils , time , enum , face_recognition , numpy , datetime. 

Please Note depending on OS you may need system package to config specific python libaries.
</p>

# Setup of Raspberry PI and Server
<p>
  Now that you have all hardware and Software Requirments.
  
  <b> Setting up Raspberry Pi </b>
  <il>
  
  Step 1) Place Pi in well lit area where you woud like it to count vistors.
  
  Step 2) Power Pi and Connect to network
  
  Step 3) Set up RSA key between Pi and the Server
  
  Step 4) Replace host in SCPInit functions to point at your host, along with the user name your have an RSA key set up with.
  </il>
  
  <b> Setting up Website </b>
  <il>
  
  Step 1) Replace values in main.py with your host and user name.
  
  Step 2) Choose a port to host the server off of
  
  </il>
</p>  
  
  
  

