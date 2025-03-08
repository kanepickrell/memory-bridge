import ast
import base64
import json
import os
import random
import re
import io
from swarm import Swarm, Agent
import time
from MemoryManager import MemoryAccess
from voice import VoiceChat

client = Swarm()
vc = VoiceChat()

# MEMORY_FILE = "memory_bank.json"
MEMORY_FILE = "C:/repos/memory-bridge/frontend/src/data.json"
memorymap = MemoryAccess(MEMORY_FILE)

def load_memory():
    """Loads the memory bank JSON file into a Python dictionary."""
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as file:
            memory_bank = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        memory_bank = {"people": [], "events": [], "locations": []}  # Default structure

    return memory_bank

# Load memory at script start
memory_bank = load_memory()

def store_memory(new_memory):
    """
    Update the existing graph data JSON file with new memory nodes and links.
    """
    print(f"New Memory: {new_memory}")

    # Load current memory bank
    memory_bank = load_memory()

    # Ensure 'nodes' and 'links' keys exist
    if "nodes" not in memory_bank:
        memory_bank["nodes"] = []
    if "links" not in memory_bank:
        memory_bank["links"] = []

    # Append new nodes if not already present
    existing_node_ids = {node["id"] for node in memory_bank["nodes"]}
    for new_node in new_memory.get("nodes", []):
        if new_node["id"] not in existing_node_ids:
            memory_bank["nodes"].append(new_node)
            existing_node_ids.add(new_node["id"])

    # Append new links if not already present
    existing_links = {(link["source"], link["target"]) for link in memory_bank["links"]}
    for new_link in new_memory.get("links", []):
        link_tuple = (new_link["source"], new_link["target"])
        if link_tuple not in existing_links:
            memory_bank["links"].append(new_link)
            existing_links.add(link_tuple)

    # Save updated memory bank
    with open(MEMORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(memory_bank, file, indent=4, ensure_ascii=False)

    print("Memory successfully updated.")


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


agent_p = Agent(
    name="Agent P",
    instructions=f"""
    Agent Instructions: Memory Structuring, Updating, and Incremental JSON Completion

    Role:
    You are an advanced memory processing assistant for the Memory Bridge AI, designed to incrementally update an existing memory bank JSON with each new memory provided. You must:

    **1. Reference Existing Memory Bank:**
        - Begin by analyzing the provided memory.
        - Check existing entries to prevent duplication and maintain consistency.

    **Existing Memory Bank:**
    {json.dumps(memory_bank, indent=4)}

    ---
    **Incremental Memory Update Workflow:**

    **Step 1: Extract and Reference People:**
        - Extract names from the memory.
        - Check if each person already exists in the memory bank:
            - If yes, reference their existing "id".
            - If no, create a new entry with a unique "id".
        - Contextually determine relationships:
            - Family context → "Family" (e.g., "brother", "aunt")
            - Leisure/social context → "Friend"
            - Work-related → "Colleague"
            - Romantic context → "Partner"
            - Caregiving/mentorship context → "Mentor" or "Caregiver"
            - Default unclear context → "Acquaintance"
        - Assign or update "recall_strength" (0.0 - 1.0) based on emotional significance and frequency of mention.

    **Step 2: Extract and Reference Events:**
        - Identify if the event is new or references an existing event:
            - Create new events with unique IDs.
            - If the event already exists, reference the existing ID.
        - Extract and include details clearly:
            - Event date (if available)
            - Brief description
            - Tags ("travel", "family gathering", "work conference", etc.)
        - Link related people and locations with "recall_strength" (0.0 - 1.0).

    **Step 3: Extract and Reference Locations:**
        - Check existing locations to avoid duplication:
            - Create new entries with unique IDs if needed.
            - Include clear name and descriptions.
        - Assign "recall_strength" based on how clearly the location is recalled.

    **Step 4: Update Connections and Relationships Clearly:**
        - Create new connections between existing and new nodes (people, events, locations).
        - Ensure connections clearly represent relationships with appropriate recall strengths.

    **Step 5: Incremental Updates:**
        - Ensure all new information integrates seamlessly with the existing JSON structure.
        - Only modify existing entries to update recall_strength or add missing context.

    ---
    **Output Requirements:**
    - Produce **only valid JSON** reflecting the fully updated memory bank.
    - Do not provide any additional commentary or explanation.
    - Use existing IDs for known entities; generate new unique IDs for new entities.

    **Example Input Memory:**
    _"In 2005, I traveled to Japan with my cousin Emily and my college friend Jake. We explored Tokyo, and Jake kept talking about how he wanted to move there one day."_

    **Generated JSON Update Example:**
    {{
        "people": [
            {{
                "id": "p4",
                "name": "Emily",
                "relationship": "Cousin",
                "recall_strength": 0.9
            }},
            {{
                "id": "p5",
                "name": "Jake",
                "relationship": "Friend",
                "recall_strength": 0.8
            }}
        ],
        "events": [
            {{
                "id": "e5",
                "description": "Trip to Japan with Emily and Jake",
                "tags": ["travel", "friends"],
                "recall_strength": 0.9
            }}
        ],
        "locations": [
            {{
                "id": "l7",
                "name": "Tokyo, Japan",
                "description": "Capital city of Japan",
                "recall_strength": 0.9
            }}
        ],
        "connections": [
            {{ "source": "p4", "target": "e5", "recall_strength": 0.9 }},
            {{ "source": "p5", "target": "e5", "recall_strength": 0.8 }},
            {{ "source": "e5", "target": "l7", "recall_strength": 0.9 }}
        ]
    }}

    Ensure each memory prompt incrementally expands and accurately refines the memory bank.
    """
)


agent_a = Agent(
    name="Affirming Agent",
    instructions="Generate a verbally affirming response that would validate the response of a dementia patient participating in CST session",
)

agent_c = Agent(
    name="CST Agent",
    instructions="Follow a Cognitive Stimulation Therapy (CST) session script for a facillatator to follow that follows the protocols set by Spector 2001 and 2006",
)

agent_m = Agent(
    name="Memory Prompt Agent",
    instructions=f"""
    While continuing the conversation naturally, subtly give a memory prompt to a patient using Cognitive Stimulation Therapy (CST) session script for a facillatator to follow that follows the protocols set by Spector 2001 and 2006.

    You will recieve a selected memory and a user_input, if they are related, respond in a way that ties them together. 
    
    If they are not related, then respond to the user_input normally.

    """,
    function=[]
)

agent_t = Agent(
    name="Topical_Characterizing_Agent",
    instruction=""""
    Role:
    You are an agent meant to categorize conversation. 
    Instructions: Characterize the prompt that was provided as one of the following: negative or confused or normal
    
    Examples: 
    User: "No, I'm not sure, I don't remember, or curse words, etc"
    Classification: Negative 
    User: "No, I'm not sure, I don't remember, or curse words, etc"
    Classification: Confused 

    Output Format:
    Respond with only "Negative", "Confused", or "Normal", do not say anything further.
    """,
)

agent_v = Agent(
    name="Validation Agent",
    instructions="""
    You are a validation agent. Your task is to determine if the patient’s response affirms the memory prompt provided by the Memory Prompt Agent.
    Analyze the provided memory prompt and the patient’s response. 
    Respond with "Affirmed" if the response confirms or relates to the memory prompt, or "Not Affirmed" if it does not.
    """
)


negative_count = 0
confused_count = 0
normal_count = 0
conversational_flag = False
duration = 4 
fs = 44100   
voice_mode = 1

while True:

    if voice_mode == 1:
        audio = vc.record_audio(duration, fs)
        buffer = vc.audio_to_buffer(audio, fs)
        user_input = vc.transcribe_audio(buffer)
        print("You said:", user_input)

    else:
        user_input = input("Enter a statement (or type 'exit' to quit): ")

    selected_memory = memorymap.get_highest_recall_memories()
    print(selected_memory)
    selected_memory_text = ", ".join([m[1] for m in selected_memory]) if selected_memory else "No memory found"
    print(selected_memory_text) 

    
    # user_input = input("Enter a statement (or type 'exit' to quit): ")
    selected_memory = memorymap.get_highest_recall_memories()
    print(selected_memory)
    selected_memory_text = ", ".join([m[1] for m in selected_memory]) if selected_memory else "No memory found"
    # print(selected_memory_text) 

    if user_input.lower() == "exit":
        print("Exiting...")
        break

    # Run Agent S
    print("Running steering agent...")
    response_s = client.run(
        agent=agent_s,
        messages=[{"role": "user", "content": user_input}]
    )

    # Extract content from Agent S's response
    if response_s:
        classification = response_s.messages[-1]["content"]
        print(f"Agent S Classification: {classification}")

        # If Agent S classifies it as a memory, trigger Agent P
        if classification.strip().lower() == "memory":
            response_p = client.run(agent=agent_p, messages=[{"role": "user", "content": user_input}])

            if response_p and response_p.messages[-1]["content"]:
                try:
                    processed_memory = json.loads(response_p.messages[-1]["content"])
                    if isinstance(processed_memory, dict):
                        store_memory(processed_memory)
                    else:
                        print("Processed memory isn't a valid JSON object.")
                except json.JSONDecodeError:
                    print("Invalid JSON from Agent P.")

            # After running Agent M:
            print("Running Memory Agent...")
            response_m = client.run(
                agent=agent_m, 
                messages=[
                    {"role": "user", "content": user_input},
                    {"role": "system", "content": f"Selected memory: {selected_memory_text}"}
                ]
            )

            if response_m and response_m.messages:
                memory_prompt_output = response_m.messages[-1]['content']
                print(f"Memory Agent Response: {memory_prompt_output}")

                if voice_mode == 1:
                    audio = vc.record_audio(duration, fs)
                    buffer = vc.audio_to_buffer(audio, fs)
                    user_input = vc.transcribe_audio(buffer)
                    print("You said:", user_input)
                
                else:
                    # Ask the user for a follow-up response regarding the memory prompt.
                    validation_input = input("Enter a statement: ")
                    
                print("Running Validation Agent...")
                response_v = client.run(
                    agent=agent_v,
                    messages=[
                        {"role": "system", "content": f"Memory prompt: {memory_prompt_output}"},
                        {"role": "user", "content": validation_input},
                        
                    ],
                )
                
                if response_v and response_v.messages:
                    validation_result = response_v.messages[-1]['content']
                    print(f"Validation Agent Response: {validation_result}")
                    if validation_result == "Affirmed":
                        memorymap.increase_recall(selected_memory[0].id)
                else:
                    print("Validation Agent did not respond.")
            else:
                print("Memory Agent did not respond.")

        
        # If Agent S classifies it as a topical, trigger Agent 
        if classification.strip().lower() == "topical":
            response_t = client.run(
                agent=agent_t,
                messages=[{"role": "user", "content": user_input}]
            )
            print(f'Response T: {response_t.messages[-1]["content"]}')
            if response_t == "Negative":
                negative_count += 1
                if negative_count < 2:
                    response_m = client.run(
                        agent=agent_m,
                        messages=[{"role": "user", "content": "Beforehand patient has failed to recall a memory, provide an empathetic response"}],
            )
                else:
                    conversational_flag = True

            if response_t == "Confused":
                confused_count += 1
                if confused_count < 2:
                    response_m = client.run(
                        agent=agent_m,
                        messages=[{"role": "user", "content": "Beforehand patient has failed to recall a memory, provide an empathetic response"}],
            )
                else:
                    conversational_flag = True

            if response_t == "Normal":
                normal_count += 1
                if not conversational_flag: 
                    response_m = client.run(
                        agent=agent_m,
                        messages=[{"role": "user", "content": "Beforehand patient has failed to recall a memory, provide an empathetic response"}],
                    )

            

    else:
        print("Error: No valid response from Agent X.")





