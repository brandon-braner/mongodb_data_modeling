from pymongo import MongoClient
from bson.objectid import ObjectId
from faker import Faker
from datetime import datetime, timedelta
import random


import argparse

parser = argparse.ArgumentParser(description='Generate daycare data')
parser.add_argument('--events-per-child', type=int, default=200, help='Number of events per child')
parser.add_argument('--db_name', type=str, default='daycare_db', help='Name of the database')
args = parser.parse_args()


# Configuration
NUM_CHILDREN = 10000
NUM_STAFF = 100
NUM_EVENTS_PER_CHILD = args.events_per_child
BATCH_SIZE = 10000

DB_NAME = args.db_name

fake = Faker()
client = MongoClient('mongodb://root:password@localhost:27017/') # change if you have a different host or port
db = client[DB_NAME]
children_collection = db['children']
staff_collection = db['staff']
daily_events_collection = db['dailyEvents']

def convert_to_mongo_date(date_data):
    return datetime.combine(date_data, datetime.min.time())

def generate_child_data():
    children = []
    for _ in range(NUM_CHILDREN):
        date_of_birth = convert_to_mongo_date(fake.date_of_birth(minimum_age=1, maximum_age=6))
        # print(f'DATA OF BIRTH TYPE {type(date_of_birth)}')
        child = {
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'dateOfBirth': date_of_birth,
            'enrollmentDate': fake.date_time_between(start_date='-3y'),
            'allergies': random.sample(['nuts', 'dairy', 'gluten', 'soy', 'eggs', 'fish'], random.randint(0, 3)),
            'emergencyContact': {
                'name': fake.name(),
                'phone': fake.phone_number(),
                'relationship': random.choice(['Parent', 'Grandparent', 'Guardian'])
            }
        }
        children.append(child)
    return children


def generate_staff_data():
    staff_members = []
    for _ in range(NUM_STAFF):
        hire_date = convert_to_mongo_date(fake.date_between(start_date='-5y'))
        staff = {
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'hireDate': hire_date,
            'role': random.choice(["Teacher", "Assistant", "Director"]),
            'credentials': random.sample(["CPR", "First Aid", "ECE", "CDA"], random.randint(0, 4))
        }
        staff_members.append(staff)
    return staff_members


def generate_event_data(child_ids, staff_ids):
    events = []
    event_types = ["Arrival", "Nap", "Meal", "Activity", "Departure", "Diaper Change"]
    for child_id in child_ids:
        for _ in range(NUM_EVENTS_PER_CHILD):
          random_timestamp = fake.date_time_between(start_date='-600d', end_date='now')
          event_type = random.choice(event_types)

          event = {
              'childId': child_id,
              'staffId': random.choice(staff_ids),
              'timestamp': random_timestamp,
              'eventType': event_type,
              'details': fake.text(max_nb_chars=50),
              'notes': fake.text(max_nb_chars=100)
            }
          events.append(event)
    return events
    
def insert_data():

    # Insert children data
    print("Inserting Children Data")
    children = generate_child_data()
    inserted_children = children_collection.insert_many(children)
    child_ids = inserted_children.inserted_ids

    # Insert staff data
    print("Inserting Staff Data")
    staff_members = generate_staff_data()
    inserted_staff = staff_collection.insert_many(staff_members)
    staff_ids = inserted_staff.inserted_ids

    print("Inserting Events Data")
    events = generate_event_data(child_ids,staff_ids)
    
    # # Insert event data in batches
    print("Inserting event data in batches")
    num_of_event_insertions = len(events) // BATCH_SIZE
    
    for i in range(0, len(events), BATCH_SIZE):
        print(f"Inserting batch {i // BATCH_SIZE + 1}/{num_of_event_insertions}")
        batch = events[i:i + BATCH_SIZE]
        daily_events_collection.insert_many(batch)
    
    print("Data insertion complete.")


if __name__ == "__main__":
    insert_data()