
import uuid
import datetime
import sys,os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*

#Blog Services
def create_post(root, username, post_id, title, content,created_at,like, postedby, yearpost):
    root[username].posts[post_id] = {
        "post_id": post_id,
        "title": title,
        "content": content,
        "time": created_at,
        "like":like,
        "postedby": postedby,
        "yearpost": yearpost,
        "liked_by":[]

    }
    commit()
    print("post created")
    
def read_post(root, username, post_id):
    return root[username].posts[post_id]

def add_post(root, username, post_id, title, content,created_at,like, postedby, yearpost):
    root[username].posts[post_id] = {
        "post_id": post_id,
        "title": title,
        "content": content,
        "time": created_at,
        "like":like,
        "postedby": postedby,
        "yearpost": yearpost,

    }
    commit()
    print("post added")


# def add_like(root, post_id, new_like_count, username):
#     for user in root:
#         for post_key in list(root[user].posts.keys()):
#             #one user can give 1 like to 1 post
#             if post_key == post_id:
#                 if username not in root[user].posts[post_key]["liked_by"]:
#                     updated_post = root[user].posts[post_key].copy()
#                     updated_post["like"] = new_like_count
#                     root[user].posts[post_key] = updated_post
#                     root[user].posts[post_key]["liked_by"].append(username)
#                     commit()
#                     print("Like added")

def add_like(root, post_id, new_like_count, username):
    for user in root:
        # Check if the object is an instance of Accounts
        if isinstance(root[user], Accounts):
            for post_key in list(root[user].posts.keys()):
                # One user can give 1 like to 1 post
                if post_key == post_id:
                    if "liked_by" not in root[user].posts[post_key]:
                        root[user].posts[post_key]["liked_by"] = []

                    if username not in root[user].posts[post_key]["liked_by"]:
                        updated_post = root[user].posts[post_key].copy()
                        updated_post["like"] = new_like_count
                        updated_post["liked_by"].append(username)  # Update liked_by in the copied dict
                        root[user].posts[post_key] = updated_post  # Replace the old post with the updated one
                        commit()
                        print("Like added")



def read_all_post(root, username):
    post_list = []
    # Check if the object associated with the username is an instance of Accounts
    if isinstance(root.get(username, None), Accounts):
        for post_id, post_data in root[username].posts.items():
            post_list.append(
                {
                    "username": username,
                    "post_id": post_id,
                    "title": post_data.get("title", ""),
                    "content": post_data.get("content", ""),
                    "time": post_data.get("time", ""),  # Provide a default value if 'time' is not present
                    "like": post_data.get("like", 0),
                    "liked_by": post_data.get("liked_by", []),
                    "postedby": post_data.get("postedby", ""),
                    "yearpost": post_data.get("yearpost", "")  # Add this line
                }
            )
    return post_list


def clear_all_posts(root, username):
    root[username].posts = {}
    commit()
    print("All posts for user {} cleared.".format(username))


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


