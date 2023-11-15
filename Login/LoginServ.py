import os,sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*


def create_account(root, username, email, password, year, firstname, lastname):
    root[username] = Accounts(username, email, password, year, firstname, lastname)
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
    
#Professor Services

def create_professor(root, username, email, password, firstname, lastname, subject):
    root[username] = Professor(username, email, password, firstname, lastname, subject)
    commit()
    print("professor created")
    
def read_professor(root, username):
    return root[username].all_data()

def read_all_professor(root):
    for key in root.keys():
        print(root[key].all_data())
        
def update_professor(root, username, email, password, firstname, lastname, subject):
    root[username].email = email
    root[username].password = password
    root[username].firstname = firstname
    root[username].lastname = lastname
    root[username].subject = subject
    commit()
    print("professor updated")
    
    
    
# root = open_db_client()
# for i in root:
#     clear_all_posts(root, i)
# shutdown_db_client()

# root = open_db_client()
# create_account(root, "65011610", "65011610@kmitl.ac.th", "123456", 2, "Tonkla", "Pokaew")
# create_account(root, "65011611", "65011611@kmitl.ac.th", "123456", 3, "John", "Doe")
# create_account(root, "65011612", "65011610@kmitl.ac.th", "123456", 2, "Peeranut", "Kongthong")
# create_account(root, "65011613", "65011610@kmitl.ac.th", "123456", 4, "Ibrahim", "Ali")
# create_account(root, "65011614", "65011610@kmitl.ac.th", "123456", 4, "Mark", "Zuckerberg")

# create_post(root, "65011610", str(uuid.uuid4()), "65011610", "content1",datetime.datetime.now().ctime(),0)
# create_post(root, "65011610", str(uuid.uuid4()), "65011610", "content2",datetime.datetime.now().ctime(),0)
# create_post(root, "65011610", str(uuid.uuid4()), "65011610", "content3",datetime.datetime.now().ctime(),0)
# create_post(root, "65011610", str(uuid.uuid4()), "65011610", "content4",datetime.datetime.now().ctime(),0)

# create_post(root, "65011611", str(uuid.uuid4()), "65011611", "content1",datetime.datetime.now().ctime(),0)
# create_post(root, "65011611", str(uuid.uuid4()), "65011611", "content2",datetime.datetime.now().ctime(),0)
# create_post(root, "65011611", str(uuid.uuid4()), "65011611", "content3",datetime.datetime.now().ctime(),0)
# create_post(root, "65011611", str(uuid.uuid4()), "65011611", "content4",datetime.datetime.now().ctime(),0)

# create_post(root, "65011612", str(uuid.uuid4()), "65011612", "content1",datetime.datetime.now().ctime(),0)
# create_post(root, "65011612", str(uuid.uuid4()), "65011612", "content2",datetime.datetime.now().ctime(),0)
# create_post(root, "65011612", str(uuid.uuid4()), "65011612", "content3",datetime.datetime.now().ctime(),0)
# create_post(root, "65011612", str(uuid.uuid4()), "65011612", "content4",datetime.datetime.now().ctime(),0)

# create_post(root, "65011613", str(uuid.uuid4()), "65011613", "content1",datetime.datetime.now().ctime(),0)
# create_post(root, "65011613", str(uuid.uuid4()), "65011613", "content2",datetime.datetime.now().ctime(),0)
# create_post(root, "65011613", str(uuid.uuid4()), "65011613", "content3",datetime.datetime.now().ctime(),0)
# create_post(root, "65011613", str(uuid.uuid4()), "65011613", "content4",datetime.datetime.now().ctime(),0)

# create_post(root, "65011614", str(uuid.uuid4()), "65011614", "content1",datetime.datetime.now().ctime(),0)
# create_post(root, "65011614", str(uuid.uuid4()), "65011614", "content2",datetime.datetime.now().ctime(),0)
# create_post(root, "65011614", str(uuid.uuid4()), "65011614", "content3",datetime.datetime.now().ctime(),0)
# create_post(root, "65011614", str(uuid.uuid4()), "65011614", "content4",datetime.datetime.now().ctime(),0)

# print(root["65011610"].username)
# print(root["65011610"].email)
# print(root["65011610"].password)
# print(root["65011610"].year)
# print(root["65011610"].get_fullname())



# # Display the posts before updating the "like" count
# for user in root:
#     for post in read_all_post(root, user):
#         print(post["title"])
#         print(post["content"])
#         print(post["time"])
#         print(post["like"])

# Update the "like" count for each post
# for user in root:
#     for post_id in root[user].posts.keys():
#         root[user].posts[post_id]["like"] = 6;
#         commit()

# Commit the changes to the database


# Display the posts after updating the "like" count
# for user in root:
#     for post in read_all_post(root, user):
#         print(post["title"])
#         print(post["content"])
#         print(post["time"])
#         print(post["like"])

# Close the database connection


# add_post(root, "65011610", str(uuid.uuid4()), "65011610", "new post",datetime.datetime.now().ctime(),0)


# print(read_all_post(root, "65011610"))
                
# add_like(root, "051248f5-986b-4d16-818a-538c6a1f1c8a", 7, "65011613")

# print(read_all_post(root, "65011610"))

# shutdown_db_client()


#Create Professor account
root = open_db_client()
# create_professor(root, "professor1", "professor1@kmitl", "123456", "Prof. Max", "Oloak", "AI")
# create_professor(root, "professor2", "professor2@kmitl", "123456", "Prof. John", "Lake", "Database")
# create_professor(root, "professor3", "professor3@kmitl", "123456", "Prof. Micheal", "Hamza", "Web Programming")

# read_all_professor(root)

shutdown_db_client()