import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Set uip pin 18 for LED
#GPIO.setup(18, GPIO.OUT)

#Set up pin 26 for relay
GPIO.setup(26, GPIO.OUT)#, pull_up_down=GPIO.PUD_UP)

 



#Turn on LED
"""
GPIO.output(18, GPIO.HIGH)
time.sleep(3)
GPIO.output(18, GPIO.LOW)"""
def callbackFunction(channel):
    #Callback for hall effect sensor
    timestamp = time.time()
    print(f"input showing as {GPIO.input(channel)}")
    GPIO.output(18, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(18, GPIO.LOW)
    if GPIO.input(channel):
        #No magnet detected)
        print(f"Sensor showing HIGH (no magnet) {timestamp}")
    else:
        #magnet present
        print(f"sensor showing LOW (Magnet detected) {timestamp}")

def main():
    callbackFunction(17)
    try:
        while True:
            print(GPIO.input(17))
            time.sleep(3)
            
    except:
        GPIO.cleanup()
        
    

#GPIO.add_event_detect(17, GPIO.BOTH, callback=callbackFunction, bouncetime=200)

if __name__ == "__main__":
    #main()
    GPIO.output(26, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(26, GPIO.LOW)


