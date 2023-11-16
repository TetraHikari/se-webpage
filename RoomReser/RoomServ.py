import os,sys
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from db.database import*

def create_room(root, room_id, description, capacity):
    room = Room(room_id)
    room.description = description
    room.capacity = capacity
    root[room.get_room_id()] = room
    return room

def get_total_room(root):
    return len(root.keys())

def get_all_room_id(root):
    room_id_list = []
    for key in root.keys():
        if isinstance(root[key], Room):
            room_id_list.append(root[key].get_room_id())
    return room_id_list

def get_available_room_id(root):
    room_id_list = []
    for key in root.keys():
        if isinstance(root[key], Room):
            if root[key].is_reserved() == False:
                room_id_list.append(root[key].get_room_id())
    return room_id_list

def reserved_room(root, room_id):
    root[room_id].reservation = True
    commit()
    print("room reserved")
    
def cancel_room(root, room_id):
    root[room_id].reservation = False
    commit()
    print("room canceled")

def room_detail(root, room_id):
    data={}
    data["room_id"] = root[room_id].get_room_id()
    data["description"] = root[room_id].description
    data["capacity"] = root[room_id].capacity
    data["reservation"] = root[room_id].reservation
    return data


# # Open the database connection
# root = open_db_client()

# # Create 5 example rooms
# room1 = create_room(root, "Room101", "Small meeting room", 10)
# room2 = create_room(root, "Room102", "Medium meeting room", 15)
# room3 = create_room(root, "Room201", "Large meeting room", 20)
# room4 = create_room(root, "Room202", "Conference room", 30)
# room5 = create_room(root, "Room301", "Training room", 25)

# # Get total number of rooms
# total_rooms = get_total_room(root)
# print(f"Total number of rooms: {total_rooms}")

# # Get all room IDs
# all_room_ids = get_all_room_id(root)
# print("All Room IDs:", all_room_ids)

# # Get available room IDs
# available_room_ids = get_available_room_id(root)
# print("Available Room IDs:", available_room_ids)

# # Reserve a room (assuming Room101 is available)
# reserve_room_id = "Room101"
# reserved_room(root, reserve_room_id)

# # Get available room IDs after reservation
# updated_available_room_ids = get_available_room_id(root)
# print("Available Room IDs after reservation:", updated_available_room_ids)

# # Cancel reservation for a room (assuming Room101 is reserved)
# cancel_room_id = "Room101"
# cancel_room(root, cancel_room_id)

# # Get available room IDs after cancellation
# updated_available_room_ids = get_available_room_id(root)
# print("Available Room IDs after cancellation:", updated_available_room_ids)

# # Close the database connection
# shutdown_db_client()

# root = open_db_client()

# for room_id in root.keys():
#     if isinstance(root[room_id], Room):
#         print(room_detail(root, room_id))

# shutdown_db_client()