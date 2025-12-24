import uvicorn
import os
from fastapi import Depends, FastAPI, HTTPException, status, Response, Cookie, Request
from fastapi.security import HTTPBasic
from fastapi.responses import StreamingResponse, FileResponse
from starlette.staticfiles import StaticFiles
from datetime import datetime
from dotenv import load_dotenv
import time
from pathlib import Path
from typing import Iterable
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from dotenv import load_dotenv
import logging
#rom urllib.parse import quote_plus
from contextlib import asynccontextmanager
import sys
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_utils.tasks import repeat_every

from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from tinydb import TinyDB, Query

import io
from routes import timer, sensors, login, cam_mount
import RPi.GPIO as GPIO



####RPi Hardware imports
import displayfn as display


from picamzero import Camera


import secrets
import base64


############################################Startup and lifespan run###############################


origins = [
    "*"
]


connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}



#security = HTTPBasic()


#@app.get("/frontend")
#async def serve_react_app(credentials: HTTPBasicCredentials = Depends(security)):
#    verify_credentials(credentials)
#    response = FileResponse("frontend/dist/index.html")
#    response.set_cookie('basic_auth', f"Basic {encode_credentials(credentials.username, credentials.password)}", expires=None)
#    return response



 
@asynccontextmanager
async def lifespan(app: FastAPI):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    #halleffect sensor 1
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    #HES2
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    
    #relay for light
    GPIO.setup(26,GPIO.OUT)
    
    #setup camera
    global cam
    cam = Camera()

    global disp
    disp = display.Display()
    disp.draw_rectangle([0,20,20,40])
    disp.refresh_image()
    time.sleep(3)

    global db
    db = TinyDB('db/db.json')
    load_dotenv()
    time_dict = timer.get_times()
    if time_dict == []:
        print("setting default start end times")
        timer.reset_db_timer()
    #Begin cycling fn
    
    global mount
    mount=cam_mount.mount(13,12)
    
    
    
    await screen_refresh_fn()
    yield
    disp.refresh_image()
    mount.stop_all()
    print("bye bye")
    disp.clear_screen()




#############################################Start FastAPI App##############################
app = FastAPI(lifespan=lifespan)
 
# mount static files first
#app.mount("/assets", StaticFiles(directory="UI/dist/assets"), name="assets")
#app.mount("/static", StaticFiles(directory="UI/dist"), name="static")
 
#security = HTTPBasic()

# API routes should be defined BEFORE the catch-all routes
app.include_router(timer.router)
app.include_router(sensors.router)
app.include_router(login.router)

'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)'''
# serve the frontend at root

#Serve frontend
#@app.get("/")
#async def serve_react_app():
#    return FileResponse("UI/dist/index.html")


# only handle specific static files that aren't in /assets
"""@app.get("/{filename:path}")
async def serve_static_or_spa(filename: str):
    # Don't intercept API routes
    if filename.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    # Don't intercept assets (they're handled by mount)
    if filename.startswith("assets/"):
        raise HTTPException(status_code=404, detail="Asset not found")

    # Check if it's a static file in the root dist directory
    file_path = f"UI/dist/{filename}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    # For everything else (SPA routes), serve React app
    return FileResponse("UI/dist/index.html")"""
    
###########################################################    

    
    
'''
def verify_credentials(
    credentials: HTTPBasicCredentials,
):
    
    creds = ("admin", "jamesp123")
    
    c_un, c_pass = creds
    
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_string = c_un
    correct_username_bytes = correct_username_string.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_string = c_pass
    correct_password_bytes = correct_password_string.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def encode_credentials(username: str, password: str) -> str:
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode("utf-8")
    return encoded_credentials
'''
    

#@repeat_every(seconds=5)
async def cycle_time_check():
    time_dict = timer.get_times()[0]
    time_status = timer.check_currenttime(time_dict)
    print(time_dict)
    print(time_status)
    if time_status:
        GPIO.output(26, GPIO.HIGH)
    else:
        GPIO.output(26, GPIO.LOW)
    
    return time_dict
    

#@repeat_every(seconds=5)
@app.get("/api/hallsensors", tags=["sensors"])
async def hall_sensors(sensormap=[(6, "HE1"), (17, "HE2")]):
    #Callback for hall effect sensor
    timestamp = time.time()
    """
    print(f"input showing as {GPIO.input(channel)}")   
    if GPIO.input(channel):
        #No magnet detected)
        print(f"Sensor showing HIGH (no magnet) {timestamp}")
    else:
        #magnet present
            print(f"sensor showing LOW (Magnet detected) {timestamp}")
    """
    res = {}
    for channel, sensor in sensormap:
        res[sensor] = GPIO.input(channel)
    
    print(f"sensor readout: {res}")
    return res
        


@app.get("/api/take_pic", tags=["camera"])
async def take_pic( request:Request, name="test.jpg"):
    login.verify_credentials(request)

    cam.take_photo("pictures/"+name)

    return FileResponse("pictures/"+name)
 
##################################NEW PANTILT ENDPOINTS#################

@app.post("/api/pan_right", tags=["camera"])
async def pan_right():
    
    r = mount.pan_increment(dir=-1)
    time.sleep(.5)
    return r

@app.post("/api/pan_left", tags=["camera"])
async def pan_left():
    
    r = mount.pan_increment(dir=1)
    time.sleep(.5)
    return r
    

@app.post("/api/tilt_up", tags=["camera"])
async def tilt_up():
    
    r = mount.tilt_increment(dir=-1)
    time.sleep(.5)
    return r

@app.post("/api/tilt_down", tags=["camera"])
async def tilt_down():
    
    r = mount.tilt_increment(dir=1)
    time.sleep(.5)
    return r


#####################ORCHESTRATION LOOP##############################

     
@repeat_every(seconds=5)
async def screen_refresh_fn():
    
    
    time_dict = await cycle_time_check()
    sensors = await hall_sensors()
    
    line1 = "Plant Bucket V2"
    line2 = str(datetime.now())[:19]
    line3 = "Light:"+str(time_dict['start_time'])+str(time_dict['end_time'])
    line4 = "Sensor:"+str(sensors)
    
    disp.image=disp.get_blank_image()
    disp.show_text((1,1),line1)
    disp.show_text((1,15),line2)
    disp.show_text((1,30),line3)
    disp.show_text((1,45),line4)

    disp.refresh_image()
    
    pass# TODO rewrite as a single orchestration loop function to repeatthat way you can persist values between the fumctions
    







    """if __name__ == "__main__":

    uvicorn.run("app:app", host="0.0.0.0",port=3000)

"""


def main():
    print("No main function")
    pass

 
if __name__ == '__main__':
    main()

 

 

 

 

 
