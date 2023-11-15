import os,sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*

   
def create_student(root, username, email, password, year, firstname, lastname):
    account = Student(username, email, password, year, firstname, lastname)
    root[account.get_username()] = account
    return account
   
def read_student(root, username):
    return root[username].all_data()

def read_all_student(root):
    student_list = []
    for key in root.keys():
        if isinstance(root[key], Student):
            student_list.append(root[key].all_data())
            
    return student_list
        
def update_student(root, username, email, password, year, firstname, lastname):
    root[username].email = email
    root[username].password = password
    root[username].year = year
    root[username].firstname = firstname
    root[username].lastname = lastname
    commit()
    print("account updated")
    

#Professor Services
def create_professor(root, username, email, password, firstname, lastname):
    account = Professor(username, email, password, firstname, lastname)
    root[account.get_username()] = account
    return account
    
def read_professor(root, username):
    return root[username].all_data()

def read_all_professor(root):
    professor_list = []
    for key in root.keys():
        if isinstance(root[key], Professor):
            professor_list.append(root[key].all_data())
            
    return professor_list
        
def update_professor(root, username, email, password, firstname, lastname, subject):
    root[username].email = email
    root[username].password = password
    root[username].firstname = firstname
    root[username].lastname = lastname
    root[username].subject = subject
    commit()
    print("professor updated")
    

    



