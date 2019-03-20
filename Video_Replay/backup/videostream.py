from threading import Thread



import cv2 as cv

class VideoStream:
    def __init__(self, src = 0):

        # initialize the video camera stream and reads the first frame from the stream
        self.stream = cv.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()             #self.stream.read() return (boolean,frame), the bool is if the frame was successfully polled

        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # returns the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True