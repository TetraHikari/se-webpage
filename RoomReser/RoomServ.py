import os,sys
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*


def create_room(root, room_id, roomType, capacity):
    room = Room(room_id, roomType, capacity)
    root[room_id] = room
    commit()
    return room

def add_time_slot(root, room_id, slot):
    root[room_id].reservation[slot] = {"status": "available", 
                                       "username": ""}
    commit()



def get_available_room(root, slot):
    room_list = []
    for key in root:
        if isinstance(root[key], Room):
            if root[key].reservation[slot]["status"] == "available":
                room_list.append(key)
    return room_list

def get_room_info(root, room_id):
    return root[room_id].get_reservation()


def clear_room_database():
    root = open_db_client()
    try:
        for key in list(root.keys()):
            if isinstance(root[key], Room):
                del root[key]
        commit()
        print("Room database cleared")
    finally:
        shutdown_db_client()
        
def get_room_from_timeslot(root, slot):
    room_list = []
    for key in root:
        if isinstance(root[key], Room):
            room_list.append({"room_id": key, "status": root[key].reservation[slot]["status"]})
    return room_list

#clear_room_database()

def reserve_room(root, room_id, slot, username):
    root[room_id].reservation[slot] = {"status": "reserved","username": username}
    commit()
    
def cancel_room(root, room_id, slot):
    root[room_id].reservation[slot] = {"status": "available","username": ""}
    commit()
    
def reservation_detail(root, username):
    room_list = []
    for key in root:
        if isinstance(root[key], Room):
            for slot in root[key].reservation:
                if root[key].reservation[slot]["username"] == username:
                    room_list.append({"room_id": key, "slot": slot})
    return room_list
times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

def remove_all_room(root):
    for key in list(root.keys()):
        if isinstance(root[key], Room):
            del root[key]
    commit()




# root = open_db_client()

# cancel_room(root, "801", "08:00")
# cancel_room(root, "801", "09:00")
# cancel_room(root, "801", "10:00")
# cancel_room(root, "801", "11:00")
# cancel_room(root, "801", "12:00")
# cancel_room(root, "801", "13:00")
# cancel_room(root, "801", "14:00")
# cancel_room(root, "801", "15:00")
# cancel_room(root, "801", "16:00")
# cancel_room(root, "801", "17:00")
# cancel_room(root, "801", "18:00")

# shutdown_db_client()


# root = open_db_client()
# # Create 801 Lecture Room
# create_room(root, "801", "lecture", 50)
# add_time_slot(root, "801", "08:00")
# add_time_slot(root, "801", "09:00")
# add_time_slot(root, "801", "10:00")
# add_time_slot(root, "801", "11:00")
# add_time_slot(root, "801", "12:00")
# add_time_slot(root, "801", "13:00")
# add_time_slot(root, "801", "14:00")
# add_time_slot(root, "801", "15:00")
# add_time_slot(root, "801", "16:00")
# add_time_slot(root, "801", "17:00")
# add_time_slot(root, "801", "18:00")

# # Create 802 Lecture Room
# create_room(root, "802", "lecture", 40)
# add_time_slot(root, "802", "08:00")
# add_time_slot(root, "802", "09:00")
# add_time_slot(root, "802", "10:00")
# add_time_slot(root, "802", "11:00")
# add_time_slot(root, "802", "12:00")
# add_time_slot(root, "802", "13:00")
# add_time_slot(root, "802", "14:00")
# add_time_slot(root, "802", "15:00")
# add_time_slot(root, "802", "16:00")
# add_time_slot(root, "802", "17:00")
# add_time_slot(root, "802", "18:00")

# # Create 803 Lecture Room
# create_room(root, "803", "lecture", 60)
# add_time_slot(root, "803", "08:00")
# add_time_slot(root, "803", "09:00")
# add_time_slot(root, "803", "10:00")
# add_time_slot(root, "803", "11:00")
# add_time_slot(root, "803", "12:00")
# add_time_slot(root, "803", "13:00")
# add_time_slot(root, "803", "14:00")
# add_time_slot(root, "803", "15:00")
# add_time_slot(root, "803", "16:00")
# add_time_slot(root, "803", "17:00")
# add_time_slot(root, "803", "18:00")

# # Create 804 Lecture Room
# create_room(root, "804", "lecture", 30)
# add_time_slot(root, "804", "08:00")
# add_time_slot(root, "804", "09:00")
# add_time_slot(root, "804", "10:00")
# add_time_slot(root, "804", "11:00")
# add_time_slot(root, "804", "12:00")
# add_time_slot(root, "804", "13:00")
# add_time_slot(root, "804", "14:00")
# add_time_slot(root, "804", "15:00")
# add_time_slot(root, "804", "16:00")
# add_time_slot(root, "804", "17:00")
# add_time_slot(root, "804", "18:00")

# # Create 805 Lab Room
# create_room(root, "805", "lab", 20)
# add_time_slot(root, "805", "08:00")
# add_time_slot(root, "805", "09:00")
# add_time_slot(root, "805", "10:00")
# add_time_slot(root, "805", "11:00")
# add_time_slot(root, "805", "12:00")
# add_time_slot(root, "805", "13:00")
# add_time_slot(root, "805", "14:00")
# add_time_slot(root, "805", "15:00")
# add_time_slot(root, "805", "16:00")
# add_time_slot(root, "805", "17:00")
# add_time_slot(root, "805", "18:00")

# shutdown_db_client()

# root = open_db_client()

# # print(f'AVAILABLE ROOMS AT 08:00: {get_available_room(root, "08:00")}')

# shutdown_db_client()



# root = open_db_client()

# print(reservation_detail(root, "65011610"))

# shutdown_db_client()

