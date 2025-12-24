from urllib.parse import quote
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tinydb import TinyDB, Query
import time
import RPi.GPIO as GPIO


 
router = APIRouter()


class sensor_set():
    pass

@router.get("/api/get_sensors", tags=["sensors"])
def get_sensors():
    
    sensormap=[(6, "HE1"), (17, "HE2")]
    """db = TinyDB('db/db.json')
    User = Query()
    #db.insert({'name': 'John', 'age': 22})
    res = db.search(User.identity == 'times')"""
    res1 = GPIO.input(6)
    res2 = GPIO.input(17)
    res = {"H1":res1,"H2":res2}
    return res
 

 
 


