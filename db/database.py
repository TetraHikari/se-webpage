import uuid
from persistent import Persistent


class Post(Persistent):
    def __init__(self, title, content):
        self.title = title
        self.content = content


class Accounts(Persistent):
    def __init__(self, username, email, password, year):
        self.email = email
        self.username = username
        self.password = password
        self.year = year
        self.posts = []

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_year(self):
        return self.year

    def all_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "year": self.year
        }

        return data

    def create_post(self, title, content):
        post_id = str(uuid.uuid4())  # Generate a unique post_id using uuid
        self.posts.append(
            {"post_id": post_id, 
             "title": title, 
             "content": content}
        )

    def update_post(self, post_id, new_title, new_content):
        if post_id in self.posts:
            self.posts[post_id]["title"] = {"title": new_title, "content": new_content}


    def delete_post(self, post_id):
        if post_id in self.posts:
            del self.posts[post_id]
    

from ZODB import FileStorage, DB
from persistent import Persistent

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


# from transaction import commit

# storage = FileStorage.FileStorage('db/account.fs')
# db = DB(storage)
# connection = db.open()
# root = connection.root()

# person1 = Accounts("65011610","65011610@kmitl.ac.th","123456",1)
# person2 = Accounts("65011611","65011611@kmitl.ac.th","123456",1)
# person3 = Accounts("65011612","65011612@kmitl.ac.th","123456",1)

# person1.create_post("Hello World", "This is my first post 65011610")
# person2.create_post("Hello World", "This is my first post 65011611")
# person3.create_post("Hello World", "This is my first post 65011612")

# # Store the Accounts objects with usernames as keys
# root["65011610"] = person1
# root["65011611"] = person2
# root["65011612"] = person3

# commit()

# Read

# print(root["65011610"].get_username())
# print(root["65011610"].get_email())
# print(root["65011610"].get_password())
# print(root["65011610"].get_year())
# print()
# for value in root["65011610"].allData().values():
#     print(value)


# print(root["65011610"].username)
# print(root["65011610"].email)
# print(root["65011610"].password)

# print(root["65011611"].username)
# print(root["65011611"].email)
# print(root["65011611"].password)

# print(root["65011612"].username)
# print(root["65011612"].email)
# print(root["65011612"].password)

#Read Posts
# for user in root:
#     for post in root[user].posts:
#         print(post["post_id"])
#         print(post["title"])
#         print(post["content"])
#         print()



# # Close the connection
# connection.close()
# db.close()




