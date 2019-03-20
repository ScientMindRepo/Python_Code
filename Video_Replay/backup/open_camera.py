try:
    import RPi.GPIO as GPIO
    import os
    import os.path
    import time
    from picamera import PiCamera
    import subprocess
    from subprocess import Popen
except RuntimeError:
    print("Error importing ")




movie_path = '/home/pi/video.h264'
mp4movie_path = '/home/pi/video.mp4'

#Variables
sensor1_pin = 12            # sensor 1 - Start Button
sensor2_pin = 16            # sensor 2 - Stop Button
sensor1_triggered = False           # sensor 1 state
sensor2_triggered = False           # sensor 2 state

#RPi Board Configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor1_pin, GPIO.IN, GPIO.PUD_UP)          # sets sensor1 pin state to high (1)
GPIO.setup(sensor2_pin, GPIO.IN, GPIO.PUD_UP)          # sets sensor2 pin state to high (1)


#RPi Camera Configuration
camera = PiCamera()
camera.rotation = 180           # rotates the display 180 deg
camera.resolution = (640, 480)
camera.framerate = 10


### 1.SCRIPT START


# 2. SENSOR ONE LISTENING FOR TRIGGERING
current_btn1_state = GPIO.wait_for_edge(sensor1_pin, GPIO.FALLING, bouncetime=200)         # listening for sensor 1 to be triggered
sensor1_triggered = bool(current_btn1_state)            #print(sensor1_triggered)

# CHECK IF sensor 1 (S1) is triggered and camera is not recording
if sensor1_triggered == True and camera.recording != True:

    camera.start_preview()          # start camera and previews on display
    time.sleep(0.1)             # camera sensor warm up


    # CHECK IF there is a previous file and is it readable
    if os.path.isfile(movie_path) and os.access(movie_path, os.R_OK):

        os.remove(movie_path)           # delete the file
        print(" FILE DELETED :", movie_path)

        camera.start_recording('/home/pi/video.h264')
        print("RECORDING STARTED")

    else:
        camera.start_recording('/home/pi/video.h264')
        print("NEW VIDEO, START RECORDING")


#3. WHILE CAMERA IS RECORDING LOOP
while camera.recording == True:


    current_btn2_state = GPIO.input(sensor2_pin)            # get sensor 2 (S2) state

    if current_btn2_state == GPIO.LOW:          # if triggered pin 16 --> LOW

        camera.stop_recording()         # camera stops recording
        camera.stop_preview()           # camera stops preview broadcast
        videoname = "video.h264"
        camera.close()              # free up resources used by camera

        print("Video is saved at ; ", movie_path)
        print("saved movie size: ", os.stat(movie_path).st_atime)

        print("convertion success : ", os.path.isfile(mp4movie_path))


        # Sensors reset to listening for trigger
        sensor1_triggered == False
        sensor2_triggered == False

        #END WHILE CAMERA IS RECORDING LOOP
        break


    time.sleep(0.001)            # has to be checking faster than we can consecutively push the button



# TIME DELAY BEFORE REPLAY
REPLAY_DELAY_TIME = 5          # seconds
print("REPLAY DELAY STARTED", ", SET AT ", REPLAY_DELAY_TIME)
time.sleep(REPLAY_DELAY_TIME)

# Open Movie at '/home/pi/video.h264'
try :
    omxp = Popen(['omxplayer', movie_path])

    time.sleep(15)          # THIS TIME SHOULD BE THE LENGTH OF THE VIDEO
except FileNotFoundError:
    print(' File is not found @ ', movie_path)


GPIO.cleanup()          # good practice when donefree up any resources used by GPIO channels
#omxp.terminate()
print("END OF PROGRAM, Opening file \r")




#exit()

