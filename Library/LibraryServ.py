import os,sys
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*
import uuid

# auto create book_id
import uuid

def create_book(root, title, author, year, genre, isbn, book_url, cover_url):
    book_id = str(uuid.uuid4())  # Generate a unique UUID
    book = Book(book_id, title, author, year, genre, isbn, book_url, cover_url)
    root[book_id] = book
    commit()
    return book.all_data()  # Return the data of the newly created book


 #also use isinstance

def get_book_info(root, book_id):
    return root[book_id].all_data()

def clear_book_database():
    root = open_db_client()
    try:
        for key in list(root.keys()):
            if isinstance(root[key], Book):
                del root[key]
        commit()
        print("Book database cleared")
    finally:
        shutdown_db_client()

def get_all_books(root):
    book_list = []
    for key in root:
        if isinstance(root[key], Book):
            book_list.append(root[key].all_data())
    return book_list

def get_book_from_title(root, title):
    book_list = []
    for key in root:
        if isinstance(root[key], Book):
            if root[key].get_title() == title:
                book_list.append(root[key].all_data())
    return book_list

def get_book_from_author(root, author):
    book_list = []
    for key in root:
        if isinstance(root[key], Book):
            if root[key].get_author() == author:
                book_list.append(root[key].all_data())
    return book_list

def get_book_from_year(root, year):
    book_list = []
    for key in root:
        if isinstance(root[key], Book):
            if root[key].get_year() == year:
                book_list.append(root[key].all_data())
    return book_list

def get_book_from_genre(root, genre):
    book_list = []
    for key in root:
        if isinstance(root[key], Book):
            if root[key].get_genre() == genre:
                book_list.append(root[key].all_data())
    return book_list

def get_book_from_isbn(root, isbn):
    book_list = []
    for key in root:
        if isinstance(root[key], Book):
            if root[key].get_isbn() == isbn:
                book_list.append(root[key].all_data())
    return book_list

def get_book_from_book_url(root, book_url):
    book_list = []
    for key in root:
        if isinstance(root[key], Book):
            if root[key].get_book_url() == book_url:
                book_list.append(root[key].all_data())
    return book_list

def delete_book_from_id(root, book_id):
    del root[book_id]
    commit()


# #initialize database
# clear_book_database()
# root = open_db_client()

# #add books
# create_book(root, "The Hunger Games", "Suzanne Collins", "2008", "Science Fiction", "978-3-16-148410-0", "https://en.wikipedia.org/wiki/The_Hunger_Games", "https://upload.wikimedia.org/wikipedia/en/thumb/3/39/The_Hunger_Games_cover.jpg/220px-The_Hunger_Games_cover.jpg")
# create_book(root, "Harry Potter and the Philosopher's Stone", "J. K. Rowling", "1997", "Fantasy", "978-3-16-148410-1", "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Philosopher%27s_Stone", "https://www.adazing.com/wp-content/uploads/2022/12/Harry-Potter-Book-Covers-Order-of-the-Phoenix-667x1024.jpg")
# create_book(root, "Twilight", "Stephenie Meyer", "2005", "Fantasy", "978-3-16-148410-2", "https://en.wikipedia.org/wiki/Twilight_(novel)", "https://upload.wikimedia.org/wikipedia/en/thumb/1/1d/Twilightbook.jpg/220px-Twilightbook.jpg")

# #commit
# commit()
# shutdown_db_client()
