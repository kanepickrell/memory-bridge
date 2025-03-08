from swarm import Swarm, Agent
import json

class TherapyAgents:
    def __init__(self, memory_bank_path):
        self.client = Swarm()
        self.memory_bank_path = memory_bank_path
        self.memory_bank = self.load_memory()
        self.agents = {}
        self.initialize_agents()

    def load_memory(self):
        try:
            with open(self.memory_bank_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"people": [], "events": [], "locations": []}

    def initialize_agents(self):
        self.agents['steering_agent'] = Agent(
            name="Agent S",
            instructions="""
            You are an expert in memory therapy and understand when to apply spaced retrieval therapy (SRT) or cognitive stimulation therapy (CST).
            Classify user input as 'SRT' or 'CST'.
            """
        )

        self.agents['srt_agent'] = Agent(
            name="Spaced Retrieval Therapy Agent",
            instructions="""
            Role:
            You are an expert in Spaced Retrieval Therapy (SRT) conducting personalized, one-on-one reminiscence and memory training sessions tailored specifically for individuals with early-stage Alzheimer's disease. Your primary goal is to assist participants in reliably recalling essential personal information, daily routines, or specific tasks through structured repetition at progressively longer intervals.

            Responsibilities:
            - Select clear, personally meaningful targets for spaced retrieval practice.
            - Clearly state the memory target initially. Prompt immediate repetition.
            - Conduct recall prompts at progressively longer intervals, utilizing errorless learning.
            - Engage in relaxed, positive conversations between intervals.
            - Maintain positivity, empathy, and reassurance.
            - Adapt dynamically based on engagement.

            Output Format:
            - Respond clearly and conversationally.
            - Explicitly state the correct answer on incorrect responses.
            - When the task succeeds, ONLY respond with "COMPLETE".
            """
        )

        self.agents['cst_agent'] = Agent(
            name="Cognitive Stimulation Therapy",
            instructions="""
            Role:
            You facilitate personalized, one-on-one CST sessions for early-stage Alzheimer's patients, fostering meaningful conversation and cognitive engagement.

            Responsibilities:
            - Provide orientation cues.
            - Introduce clear themes.
            - Engage participants with personalized questions.
            - Maintain positivity and empathy.
            - Provide gentle cues when needed.
            - Adapt to signs of frustration or fatigue.

            Output Format:
            - Respond exclusively with relevant conversational questions or statements.
            - Upon successful completion or fatigue, ONLY respond with "COMPLETE".
            """
        )

        # Placeholder agents
        self.agents['mood_detection_agent'] = Agent(name="Mood Detection Agent", instructions="")
        self.agents['therapeutic_progress_analyzer'] = Agent(name="Therapeutic Progress Analyzer", instructions="")
        self.agents['caregiver_agent'] = Agent(name="Caregiver Agent", instructions="")
        self.agents['personalization_agent'] = Agent(name="Personalization Agent", instructions="")


class Session():
    def __init__(self, therapy_agents):
        self.client = therapy_agents.client
        self.agents = therapy_agents.agents
        self.memory_bank = therapy_agents.memory_bank

    def get_agent(self, agent_name):
        return self.agents.get(agent_name)

    def handle_patient_prompt(self, patient_prompt):
        initial_message = {"role": "user", "content": patient_prompt}
        history = [initial_message]

        steering_response = self.client.run(
            agent=self.get_agent('steering_agent'),
            messages=history
        )
        classification = steering_response.messages[-1]['content'].strip()
        print(f"Steering Agent Classification: {classification}")

        if classification == "CST":
            agent_name = 'cst_agent'
        else:
            agent_name = 'srt_agent'

        session_complete = False
        while not session_complete:
            therapy_response = self.client.run(
                agent=self.get_agent(agent_name),
                messages=history
            )
            agent_reply = therapy_response.messages[-1]['content'].strip()
            print(f"{agent_name.upper()}: {agent_reply}")

            if agent_reply == "COMPLETE":
                session_complete = True
            else:
                history.append({"role": "assistant", "content": agent_reply})
                patient_prompt = input("Provide User Response: ")
                history.append({"role": "user", "content": patient_prompt})

        # Placeholder for feedback loop
        # mood analysis could compile voice condition and pitch to assist in mood prediction as well as responses
        mood_analysis = self.client.run(agent=self.get_agent('mood_detection_agent'), messages=history, functions=[])

        # therepeutic progrees could run a diagnostic on the memory map for weak clusters
        therapeutic_progress = self.client.run(agent=self.get_agent('therapeutic_progress_analyzer'), messages=history)

        # reviews and provides summary of patient state
        caregiver_summary = self.client.run(agent=self.get_agent('caregiver_agent'), messages=history)

        # 
        personalization_update = self.client.run(agent=self.get_agent('personalization_agent'), messages=history)

        # Store conversation in memory bank (simplified)
        self.memory_bank['conversation_history'] = history

        return "Session COMPLETE"


if __name__ == "__main__":
    memory_bank_path = "C:/repos/memory-bridge/frontend/src/data.json"
    therapy_agents = TherapyAgents(memory_bank_path)
    session = Session(therapy_agents)

    difficult_prompt = "Why are we even talking about this stuff? It's boring, and I don’t see how this helps me. I'd rather just sit quietly."
    print(f"Difficult Prompt: {difficult_prompt}")
    response = session.handle_patient_prompt(difficult_prompt)
    print(f"Final Response to Patient: {response}")
