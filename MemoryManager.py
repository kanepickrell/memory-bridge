import json
from pprint import pprint
from collections import namedtuple
from fuzzywuzzy import fuzz

# Define namedtuples
Person = namedtuple("Person", ["id", "name", "age", "relationship", "description", "tags", "recall_strength"])
Event = namedtuple("Event",["id", "date", "related_people", "description", "tags", "related_places", "recall_strength"])
Location = namedtuple("Location", ["id", "name", "address", "description", "recall_strength"])


class MemoryAccess:
    def __init__(self, filename):
        self.filename = filename
        self.people = []
        self.events = []
        self.locations = []
        self.load_data()

    def load_data(self):
        with open(self.filename, "r") as file:
            data = json.load(file)

        self.people = [Person(**person) for person in data.get("people", [])]
        self.events = [Event(**event) for event in data.get("events", [])]
        self.locations = [Location(**location) for location in data.get("locations", [])]

    def get_people(self):
        return self.people

    def get_events(self):
        return self.events

    def get_locations(self):
        return self.locations

    def update_recall_strength(self, element_id, increment=0.1):
        self.people = [p._replace(recall_strength=min(1.0, p.recall_strength + increment)) if p.id == element_id else p for p in self.people]
        self.events = [e._replace(recall_strength=min(1.0, e.recall_strength + increment)) if e.id == element_id else e for e in self.events]
        self.locations = [l._replace(recall_strength=min(1.0, l.recall_strength + increment)) if l.id == element_id else l for l in self.locations]

    def add_person(self, id, name, age, relationship, description, tags, recall_strength=0.5):
        self.people.append(Person(id, name, age, relationship, description, tags, recall_strength))

    def add_event(self, id, date, related_people, description, tags, related_places, recall_strength=0.5):
        for person_id, _ in related_people:
            self.update_recall_strength(person_id)
        for location_id, _ in related_places:
            self.update_recall_strength(location_id)
        self.events.append(Event(id, date, related_people, description, tags, related_places, recall_strength))

    def add_location(self, id, name, address, description, recall_strength=0.5):
        self.locations.append(Location(id, name, address, description, recall_strength))

    def fuzzy_search_people(self, query, threshold=80):
        return [person for person in self.people if fuzz.partial_ratio(query.lower(), person.name.lower()) >= threshold]

    def fuzzy_search_events(self, query, threshold=80):
        return [event for event in self.events if fuzz.partial_ratio(query.lower(), event.description.lower()) >= threshold]

    def fuzzy_search_locations(self, query, threshold=80):
        return [location for location in self.locations if fuzz.partial_ratio(query.lower(), location.name.lower()) >= threshold]


if __name__ == "__main__":
    json_filename = "MemoryFiles/MemoryFileV2.json"  # Replace with the actual JSON filename
    memory_map = MemoryAccess(json_filename)

    print("People:", memory_map.get_people())
    print("Events:", memory_map.get_events())
    print("Locations:", memory_map.get_locations())




    query = "John"
    print("Fuzzy search people:", memory_map.fuzzy_search_people(query))
    query = "Canyon"
    print("Fuzzy search events:", memory_map.fuzzy_search_events(query))
    query = "Canion"
    print("Fuzzy search locations:", memory_map.fuzzy_search_locations(query))
