import json
import asyncio
from datetime import datetime
from swarm import Swarm, Agent

# SessionAggregator Class remains similar
class SessionAggregator:
    def __init__(self, session_id, patient_id):
        self.data = {
            "session_id": session_id,
            "patient_id": patient_id,
            "start_time": datetime.utcnow().isoformat() + "Z",
            "end_time": None,
            "overall_session_type": "Mixed",
            "mood": [],
            "dialogue_segments": [],
            "dynamic_adjustments": [],
            "session_summary": {}
        }

    def add_dialogue_segment(self, segment):
        self.data["dialogue_segments"].append(segment)

    def add_dynamic_adjustment(self, adjustment):
        self.data["dynamic_adjustments"].append(adjustment)

    def set_end_time(self):
        self.data["end_time"] = datetime.utcnow().isoformat() + "Z"

    def update_session_summary(self, summary):
        self.data["session_summary"] = summary

    def update_mood(self, mood):
        if isinstance(mood, str):
            self.data["mood"] = [m.strip() for m in mood.split(",")]
        elif isinstance(mood, list):
            self.data["mood"] = mood
        else:
            raise ValueError("Mood must be a string or list of strings.")

    def get_session_data(self):
        return self.data

# Helper function to append session logs asynchronously (simulate I/O-bound work)
async def append_session_log(new_session_data, session_log_path="data/session_log.json"):
    # In a production system, consider using an async file I/O library (e.g., aiofiles)
    try:
        with open(session_log_path, 'r', encoding='utf-8') as file:
            session_log = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        session_log = {}

    if "sessions" not in session_log or not isinstance(session_log["sessions"], list):
        session_log["sessions"] = []

    session_log["sessions"].append(new_session_data)

    with open(session_log_path, 'w', encoding='utf-8') as file:
        json.dump(session_log, file, indent=4, ensure_ascii=False)

    return "Session log updated successfully."

# TherapyAgents class remains largely the same with defined agents.
class TherapyAgents:
    def __init__(self):
        self.client = Swarm()
        self.agents = {}
        self.initialize_agents()
    
    def reminiscence():
        # Stub for reminiscence therapy
        pass

    def narrative():
        # Stub for narrative therapy
        pass

    def adaptive_feedback():
        # Stub for adaptive feedback
        pass

    def initialize_agents(self):
        self.agents['steering_agent'] = Agent(
            name="Agent S",
            instructions="""
            You are an expert in memory therapy and understand when to apply spaced retrieval therapy (SRT)
            or multi-modal therapy (MULTI). Classify user input as 'SRT' or 'MULTI'.
            """
        )

        self.agents['srt_agent'] = Agent(
            name="Spaced Retrieval Therapy Agent",
            instructions="""
            Role:
            You are an expert in SRT, conducting personalized memory training sessions.
            Responsibilities:
            - Select meaningful memory targets.
            - Prompt immediate repetition with errorless learning.
            - Maintain a relaxed, positive conversation.
            Output Format:
            - Respond clearly and conversationally.
            - If successful, respond with "COMPLETE".
            """
        )

        self.agents['multi_agent'] = Agent(
            name="Multi-Modal Therapy Agent",
            instructions="""
            Role:
            Facilitate personalized multi-modal sessions combining various therapies.
            Responsibilities:
            - Provide orientation cues and ask engaging questions.
            - Adapt dynamically based on patient responses.
            Output Format:
            - Respond with conversational prompts.
            - When done, respond with "COMPLETE".
            """
        )

        self.agents['mood_detection_agent'] = Agent(
            name="Mood Detection Agent",
            instructions="""
            Role:
            Analyze patient conversations to summarize mood using descriptive keywords.
            Output Format:
            - Return mood keywords as a comma-separated string.
            """
        )

        self.agents['therapeutic_progress_analyzer'] = Agent(name="Therapeutic Progress Analyzer", instructions="")
        self.agents['caregiver_agent'] = Agent(
            name="Caregiver Agent", 
            instructions="""
            Role:
            Review the patient's session.
            Responsibilities:
            - Summarize the session.
            - Provide clinician-relevant feedback.
            Output Format:
            - Return a summary report.
            """
        )
        self.agents['personalization_agent'] = Agent(
            name="Personalization Agent", 
            instructions="""
            Role:
            Analyze session history to extract insights for future sessions.
            Responsibilities:
            - Update patient profiles.
            - Extract themes or preferences.
            Output Format:
            - Return a concise update report.
            """
        )

    def get_agent(self, agent_name):
        return self.agents.get(agent_name)

