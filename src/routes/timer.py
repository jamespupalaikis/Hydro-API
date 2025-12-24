from urllib.parse import quote
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tinydb import TinyDB, Query
import time

from routes.login import verify_credentials


 
router = APIRouter()

@router.post("/api/reset_times", tags=["timer"])
def reset_db_timer(request:Request):
    verify_credentials(request)

    db = TinyDB('db/db.json')
    #User = Query()
    start_time = (8,30) # 8:00 AM
    end_time = (19,15) # 5:00 PM
    db.truncate()
    db.insert({"identity":"times",'start_time': start_time, 'end_time': end_time})
    #a = db.search(User.name == 'John')
    return f"times reset to default:  {start_time}, {end_time}"


@router.post("/api/set_times", tags=["timer"])
def set_db_timer(request:Request, start_hour, start_min, end_hour, end_min):
    verify_credentials(request)
    db = TinyDB('db/db.json')
    #User = Query()
    start_time = (start_hour,start_min) # 8:00 AM
    end_time = (end_hour,end_min) # 5:00 PM
    db.update({"identity":"times",'start_time': start_time, 'end_time': end_time})
    #a = db.search(User.name == 'John')
    return f"times set to {start_time}, {end_time}"
 

 
@router.get("/api/get_times", tags=["timer"])
def get_times():
    db = TinyDB('db/db.json')
    User = Query()
    #db.insert({'name': 'John', 'age': 22})
    res = db.search(User.identity == 'times')
    return res
 
 
 
def check_currenttime(time_dict):
    print(time_dict)
    starthr, startmin = time_dict['start_time']
    endhr, endmin = time_dict['end_time']
    starthr, startmin, endhr, endmin = int(starthr), int(startmin), int(endhr), int(endmin)
    ctime = time.localtime(time.time())
    #print(ctime)
    chour, cmin = ctime.tm_hour, ctime.tm_min
    if(chour >= starthr and chour <= endhr):
        if starthr == endhr:
            if chour != starthr:
                return False
            else:
                #all same
                return cmin >= startmin and cmin <= endmin
            
        if(chour == starthr):
            if cmin >= startmin:
                return True
            else:
                return False
        if chour == endhr:
            if cmin <= endmin:
                return True
            else:
                return False
        return True
    else:
        return False

 
 

   
""" 
@router.get("/api/export", tags=["export"])
async def export_zip(state: str, user_id: str):
    question_file = "Test Response"
 
    buffer = await template_export_report(state, user_id, question_file)
 
    quoted_name = quote(user_id, safe="")
 
    content_disposition = (
        f"attachment; "
        f'filename="{quoted_name}.zip"; '         # fallback; will be ASCII-only
        f"filename*=UTF-8''{quoted_name}.zip"     # RFC5987 encoding for unicode
    )
 
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": content_disposition
        }
    )
"""