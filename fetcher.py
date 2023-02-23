"""
Weldegelijk fetching van detecties 
"""

from requests import get as _get, post
from config import TELRAAM_URL
import json

_cached_detections = []

#TODO: mss Exception handling bij mislukte requests (in functie get_json dan).

#def get_json(url:str):
    return _get(f"{TELRAAM_URL}/{url}").json()

def get_detections(): 
    #use next id,starting from last id + 1
    #or use id 0 when no detections are cached (yet)
    rid = _cached_detections[-1]['id']+1 if _cached_detections else 0 

    #Assumption: get_detections_since returns sorted list (sorted using 'id')
    new_detections = get_detections_since(rid)
    _cached_detections.extend(new_detections)

def get_detections_since(first_detection_id:int,limit=1000:int):
    """GETs first n (= limit, default is 1000) detections since first_detection_id"""
    response = requests.get(f"{TELRAAM_URL}detection/since/{first_detection_id}?limit={limit}")
    return response.json()
