import pandas as pd
import random
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd


life_periods = [
    {"Period": "Childhood", "Stage": "Early", "Themes": "Family, Play", "Location": "Dayton", "Duration": "12 years", "Emotion": "Positive"},
    {"Period": "High School", "Stage": "Adolescence", "Themes": "Education, Friends", "Location": "Troy", "Duration": "4 years", "Emotion": "Mixed"},
    {"Period": "University", "Stage": "Early Adulthood", "Themes": "Independence, Education", "Location": "Austin", "Duration": "4 years", "Emotion": "Positive"},
    {"Period": "Career", "Stage": "Adult", "Themes": "Professional Growth, Travel", "Location": "San Antonio", "Duration": "10 years", "Emotion": "Mixed"}
]

people = ["Frank", "Lisa", "Tim", "Joe"]
places = ["Beach", "Paris", "Vegas", "Tennessee", "Dayton", "Coffee Shop", "Iceland", "San Antonio"]
events = ["Vacation", "Graduation", "Wedding", "Basketball", "Fishing", "Hiking", "Sleeping", "Running"]
times = ["1998", "two years ago", "Childhood", "Last Year", "This Year", "2001", "2015", "March", "July"]


memories = [
    f"{event} with {person} at {place}" for event in events for person in people for place in places
]

def generate_conway_memory_dataset(n=100):
    data = []

    for _ in range(n):
        memory = random.choice(memories)
        person = random.choice(people)
        place = random.choice(places)
        event = random.choice(events)
        time = random.choice(times)
        
        data.append([memory, person, place, event, time])

    df = pd.DataFrame(data, columns=["Memory", "Person", "Place", "Event", "Time"])
    df = df.sample(frac=1).reset_index(drop=True)
    return df

conway_memory_dataset = generate_conway_memory_dataset(100)
# print(conway_memory_dataset.head(50))

# Semantic embeddings (SentenceTransformer)
model = SentenceTransformer('all-MiniLM-L6-v2')
text_embeddings = model.encode(conway_memory_dataset["Memory"])

# One-hot encode categorical dimensions clearly
categorical_embeddings = pd.get_dummies(conway_memory_dataset[["Person", "Place", "Event", "Time"]]).values

# Combine embeddings
combined_embeddings = np.concatenate([text_embeddings, categorical_embeddings], axis=1)

print("Combined embeddings shape:", combined_embeddings.shape)


def generate_lifetime_dataset(n=50):
    data = []
    for _ in range(n):
        period = random.choice(life_periods)
        
        memory = (f"{period['Period']} ({period['Stage']}): "
                       f"Themes included {period['Themes']} primarily in {period['Location']} lasting {period['Duration']}. "
                       f"Overall emotional tone was {period['Emotion']}.")
        
        data.append([memory, period["Period"], period["Themes"], period["Location"], period["Duration"], period["Emotion"]])
        
    df = pd.DataFrame(data, columns=["Memory", "Period", "Themes", "Location", "Duration", "Emotion"])
    return df.sample(frac=1).reset_index(drop=True)

# Generate lifetime dataset explicitly aligned to Conway
dataset = generate_lifetime_dataset(50)