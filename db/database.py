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

    



# create_account(root, "65011610", "65011610@kmitl.ac.th", "123456", 2, "Tonkla", "Pokaew")
# create_account(root, "65011611", "65011611@kmitl.ac.th", "123456", 3, "John", "Doe")
# create_account(root, "65011612", "65011610@kmitl.ac.th", "123456", 2, "Peeranut", "Kongthong")
# create_account(root, "65011613", "65011610@kmitl.ac.th", "123456", 2, "Ibrahim", "Ali")
# create_account(root, "65011614", "65011610@kmitl.ac.th", "123456", 2, "Mark", "Zuckerberg")

# commit()


# root = open_db_client()

# print(root["65011610"].username)
# print(root["65011610"].email)
# print(root["65011610"].password)
# print(root["65011610"].year)
# print(root["65011610"].get_fullname())

# shutdown_db_client()




    


    




