import os
import json

# fake clickstream data
from faker import Faker
from faker_clickstream import ClickstreamProvider


def create_clickstream_data(sessions=500, flatten=True):
    fake = Faker()
    fake.add_provider(ClickstreamProvider)

    sessions = [fake.session_clickstream() for s in range(sessions)]
    print(len(sessions), " fake sessions were generated.")

    if flatten:
        events = {"data": [event for s in sessions for event in s]}
        print(len(events["data"]), " records were generated.")
        
        return events
    
def save_to_file(data):
    
    file = "clickstream_data.json"
    fp = os.path.join("data", file)
    
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Fake data saved to {fp}")

if __name__ == "__main__":
    
    data = create_clickstream_data()
    save_to_file(data)
