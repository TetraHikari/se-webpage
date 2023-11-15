
import uuid
import datetime
import sys,os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*

#Blog Services
# def create_post(root, username, post_id, title, content,created_at,like):
#     root[username].posts[post_id] = {
#         "post_id": post_id,
#         "title": title,
#         "content": content,
#         "time": created_at,
#         "like":like,
#         "liked_by":[]
#     }
#     commit()
#     print("post created")
    
# def read_all_post(root, username):
#     post_list = []
#     for post_id, post_data in root[username].posts.items():
#         post_list.append(
#             {
#                 "username": username,
#                 "post_id": post_id,
#                 "title": post_data.get("title", ""),
#                 "content": post_data.get("content", ""),
#                 "time": post_data.get("time", ""),  # Provide a default value if 'time' is not present
#                 "like": post_data.get("like", 0),
#                 "liked_by": post_data.get("liked_by", [])
#             }
#         )
#     return post_list

# Blog Services
def create_post(root, username, post_id, title, content, created_at, like):
    if isinstance(root[username], Accounts) or isinstance(root[username], Professor):
        root[username].posts[post_id] = {
            "post_id": post_id,
            "title": title,
            "content": content,
            "time": created_at,
            "like": like,
            "liked_by": []
        }
        commit()
        print("post created")
    else:
        print("Invalid user type")

def read_all_post(root, username):
    post_list = []
    if isinstance(root[username], Accounts) or isinstance(root[username], Professor):
        for post_id, post_data in root[username].posts.items():
            post_list.append(
                {
                    "username": username,
                    "post_id": post_id,
                    "title": post_data.get("title", ""),
                    "content": post_data.get("content", ""),
                    "time": post_data.get("time", ""),
                    "like": post_data.get("like", 0),
                    "liked_by": post_data.get("liked_by", [])
                }
            )
    else:
        print("Invalid user type")

    return post_list

# def add_post(root, username, post_id, title, content,created_at,like):
#     root[username].posts[post_id] = {
#         "post_id": post_id,
#         "title": title,
#         "content": content,
#         "time": created_at,
#         "like":like
#     }
#     commit()
#     print("post added")

# def add_like(root, post_id, new_like_count, username):
#     for user in root:
#         for post_key in list(root[user].posts.keys()):
#             #one user can give 1 like to 1 post
#             if post_key == post_id:
#                 if "liked_by" not in root[user].posts[post_key]:
#                     root[user].posts[post_key]["liked_by"] = []

#                 if username not in root[user].posts[post_key]["liked_by"]:
#                     updated_post = root[user].posts[post_key].copy()
#                     updated_post["like"] = new_like_count
#                     root[user].posts[post_key] = updated_post
#                     root[user].posts[post_key]["liked_by"].append(username)
#                     commit()
#                     print("Like added")

def add_post(root, username, post_id, title, content, created_at, like):
    if isinstance(root[username], Accounts) or isinstance(root[username], Professor):
        if "posts" not in root[username].__dict__:
            root[username].__dict__["posts"] = OOBTree()

        root[username].posts[post_id] = {
            "post_id": post_id,
            "title": title,
            "content": content,
            "time": created_at,
            "like": like,
            "liked_by": []
        }
        commit()
        print("Post added")
    else:
        print("Invalid user type")

def add_like(root, post_id, new_like_count, username):
    for user in root:
        if isinstance(root[user], Accounts) or isinstance(root[user], Professor):
            if "posts" in root[user].__dict__:
                for post_key in list(root[user].posts.keys()):
                    # one user can give 1 like to 1 post
                    if post_key == post_id:
                        if "liked_by" not in root[user].posts[post_key]:
                            root[user].posts[post_key]["liked_by"] = []

                        if username not in root[user].posts[post_key]["liked_by"]:
                            updated_post = root[user].posts[post_key].copy()
                            updated_post["like"] = new_like_count
                            root[user].posts[post_key] = updated_post
                            root[user].posts[post_key]["liked_by"].append(username)
                            commit()
                            print("Like added")
            else:
                print("Invalid user type")


    
def read_post(root, username, post_id):
    return root[username].posts[post_id]


def clear_all_posts(root, username):
    root[username].posts = {}
    commit()
    print("All posts for user {} cleared.".format(username))












