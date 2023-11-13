from persistent import Persistent


class Post(Persistent):
    def __init__(self, title, content):
        self.title = title
        self.content = content

class Accounts(Persistent):
    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.password = password
        self.posts = []  # List to store the user's posts

    def create_post(self, title, content):
        post = Post(title, content)
        self.posts.append(post)


    def update_post(self, post, new_title, new_content):
        post.title = new_title
        post.content = new_content

    def delete_post(self, post):
        self.posts.remove(post)
        
from ZODB import FileStorage, DB
from persistent import Persistent
from transaction import commit

storage = FileStorage.FileStorage('db/account.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

person1 = Accounts("65011610","65011610@kmitl.ac.th","123456")
person2 = Accounts("65011611","65011611@kmitl.ac.th","123456")
person3 = Accounts("65011612","65011612@kmitl.ac.th","123456")

person1.create_post("Hello World!", "This is my first post.")
person2.create_post("Second Post", "This is my second post.")
person3.create_post("Third Post", "This is my third post.")

# Store the Accounts objects with usernames as keys
root["65011610"] = person1
root["65011611"] = person2
root["65011612"] = person3

commit()

# Read
print(root["65011610"].username)
print(root["65011610"].email)
print(root["65011610"].password)

print(root["65011611"].username)
print(root["65011611"].email)
print(root["65011611"].password)

print(root["65011612"].username)
print(root["65011612"].email)
print(root["65011612"].password)

#Read Posts
print(root["65011610"].posts[0].title)
print(root["65011610"].posts[0].content)

print(root["65011611"].posts[0].title)
print(root["65011611"].posts[0].content)

print(root["65011612"].posts[0].title)
print(root["65011612"].posts[0].content)

# Close the connection
connection.close()
db.close()




