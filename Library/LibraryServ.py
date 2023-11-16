from ZODB import DB
from ZODB.FileStorage import FileStorage
import transaction
import persistent
from db.database import *


# class Accounts(Persistent):
#     def __init__(self, username, email, password, year, name, lastname):
#         self.email = email
#         self.username = username
#         self.password = password
#         self.name = name
#         self.lastname = lastname
#         self.year = year
#         self.posts = OOBTree()
#         self.books = OOBTree()
#         self.room_reserve = OOBTree()


#     def get_username(self):
#         return self.username

#     def get_email(self):
#         return self.email

#     def get_password(self):
#         return self.password

#     def get_year(self):
#         return self.year
    
#     def get_fullname(self):
#         return self.name + " " + self.lastname
    
#     def get_posts(self):
#         return self.posts
    
#     def get_room_reserve(self):
#         return self.room_reserve
    
#     def get_books(self):
#         return self.books

    

#     def all_data(self):
#         data = {
#             "username": self.username,
#             "email": self.email,
#             "password": self.password,
#             "year": self.year
#         }
#         return data

    
#     def __str__(self):
#         return f"username: {self.username}, email: {self.email}, password: {self.password}, year: {self.year}"
    
# class Book(Persistent):

#     def __init__(self, book_id, title, author, year, genre, isbn, url):
#         self.book_id = book_id
#         self.title = title
#         self.author = author
#         self.year = year
#         self.genre = genre
#         self.isbn = isbn
#         self.url = url

#     def get_book_id(self):
#         return self.book_id
    
#     def get_title(self):
#         return self.title
    
#     def get_author(self):
#         return self.author
    
#     def get_year(self):
#         return self.year
    
#     def get_genre(self):
#         return self.genre
    
#     def get_isbn(self):
#         return self.isbn
    
#     def get_url(self):
#         return self.url

#     def __str__(self):
#         return f"{self.title} by {self.author}, {self.year}"

#         # You can add more methods as needed, like getters or setters.

# class Room(Persistent):
#     def __init__(self, room_id):
#         self.room_id = room_id
#         self.reservation = False
        
#     def get_room_id(self):
#         return self.room_id
    
#     def is_reserved(self):
#         return self.reservation

    
    
# def open_db_client():
#     global db, connection
#     storage = FileStorage.FileStorage('db/account.fs')
#     db = DB(storage)
#     connection = db.open()
#     root = connection.root()
#     print("database connected")
#     return root

# def shutdown_db_client():  
#     db.close()
#     connection.close()
#     print("database disconnected")
    
# def create_account(root, username, email, password, year, name, lastname):
#     root[username] = Accounts(username, email, password, year, name, lastname)
#     commit()
#     print("account created")
    
# def read_account(root, username):
#     return root[username].all_data()

# def read_all_account(root):
#     for key in root.keys():
#         print(root[key].all_data())
        

# def update_account(root, username, email, password, year):
#     root[username].email = email
#     root[username].password = password
#     root[username].year = year
#     commit()
#     print("account updated")
    
# def delete_account(root, username):
#     del root[username]
#     commit()
#     print("account deleted")

    
def create_book(root, title, author, year, genre, isbn, url):
    book_id = str(uuid.uuid4())
    root[book_id] = Book(book_id, title, author, year, genre, isbn, url)
    commit()
    print("book created")

def get_total_book(root):
    return len(root.keys())

def get_all_book_id(root):
    book_id_list = []
    for key in root.keys():
        if isinstance(root[key], Book):
            book_id_list.append(root[key].get_book_id())
    return book_id_list

def get_book_detail(root, book_id):
    data={}
    data["book_id"] = root[book_id].get_book_id()
    data["title"] = root[book_id].title
    data["author"] = root[book_id].author
    data["year"] = root[book_id].year
    data["genre"] = root[book_id].genre
    data["isbn"] = root[book_id].isbn
    data["url"] = root[book_id].url
    return data

def delete_book(root, book_id):
    del root[book_id]
    commit()
    print("book deleted")

def update_book(root, book_id, title, author, year, genre, isbn, url):
    root[book_id].title = title
    root[book_id].author = author
    root[book_id].year = year
    root[book_id].genre = genre
    root[book_id].isbn = isbn
    root[book_id].url = url
    commit()
    print("book updated")

def book_detail(root, book_id):
    data={}
    data["book_id"] = root[book_id].get_book_id()
    data["title"] = root[book_id].title
    data["author"] = root[book_id].author
    data["year"] = root[book_id].year
    data["genre"] = root[book_id].genre
    data["isbn"] = root[book_id].isbn
    data["url"] = root[book_id].url
    return data

# #init data

# root = open_db_client()

# # # Create 5 example books
# book1 = create_book(root, "The Hunger Games", "Suzanne Collins", 2008, "Science Fiction", "978-0439023481", "https://www.amazon.com/Hunger-Games-Book/dp/B002MQYOFW")    
# book2 = create_book(root, "Harry Potter and the Philosopher's Stone", "J. K. Rowling", 1997, "Fantasy", "978-0747532743", "https://www.amazon.com/Harry-Potter-Philosophers-Stone-Rowling/dp/0747532745")
# book3 = create_book(root, "To Kill a Mockingbird", "Harper Lee", 1960, "Fiction", "978-0446310789", "https://www.amazon.com/Kill-Mockingbird-Harper-Lee/dp/0446310786")
# book4 = create_book(root, "Pride and Prejudice", "Jane Austen", 1813, "Romance", "978-0141439518", "https://www.amazon.com/Pride-Prejudice-Jane-Austen/dp/0141439513")
# book5 = create_book(root, "Twilight", "Stephenie Meyer", 2005, "Fantasy", "978-0316015844", "https://www.amazon.com/Twilight-Saga-Book-1/dp/0316015849")

# # # Get total number of books
# total_books = get_total_book(root)
# print(f"Total number of books: {total_books}")

# # # Get all book ids
# all_book_ids = get_all_book_id(root)
# print(f"All book ids: {all_book_ids}")

# # # Get book details
# print("Book details:")
# for book_id in all_book_ids:
#     book_details = get_book_detail(root, book_id)
#     print(book_details)

# # # Update a book
# update_book(root, "book1", "The Hunger Games", "Suzanne Collins", 2008, "Science Fiction", "978-0439023481", "https://www.amazon.com/Hunger-Games-Book/dp/B002MQYOFW")

# # # Get book details
# print("Book details:")
# for book_id in all_book_ids:
#     book_details = get_book_detail(root, book_id)
#     print(book_details)

# # close the database connection
# shutdown_db_client()










    


