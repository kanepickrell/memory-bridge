import json
from datetime import datetime
from swarm import Swarm, Agent

# SessionAggregator Class
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

# Helper function to append session logs
def append_session_log(new_session_data, session_log_path="data/session_log.json"):
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

# TherapyAgents class remains largely unchanged
class TherapyAgents:
    def __init__(self):
        self.client = Swarm()
        self.agents = {}
        self.initialize_agents()
    
    def reminiscence():
        """
        Reminiscence Therapy Tool
        This function implements the reminiscence therapy module. It is designed to evoke and stimulate
        memories from the patient's past by using multimodal stimuli (e.g., personal photos, music, videos)
        along with targeted prompts. The goal is to create a comfortable environment that encourages the
        patient to recall personal experiences and share details about them.
        Responsibilities:
        - Present multimedia cues tailored to the patient's personal history.
        - Ask open-ended, emotionally engaging questions to trigger autobiographical recall.
        - Adapt prompts dynamically based on real-time feedback.
        This tool is called by the Multi-Modal Therapy Agent when deeper emotional engagement is required.
        """
        pass

    def narrative():
        """
        Narrative Therapy Tool
        This function implements the narrative therapy module, aimed at facilitating structured storytelling
        and life history construction. It helps the patient organize memories into a coherent narrative that
        reinforces their identity and adds personal meaning.
        Responsibilities:
        - Guide the patient in creating a timeline of significant life events.
        - Ask follow-up questions to enrich the narrative with details and emotional context.
        - Store and structure narrative elements for later review and future session tailoring.
        This tool is activated during personal storytelling and life review.
        """
        pass

    def adaptive_feedback():
        """
        Adaptive Feedback Tool
        This function implements the adaptive feedback mechanism for memory therapy sessions.
        It continuously analyzes the patient's responses using metrics (e.g., sentiment, engagement, accuracy)
        and provides tailored, real-time feedback to support and adjust the therapeutic process.
        Responsibilities:
        - Monitor emotional cues and cognitive performance.
        - Deliver positive reinforcement and gentle corrective prompts.
        - Trigger modality switches if signs of frustration or fatigue are detected.
        - Log feedback actions and adjustments for continuous session improvement.
        This tool ensures sessions remain dynamic and responsive, emulating a compassionate caregiver.
        """
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
            name="Multi-Model Therapy",
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
            """,
            functions=[]
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
            """,
            functions=[]
        )

        self.agents['therapeutic_progress_analyzer'] = Agent(name="Therapeutic Progress Analyzer", instructions="")
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

# Load previous session summary
def load_previous_session_summary(patient_id, session_log_path="data/session_log.json"):
    try:
        with open(session_log_path, 'r', encoding='utf-8') as file:
            session_log = json.load(file)
        sessions = session_log.get("sessions", [])
        for session in reversed(sessions):
            if session["patient_id"] == patient_id:
                return session["session_summary"]["clinician_recommendation"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None
    return None

class Session:
    def __init__(self, therapy_agents):
        self.client = therapy_agents.client
        self.agents = therapy_agents.agents

    def engage_patient(self, patient_prompt, patient_id="patient_1"):
        aggregator = SessionAggregator(session_id=f"session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}", patient_id=patient_id)

        history = [{"role": "user", "content": patient_prompt}]

        # Inject previous session context
        previous_summary = load_previous_session_summary(patient_id)
        if previous_summary:
            context_message = {"role": "system", "content": f"Previous session summary: {previous_summary}"}
            history.insert(0, context_message)

        last_index = len(history)

        # Steering Agent chooses therapy type
        steering_response = self.client.run(self.agents['steering_agent'], history)
        classification = steering_response.messages[-1]['content'].strip()
        print(f"Steering Classification: {classification}")

        agent_name = 'multi_agent' if classification == "MULTI" else 'srt_agent'

        segment_counter = 1
        session_complete = False

        while not session_complete:
            response = self.client.run(self.agents[agent_name], history)
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
                patient_response = input("Patient Response: ")
                history.append({"role": "user", "content": patient_response})

        mood_analysis = self.client.run(self.agents['mood_detection_agent'], history)
        mood = mood_analysis.messages[-1]['content'].strip()
        aggregator.update_mood(mood)

        caregiver_summary = self.client.run(self.agents['caregiver_agent'], history)
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

        append_result = append_session_log(aggregator.get_session_data())
        print(append_result)

        personalization_update = self.client.run(self.agents['personalization_agent'], history)
        therapeutic_progress = self.client.run(self.agents['therapeutic_progress_analyzer'], history)

        return "Session COMPLETE"

# Main entry
if __name__ == "__main__":
    therapy_agents = TherapyAgents()
    session = Session(therapy_agents)

    difficult_prompt = "I used to go fishing somewhere important, but I can't remember who i went with. Can you help me?"
    print(f"Difficult Prompt: {difficult_prompt}")

    response = session.engage_patient(difficult_prompt, patient_id="patient_1")
    print(f"Final Response: {response}")
