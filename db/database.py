import uuid
from persistent import Persistent
from ZODB import FileStorage, DB
from persistent import Persistent
from transaction import commit
from BTrees.OOBTree import OOBTree  # Import OOBTree

class Student(Persistent):
    def __init__(self, username, email, password, year, firstname, lastname):
        self.email = email
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.year = year
        self.posts = OOBTree()
        self.subjects = OOBTree()
        self.room_reserve = OOBTree()

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_year(self):
        return self.year
    
    def get_fullname(self):
        return self.firstname + " " + self.lastname

    def all_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "year": self.year,
            "firstname": self.firstname,
            "lastname": self.lastname
        }
        return data
    
    #Return Object
    def get_subjects(self):
        return self.subjects
    
    def get_posts(self):
        return self.posts
    
    def get_room_reserve(self):
        return self.room_reserve
    
    

class Professor(Persistent):
    def __init__(self, username, email, password, firstname, lastname):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.subjects = OOBTree()
        self.posts = OOBTree()
        self.room_reserve = OOBTree()
        
    def get_username(self):
        return self.username
    
    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password
    
    def get_firstname(self):
        return self.firstname
    
    def get_lastname(self):
        return self.lastname

    
    def all_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
        }
        return data
    
    def get_subjects(self):
        return self.subjects
    
    def get_room_reserve(self):
        return self.room_reserve
    
    def get_posts(self):
        return self.posts

class Room(Persistent):
    def __init__(self, room_id, room_description="Lecture Room", room_capacity=30):
        self.room_id = room_id
        self.description = room_description
        self.capacity = room_capacity
        self.reservation = OOBTree() # {"room_id": {"7:00", Flase}}
        
    def get_room_id(self):
        return self.room_id
    
    def get_reservation(self):
        return self.reservation
    
    def all_data(self):
        data = {
            "room_id": self.room_id,
            "description": self.description,
            "capacity": self.capacity,
            "reservation": self.reservation
        }
        return data

def open_db_client():
    global db, connection
    storage = FileStorage.FileStorage('db/account.fs')
    db = DB(storage)
    connection = db.open()
    root = connection.root()
    print("database connected")
    return root

def shutdown_db_client():  
    db.close()
    connection.close()
    print("database disconnected")
    








    


    




