from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv



class CameraStream:


    def __init__(self):

        # initialize the camera and g
        self.camera = PiCamera()
        self.camera.resolution = (720, 720)
        self.camera.framerate = 60
        self.camera.rotation = 180

        #grab a reference to the raw camera capture
        self.rawCapture = PiRGBArray(self.camera, size= self.camera.resolution)

        # allow the camera to warmup
        time.sleep(0.1)

        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = False

    def start(self):
        # start a new thread and call the update
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # otherwise, read the next frame from the stream
        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            # if the thread indicator variable is set to stop the thread is closed
            if self.stopped == True:
                self.camera.close()
                return
            # show the frame

            cv.imshow("Frame", image)
            key = cv.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

    def read(self):
        # returns the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
