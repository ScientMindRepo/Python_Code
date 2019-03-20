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
        self.frame = None
        #grab a reference to the raw camera capture

        self.rawCapture = PiRGBArray(self.camera, size= self.camera.resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

        # allow the camera to warmup
        time.sleep(0.1)

        # initialize the variable used to indicate if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start a new thread and call the update
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # otherwise, read the next frame from the stream
        # capture frames from the camera
        while self.stream != None:
            for f in self.stream:
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                self.frame = f.array

                # clear the stream in preparation for the next frame
                self.rawCapture.truncate(0)

                # show the frame
                #cv.imshow("Frame", self.frame)
                key = cv.waitKey(1) & 0xFF


                # if the thread indicator variable is set to stop the thread is closed
                if self.stopped == True:
                    self.camera.close()
                    self.rawCapture.close()
                    self.camera.close()
                    return


                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break

    def read(self):
        # returns the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
