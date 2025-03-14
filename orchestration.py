import json
import asyncio
from datetime import datetime
from swarm import Swarm, Agent

# -------------------------------------
# SessionAggregator Class
# -------------------------------------
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

# -------------------------------------
# Helper to append session logs
# -------------------------------------
async def append_session_log(new_session_data, session_log_path="data/session_log.json"):
    try:
        with open(session_log_path, 'r', encoding='utf-8') as file:
            session_log = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        session_log = {}

    if "sessions" not in session_log or not isinstance(session_log.get("sessions"), list):
        session_log["sessions"] = []

    session_log["sessions"].append(new_session_data)

    with open(session_log_path, 'w', encoding='utf-8') as file:
        json.dump(session_log, file, indent=4, ensure_ascii=False)

    return "Session log updated successfully."

# -------------------------------------
# TherapyAgents class
# -------------------------------------
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
            or multi-modal therapy (MULTI). Multi-modal therapy includes CST, Reminiscence Therapy, Narrative Therapy,
            and Recall Therapy. Classify user input as 'SRT' or 'MULTI'.
            """
        )

        self.agents['srt_agent'] = Agent(
            name="Spaced Retrieval Therapy Agent",
            instructions="""
            Role:
            You are an expert in SRT, conducting personalized memory training sessions for early-stage Alzheimer's patients.

            Responsibilities:
            - Select meaningful memory targets for spaced retrieval.
            - Prompt immediate repetition and conduct recall prompts with errorless learning.
            - Maintain a relaxed, positive conversation and adapt dynamically.

            Output Format:
            - Respond clearly and conversationally.
            - If successful, respond with "COMPLETE".
            """
        )

        self.agents['multi_agent'] = Agent(
            name="Multi-Modal Therapy Agent",
            instructions="""
            Role:
            You facilitate personalized multi-modal sessions for early-stage Alzheimer's patients, combining CST, 
            Reminiscence, Narrative, and other therapies.

            Responsibilities:
            - Provide orientation cues and introduce clear themes.
            - Engage with personalized questions and maintain positivity.



            - Adapt to signs of frustration or fatigue.

            Output Format:
            - Respond with conversational questions or statements.
            - When complete with the activity or patient is finished, ONLY respond with "COMPLETE".
            """
        )

        self.agents['mood_detection_agent'] = Agent(
            name="Mood Detection Agent",
            instructions="""
            Role:
            Analyze patient conversations and summarize mood using descriptive keywords.
            Responsibilities:
            - Identify keywords (e.g., frustrated, happy, anxious, calm).

            Output Format:
            - Return mood keywords as a list of strings, e.g., "frustrated, anxious".
            """
        )

        self.agents['therapeutic_progress_analyzer'] = Agent(
            name="Therapeutic Progress Analyzer",
            instructions=""
        )

        self.agents['caregiver_agent'] = Agent(
            name="Caregiver Agent", 
            instructions="""
            Role:
            You are a seasoned memory care expert who reviews the patient's session.
            Responsibilities:
            - Summarize the session.
            - Provide clinician-relevant feedback and recommendations.
            Output Format:
            - Return a summary report.
            """
        )
        self.agents['personalization_agent'] = Agent(
            name="Personalization Agent", 
            instructions="""
            Role:
            Analyze session history to extract key personal insights for future sessions.
            Responsibilities:
            - Update patient profiles with new data points.
            - Extract themes or preferences from the conversation.
            Output Format:
            - Return a concise update report.
            """
        )

    def get_agent(self, agent_name):
        return self.agents.get(agent_name)

# -------------------------------------
# Optional: Load previous session summary
# -------------------------------------
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

# -------------------------------------
# (Optional) simulate asynchronous user input
# -------------------------------------
async def get_patient_response():
    # In a real system, you'd get the user input from an API or front-end
    response = await asyncio.to_thread(input, "Patient Response: ")
    return response

# -------------------------------------
# Session class
# -------------------------------------
class Session:
    def __init__(self, therapy_agents):
        self.client = therapy_agents.client
        self.agents = therapy_agents.agents

    async def engage_patient(self, patient_prompt, patient_id="patient_1"):
        """
        Demonstration method that:
        1. Generates 3 responses from 'srt_agent'
        2. Stores them in the aggregator
        3. Hard-codes a chosen response
        4. Logs everything to session_log.json
        """
        # Create aggregator
        aggregator = SessionAggregator(
            session_id=f"session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            patient_id=patient_id
        )

        # In a real system, you might run the steering agent to decide 'srt_agent' vs. 'multi_agent'.
        agent_name = "srt_agent"
        prompt = patient_prompt

        # 1) Generate multiple responses
        responses = await self.generate_multiple_responses(agent_name, prompt, num_responses=3)

        # 2) Store them in aggregator as a single segment
        multiple_responses_segment = {
            "segment_id": 1,
            "modality": agent_name,
            "start_time": datetime.utcnow().isoformat() + "Z",
            "end_time": datetime.utcnow().isoformat() + "Z",
            "prompt": prompt,
            "candidate_responses": [
                {"response_id": f"res{i+1}", "text": resp}
                for i, resp in enumerate(responses)
            ],
            "chosen_response": None,
            "agent_decisions": f"{agent_name} generated multiple responses."
        }
        aggregator.add_dialogue_segment(multiple_responses_segment)

        # 3) Suppose the user or front-end picks a top response
        chosen_response_id = "res2"  # Hard-coded for demonstration
        multiple_responses_segment["chosen_response"] = chosen_response_id

        # 4) Wrap up session
        aggregator.set_end_time()
        append_result = await append_session_log(aggregator.get_session_data())
        print(append_result)

        return "Session COMPLETE"

    async def generate_multiple_responses(self, agent_name: str, prompt: str, num_responses=3):
        """
        Runs the same agent multiple times to produce distinct responses.
        Alternatively, you could instruct one agent to produce multiple variations 
        in a single prompt, or use multiple agents.
        """
        responses = []
        for _ in range(num_responses):
            history = [{"role": "user", "content": prompt}]
            response = await asyncio.to_thread(self.client.run, self.agents[agent_name], history)
            agent_reply = response.messages[-1]['content'].strip()
            responses.append(agent_reply)
        return responses

# -------------------------------------
# Main entry point
# -------------------------------------
async def main():
    therapy_agents = TherapyAgents()
    session = Session(therapy_agents)
    prompt = "I used to go fishing somewhere important, but I can't remember who I went with."
    result = await session.engage_patient(prompt, "patient_1")
    print("Local test result:", result)

if __name__ == "__main__":
    asyncio.run(main())
