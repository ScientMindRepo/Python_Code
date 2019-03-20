import datetime

class vs_stats:
    def __init__(self):
        # initialized the place holders for information provided by class
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # starts the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()
        return self

    def update(self):
        # increment the total number of frames examined during the start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return time interval between start and end
        return (self._end - self._start).total_seconds()

    def fps(self):
        # computes approximate frames per second
        return self._numFrames / self.elapsed()