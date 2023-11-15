import uuid
from persistent import Persistent
from ZODB import FileStorage, DB
from persistent import Persistent
from transaction import commit
from BTrees.OOBTree import OOBTree  # Import OOBTree


class Accounts(Persistent):
    def __init__(self, username, email, password, year, name, lastname):
        self.email = email
        self.username = username
        self.password = password
        self.name = name
        self.lastname = lastname
        self.year = year
        self.posts = OOBTree()


    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_year(self):
        return self.year
    
    def get_fullname(self):
        return self.name + " " + self.lastname

    def all_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "year": self.year
        }
        return data
    
    def __str__(self):
        return f"username: {self.username}, email: {self.email}, password: {self.password}, year: {self.year}"


class Professor(Persistent):
    def __init__(self, username, email, password, firstname, lastname, subject):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.subject = subject
        self.posts = OOBTree()
        
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
    
    def get_subject(self):
        return self.subject
    
    def all_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "subject": self.subject
        }
        return data
    
    def __str__(self):
        return f"username: {self.username}, email: {self.email}, password: {self.password}, firstname: {self.firstname}, lastname: {self.lastname}, subject: {self.subject}"
    
# class Library(Persistent):
#     def __init__(self, name,id)
#         self.name = name

# class RoomReser(Persistent):

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
    








    


    