# Load previous session summary synchronously for now (could also be async if needed)
def load_previous_session_summary(patient_id, session_log_path="data/session_log.json"):
    try:
        with open(session_log_path, 'r', encoding='utf-8') as file:
            session_log = json.load(file)
        sessions = session_log.get("sessions", [])
        for session in reversed(sessions):
            if session["patient_id"] == patient_id:
                return session["session_summary"].get("clinician_recommendation")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None
    return None

# A helper function to simulate asynchronous user input.
# In a real-world scenario, this might be an HTTP request or websocket event.
async def get_patient_response():
    # For the prototype, run input() in a separate thread to avoid blocking the event loop.
    response = await asyncio.to_thread(input, "Patient Response: ")
    return response

# Session class with asynchronous patient engagement
class Session:
    def __init__(self, therapy_agents):
        self.client = therapy_agents.client
        self.agents = therapy_agents.agents

    async def engage_patient(self, patient_prompt, patient_id="patient_1"):
        aggregator = SessionAggregator(
            session_id=f"session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            patient_id=patient_id
        )

        history = [{"role": "user", "content": patient_prompt}]

        # Inject previous session context if available
        previous_summary = load_previous_session_summary(patient_id)
        if previous_summary:
            context_message = {"role": "system", "content": f"Previous session summary: {previous_summary}"}
            history.insert(0, context_message)

        last_index = len(history)

        # Steering Agent classifies therapy type
        steering_response = await asyncio.to_thread(self.client.run, self.agents['steering_agent'], history)
        classification = steering_response.messages[-1]['content'].strip()
        print(f"Steering Classification: {classification}")

        agent_name = 'multi_agent' if classification == "MULTI" else 'srt_agent'

        segment_counter = 1
        session_complete = False

        # Main session loop implemented asynchronously
        while not session_complete:
            # Run the selected therapy agent
            response = await asyncio.to_thread(self.client.run, self.agents[agent_name], history)
            agent_reply = response.messages[-1]['content'].strip()
            print(f"{agent_name.upper()}: {agent_reply}")

            new_messages = history[last_index:]
            last_index = len(history)

            segment = {
                "segment_id": segment_counter,
                "modality": agent_name,
                "start_time": datetime.utcnow().isoformat() + "Z",
                "end_time": datetime.utcnow().isoformat() + "Z",
                "transcript": new_messages,
                "emotional_cues": {},
                "agent_decisions": f"{agent_name} processed."
            }
            aggregator.add_dialogue_segment(segment)
            segment_counter += 1

            if agent_reply == "COMPLETE":
                session_complete = True
            else:
                history.append({"role": "assistant", "content": agent_reply})
                # Await asynchronous patient response from the front-end layer
                patient_response = await get_patient_response()
                history.append({"role": "user", "content": patient_response})

        # Post-session processing
        mood_analysis = await asyncio.to_thread(self.client.run, self.agents['mood_detection_agent'], history)
        mood = mood_analysis.messages[-1]['content'].strip()
        aggregator.update_mood(mood)

        caregiver_summary = await asyncio.to_thread(self.client.run, self.agents['caregiver_agent'], history)
        c_summary = caregiver_summary.messages[-1]['content'].strip()
        print(f"Caregiver Summary: {c_summary}")

        summary = {
            "overall_sentiment": mood,
            "key_memory_recall_success": "N/A, to be evaluated",
            "notes": "Session completed; patient engaged.",
            "clinician_recommendation": c_summary
        }

        aggregator.update_session_summary(summary)
        aggregator.set_end_time()

        # Asynchronously update the session log (simulate I/O-bound operation)
        append_result = await append_session_log(aggregator.get_session_data())
        print(append_result)

        personalization_update = await asyncio.to_thread(self.client.run, self.agents['personalization_agent'], history)
        therapeutic_progress = await asyncio.to_thread(self.client.run, self.agents['therapeutic_progress_analyzer'], history)

        return "Session COMPLETE"

# Main entry point for backend session orchestration
# This main function can be triggered by a front-end interface, for example via an API endpoint.
async def main():
    therapy_agents = TherapyAgents()
    session = Session(therapy_agents)
    difficult_prompt = "I used to go fishing somewhere important, but I can't remember who I went with. Can you help me?"
    print(f"Difficult Prompt: {difficult_prompt}")
    response = await session.engage_patient(difficult_prompt, patient_id="patient_1")
    print(f"Final Response: {response}")

# Entry point for asynchronous execution
if __name__ == "__main__":
    asyncio.run(main())
