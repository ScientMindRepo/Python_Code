from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv



class CameraStream:


    def __init__(self):

        # initialize the camera and g
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
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
        #  loops infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set to stop the thread is closed
            key = cv.waitKey(1) & 0xFF

            if self.stopped == True:
                self.camera.close()
                return

            # otherwise, read the next frame from the stream
            # capture frames from the camera
            with self.camera as camera:
                camera.start_preview()
                time.sleep(2)

                with self.rawCapture as stream:
                    camera.capture(stream, format='bgr')
                    # At this point the image is available as stream.array
                    image = stream.array

                    # if the `q` key was pressed, break from the loop
                    if key == ord("q"):
                        break
        #  loops infinitely until the thread is stopped

    def read(self):
        # returns the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
