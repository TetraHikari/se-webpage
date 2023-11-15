import os,sys


current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*
from Login.LoginServ import*

def add_student_subject(root, username, subject, score):
    root[username].subjects[subject] = score
    commit()
    

def add_professor_subject(root, username, subject):
    root[username].subjects[subject] = subject
    commit()
    
def get_student_from_subject(root, subject):
    student_list = []
    for key in root.keys():
        if isinstance(root[key], Student):
            if subject in root[key].subjects.keys():
                student_list.append(root[key].all_data())
    return student_list

def get_professor_from_subject(root, subject):
    professor_list = []
    for key in root.keys():
        if isinstance(root[key], Professor):
            if subject in root[key].subjects.keys():
                professor_list.append(root[key].all_data())
    return professor_list

def get_subject_from_student(root, username):
    subject_list = []
    for subject in root[username].subjects:
        subject_list.append(subject)
    return subject_list

def get_subject_from_professor(root, username):
    subject_list = []
    for subject in root[username].subjects:
        subject_list.append(subject)
    return subject_list

    

# Open the database connection
root = open_db_client()

# Create 5 student accounts
student1 = create_student(root, "65011610", "65011610@kmitl.ac.th", "123456", 2, "Tonkla", "Pokaew")
student2 = create_student(root, "65011611", "65011611@kmitl.ac.th", "123456", 3, "John", "Doe")
student3 = create_student(root, "65011612", "65011612@kmitl.ac.th", "123456", 2, "Peeranut", "Kongthong")
student4 = create_student(root, "65011613", "65011613@kmitl.ac.th", "123456", 4, "Ibrahim", "Ali")
student5 = create_student(root, "65011614", "65011614@kmitl.ac.th", "123456", 4, "Mark", "Zuckerberg")

# Create 5 professor accounts
professor1 = create_professor(root, "professor1", "professor1@kmitl", "123456", "Prof. Max", "Oloak")
professor2 = create_professor(root, "professor2", "professor2@kmitl", "123456", "Prof. John", "Lake")
professor3 = create_professor(root, "professor3", "professor3@kmitl", "123456", "Prof. Micheal", "Hamza")
professor4 = create_professor(root, "professor4", "professor4@kmitl", "123456", "Prof. Sarah", "Johnson")
professor5 = create_professor(root, "professor5", "professor5@kmitl", "123456", "Prof. Emily", "Brown")

# Associate students with subjects
add_student_subject(root, "65011610", "Computer Science", 90)
add_student_subject(root, "65011610", "Database Management", 85)
add_student_subject(root, "65011610", "Artificial Intelligence", 88)
add_student_subject(root, "65011610", "Web Programming", 95)
add_student_subject(root, "65011610", "Software Engineering", 91)

add_student_subject(root, "65011611", "Computer Science", 92)
add_student_subject(root, "65011611", "Database Management", 87)
add_student_subject(root, "65011611", "Artificial Intelligence", 89)
add_student_subject(root, "65011611", "Web Programming", 94)
add_student_subject(root, "65011611", "Software Engineering", 90)

add_student_subject(root, "65011612", "Computer Science", 91)
add_student_subject(root, "65011612", "Database Management", 86)
add_student_subject(root, "65011612", "Artificial Intelligence", 87)
add_student_subject(root, "65011612", "Web Programming", 93)
add_student_subject(root, "65011612", "Software Engineering", 92)

add_student_subject(root, "65011613", "Computer Science", 88)
add_student_subject(root, "65011613", "Database Management", 83)
add_student_subject(root, "65011613", "Artificial Intelligence", 86)
add_student_subject(root, "65011613", "Web Programming", 92)
add_student_subject(root, "65011613", "Software Engineering", 89)

add_student_subject(root, "65011614", "Computer Science", 94)
add_student_subject(root, "65011614", "Database Management", 89)
add_student_subject(root, "65011614", "Artificial Intelligence", 91)
add_student_subject(root, "65011614", "Web Programming", 96)
add_student_subject(root, "65011614", "Software Engineering", 93)

# Associate professors with subjects
add_professor_subject(root, "professor1", "Computer Science")
add_professor_subject(root, "professor2", "Database Management")
add_professor_subject(root, "professor3", "Web Programming")
add_professor_subject(root, "professor4", "Artificial Intelligence")
add_professor_subject(root, "professor5", "Software Engineering")

# Commit the transaction
commit()



# Read students from a subject
subject_name = "Computer Science"
print(f"Students taking {subject_name}:")
students_in_subject = get_student_from_subject(root, subject_name)
for student in students_in_subject:
    print(student)

# Read professors from a subject
subject_name = "Computer Science"
print(f"\nProfessors teaching {subject_name}:")
professors_in_subject = get_professor_from_subject(root, subject_name)
for professor in professors_in_subject:
    print(professor)
    
print(get_subject_from_student(root, "65011610"))
print(get_subject_from_professor(root, "professor1"))

# Close the database connection
shutdown_db_client()

