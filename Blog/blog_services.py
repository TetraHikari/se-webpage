import sys,os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*

def get_all_post():
    posts = []
    root = open_db_client()
    for user in root:
        for post in root[user].posts:
            posts.append({
                "post_id": post["post_id"],
                "title": post["title"],
                "content": post["content"]
            })
    shutdown_db_client()
    return posts

print(get_all_post())
