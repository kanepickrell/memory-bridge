import ast
import base64
import json
import os
import random
import re
import io
from swarm import Swarm, Agent
import time

client = Swarm()

print("Running steering agent...")
agent_s = Agent(
    name="Agent S",
    instructions="""
        Role: 
        You are a patient caretaker at a memory care facility, specializing in assisting individuals with cognitive impairments. Your primary task is to determine whether a given user response describes a personal memory or is simply a topical conversation response that does not reference a past experience.

        Guidelines:
        A memory typically includes references to past events, personal experiences, or emotions tied to a specific time or place.
        A topical conversation response focuses on general discussion, opinions, or facts without indicating a personal recollection.
        
        Example Classifications:
        User: "I remember going to the beach with my family when I was a kid. The sand was so hot!"
        Classification: Memory
        User: "Beaches are usually crowded during summer."
        Classification: Topical 

        Output Format:
        Respond with either "Memory" or "Topical", do not say anything further.
    """,
    functions=[]
)

# response_x = client.run(
#     agent=agent_x,
#     messages=[{"role": "user", "content": "its currently 3 o clock."}]
# )

# print(response_x.messages[-1]["content"])


print("Running memory preprocessing agent...")
agent_p = Agent(
    name="Agent P",
    instructions="""
    Agent Instructions: Memory Structuring and JSON Completion
    Role:
    You are an advanced memory processing assistant. Your job is to analyze a provided memory and integrate it into a structured JSON memory bank. You will extract relevant information, map relationships, and ensure completeness while maintaining the JSON format.

    Task Breakdown
    Identify Key People:

    Extract names from the memory and determine their relationship to the user.
    If the person exists in the memory bank, reference their id. If they are new, create a new entry.
    Assign descriptions, tags, and a recall strength (0 to 1.0) based on relevance and frequency.
    Identify Events:

    Determine whether the memory describes a new event or references an existing event.
    Capture details such as date, related people, description, and tags.
    Link related people and locations with a recall confidence score (0.0 - 1.0).
    Assign an event recall strength based on specificity and importance.
    Identify Locations:

    If a place is mentioned, determine if it exists in the memory bank.
    If new, create a new entry with an id, name, address, and description.
    Assign a recall strength (0.0 - 1.0) based on memory clarity.
    Example Memory Processing
    Input Memory:
    "Last summer, I went hiking at the Grand Canyon with my best friend Mike. It was an incredible experience! We watched the sunset and took amazing photos. I remember Mike talking about his dream of becoming a travel photographer."

    Generated JSON Update:
    json
    Copy
    Edit
    {
    "people": [
        {
        "id": "p3",
        "name": "Mike",
        "age": 32,
        "relationship": "Best Friend",
        "description": "A close friend who enjoys travel and photography.",
        "tags": ["friend", "travel", "photography", "hiking"],
        "recall_strength": 0.87
        }
    ],
    "events": [
        {
        "id": "e3",
        "date": "2024-07-10",
        "related_people": [["p3", 0.95]],
        "description": "A hiking trip to the Grand Canyon with Mike. We watched the sunset and took amazing photos.",
        "tags": ["hiking", "trip", "sunset", "photography"],
        "related_places": [["l1", 1.0]],
        "recall_strength": 0.83
        }
    ]
    }
    Output Format:
    Always return valid JSON.
    Ensure that existing IDs are used when possible to avoid duplication.
    New entities (people, events, locations) must have unique IDs.
    Recall strength should be estimated based on how vivid and clear the memory is.
    """,
    functions=[]
)

while True:
    user_input = input("Enter a statement (or type 'exit' to quit): ")

    if user_input.lower() == "exit":
        print("Exiting...")
        break

    # response_x = client.run(
    # agent=agent_x,
    # messages=[{"role": "user", "content": "its currently 3 o clock."}]
    # )

    # Run Agent X
    response_s = client.run(
        agent=agent_s,
        messages=[{"role": "user", "content": user_input}]
    )

    # print(response_x.messages[-1]["content"])

    # Extract content from Agent X's response
    if response_s:
        classification = response_s.messages[-1]["content"]
        print(f"Agent X Classification: {classification}")

        # If Agent X classifies it as a memory, trigger Agent Y
        if classification.strip().lower() == "memory":
            print("Memory detected! Triggering Agent Y...")
            response_p = client.run(
                agent=agent_p,
                messages=[{"role": "user", "content": "Tell me a joke"}]
            )

            # Extract and print Agent Y's response
            if response_p:
                joke = response_p.messages[-1]["content"]
                print(f"Agent Y response: {joke}")
        else:
            print("No memory detected. Try again.")
    else:
        print("Error: No valid response from Agent X.")


