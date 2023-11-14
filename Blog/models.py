from pydantic import BaseModel
import time
import socket
import struct


class Blog(BaseModel):
    title: str
    content: str
    
