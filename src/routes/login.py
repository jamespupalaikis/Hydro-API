from urllib.parse import quote
from fastapi import APIRouter, Depends, Request, status, Response, Cookie, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tinydb import TinyDB, Query
import time


 
router = APIRouter()




@router.post("/login", tags=["login"])
def set_login_cookie(username, password, response:Response):

    response.set_cookie(key="creds", value=f"buffer{username}:::{password}")
    
    return "ok"
    pass

#@router.get("/get-creds", tags=["login"])
def get_credentials(request: Request):
    
    return request.cookies.get("creds")
        
def verify_credentials(request:Request):
    
    Tcreds = ("admin", "jamesp123")
    c1,c2=Tcreds
    creds_GT=f"buffer{c1}:::{c2}"
    
    given =request.cookies.get("creds")
    print(given,"--  --  --", creds_GT)
    if not (given == creds_GT):
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        return False
    return True
    