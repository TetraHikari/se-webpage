import sys,os
import uuid
import datetime
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*

#Blog Services
def create_post(root, username, post_id, title, content,created_at):
    root[username].posts[post_id] = {
        "post_id": post_id,
        "title": title,
        "content": content,
        "time": created_at
    }
    commit()
    print("post created")
    
def read_post(root, username, post_id):
    return root[username].posts[post_id]

def read_all_post(root, username):
    post_list = []
    for post_id, post_data in root[username].posts.items():
        post_list.append(
            {
                "post_id": post_id,
                "title": post_data.get("title", ""),
                "content": post_data.get("content", ""),
                "time": post_data.get("time", "")  # Provide a default value if 'time' is not present
            }
        )
    return post_list

def clear_all_posts(root, username):
    root[username].posts = {}
    commit()
    print("All posts for user {} cleared.".format(username))


root = open_db_client()
for i in root:
    clear_all_posts(root, i)
shutdown_db_client()



# print(root["65011611"].username)
# print(root["65011611"].email)
# print(root["65011611"].password)
# print(root["65011611"].year)



# create_post(root, "65011610", str(uuid.uuid4()), "title1", "content1",datetime.datetime.now().ctime())
# create_post(root, "65011610", str(uuid.uuid4()), "title2", "content2",datetime.datetime.now().ctime())
# create_post(root, "65011610", str(uuid.uuid4()), "title3", "content3",datetime.datetime.now().ctime())
# create_post(root, "65011610", str(uuid.uuid4()), "title4", "content4",datetime.datetime.now().ctime())


# for user in root:
#     for post in read_all_post(root, user):
#         print(post["title"])
#         print(post["content"])
#         print(post["time"] )
#         print()
    
# shutdown_db_client()


