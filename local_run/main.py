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
import logging
#rom urllib.parse import quote_plus
from contextlib import asynccontextmanager
import sys
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_utils.tasks import repeat_every

from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from tinydb import TinyDB, Query

import io
from routes import login






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



    global db
    print("Starting UP!")
    db = TinyDB('db/db.json')
    load_dotenv()

    

    
    
    
    #await screen_refresh_fn()
    yield
    print("bye bye")





#############################################Start FastAPI App##############################
app = FastAPI(lifespan=lifespan)
app.include_router(login.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("middleware origins added")

# API routes should be defined BEFORE the catch-all routes


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
    


 
##################################NEW PANTILT ENDPOINTS#################


#####################ORCHESTRATION LOOP##############################

     
@repeat_every(seconds=5)
async def screen_refresh_fn():
    
    print("runnin down a dream")
    pass# 





    """if __name__ == "__main__":

    uvicorn.run("app:app", host="0.0.0.0",port=3000)

"""


def main():
    print("No main function")
    pass

 
if __name__ == '__main__':
    main()

 

 

 

 

 
