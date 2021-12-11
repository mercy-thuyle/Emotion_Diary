# ------- Start: B3AR config code -------
# import the necessary packages
import cv2
import os
from flask import g, Flask, current_app

camera = cv2.VideoCapture(0)

#make shots directory to save pics
try:
    os.mkdir('./snapshots')
except OSError as error:
    pass
print("[INFO] load detector")
detector = cv2.CascadeClassifier('apps/static/assets/xml/haarcascade/haarcascade_frontalface_alt_tree.xml')

def gen_frames():  # generate frame by frame from camera
   while True:
        # initialize the video stream and allow the camera sensor to warm up
        #extracting frames
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # print("[INFO] loading face detector...") # face detection
            # with current_app.app_context():
            #     print('1')
            # detector = g.get('face_detector', None)
            # if not detector:

            faces = detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             # Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
            
            # encode OpenCV raw frame to jpg and displaying it
            ret, jpeg = cv2.imencode('.jpg', frame) 
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ------- End: B3AR config code -------