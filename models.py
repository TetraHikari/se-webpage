from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from datetime import datetime

client = MongoClient('mongodb://localhost:27017')
db = client['se-blog']
collection = db['posts']

import socket
import struct
import sys
import time

def RequestTimefromNtp(addr='0.de.pool.ntp.org'):
    REF_TIME_1970 = 2208988800  # Reference time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (addr, 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    return time.ctime(t), t

class Post(BaseModel):
    title: str
    content: str
    created_at: str = RequestTimefromNtp()[0]
    
