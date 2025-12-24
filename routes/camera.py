from urllib.parse import quote
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from tinydb import TinyDB, Query
import time


 
router = APIRouter()

@router.post("/api/take_pic", tags=["camera"])
def take_pic(name="test.jpg"):
    
    return f"times reset to default:  {start_time}, {end_time}"
 

 
@router.get("/api/get_times", tags=["timer"])
def get_times():
    db = TinyDB('db/db.json')
    User = Query()
    #db.insert({'name': 'John', 'age': 22})
    res = db.search(User.identity == 'times')
    return res
 

