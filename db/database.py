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
        self.books = OOBTree()
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
        return self.name + " " + self.lastname
    
    def get_posts(self):
        return self.posts
    
    def get_room_reserve(self):
        return self.room_reserve
    
    def get_books(self):
        return self.books

    

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
    
class Book(Persistent):

    def __init__(self, book_id, title, author, year, genre, isbn, url):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn = isbn
        self.url = url

    def get_book_id(self):
        return self.book_id
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author
    
    def get_year(self):
        return self.year
    
    def get_genre(self):
        return self.genre
    
    def get_isbn(self):
        return self.isbn
    
    def get_url(self):
        return self.url

    def __str__(self):
        return f"{self.title} by {self.author}, {self.year}"

        # You can add more methods as needed, like getters or setters.

class Room(Persistent):
    def __init__(self, room_id):
        self.room_id = room_id
        self.reservation = False
        
    def get_room_id(self):
        return self.room_id
    
    def is_reserved(self):
        return self.reservation

    
    
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
    
def create_account(root, username, email, password, year, name, lastname):
    root[username] = Accounts(username, email, password, year, name, lastname)
    commit()
    print("account created")
    
def read_account(root, username):
    return root[username].all_data()

def read_all_account(root):
    for key in root.keys():
        print(root[key].all_data())
        

def update_account(root, username, email, password, year):
    root[username].email = email
    root[username].password = password
    root[username].year = year
    commit()
    print("account updated")
    
def delete_account(root, username):
    del root[username]
    commit()
    print("account deleted")

    








    


    




