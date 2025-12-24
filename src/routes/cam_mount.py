from urllib.parse import quote
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from tinydb import TinyDB, Query
import time
import RPi.GPIO as GPIO
from time import sleep

 
router = APIRouter()

class mount:
    def __init__(self, tilt_pin, pan_pin):
        
        GPIO.setmode(GPIO.BCM)
                        
        GPIO.setup(tilt_pin,GPIO.OUT)
        "set on pin at 50hz"
        pwm_tilt = GPIO.PWM(tilt_pin,50)
        "set start duty hahaha cycle"
        pwm_tilt.start(0)
        
        GPIO.setup(pan_pin,GPIO.OUT)
        "set on pin at 50hz"
        pwm_pan = GPIO.PWM(pan_pin,50)
        "set start duty hahaha cycle"
        pwm_pan.start(0)
        
        self.pins = {"pan": pan_pin, "tilt": tilt_pin}
        
        self.pwms = {"pan" : pwm_pan, "tilt": pwm_tilt}
        self.set_angle('pan',40)
        self.set_angle('tilt',40)
        self.angles = {"pan": 40, "tilt": 40}
        
        
    def stop_all(self):
        self.pwms["pan"].stop()
        self.pwms["tilt"].stop()
        
        
    def set_angle(self, axis, angle):
        pin = self.pins[axis]
        pwm = self.pwms[axis]
        """set angle of pwm servo"""
        duty= angle/18+2
        GPIO.output(pin, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(pin,False)
        pwm.ChangeDutyCycle(0)
    
    def tilt_increment(self, dir=1, mag = 10):
        cval = self.angles["tilt"]
        newval = cval + dir * mag
        
        if newval >= 0 and newval <= 90: 
            self.set_angle("tilt", newval)
            self.angles["tilt"] = newval
            
        return newval
    
    def pan_increment(self, dir=1, mag = 10):
        cval = self.angles["pan"]
        newval = cval + dir * mag
        if newval >= 0 and newval <= 90:
            self.set_angle("pan", newval)
            self.angles["pan"] = newval
        
        return newval
        
    





