import asyncio
from swarm import Swarm, Agent

class MemoryTherapyRL:
    def __init__(self):
        self.client = Swarm()
        # Initialize three agents with different instructions for memory therapy
        self.agents = {
            "agent_1": Agent(
                name="Memory Agent 1",
                instructions="""
                Role: You are a memory therapist.
                Approach: Focus on detailed recollection of specific events.
                When asked, provide detailed prompts to help the patient recall specific memories.
                """
            ),
            "agent_2": Agent(
                name="Memory Agent 2",
                instructions="""
                Role: You are a memory therapist.
                Approach: Focus on the emotional aspects of memories.
                When asked, guide the patient to explore feelings and emotional cues from their past.
                """
            ),
            "agent_3": Agent(
                name="Memory Agent 3",
                instructions="""
                Role: You are a memory therapist.
                Approach: Combine cognitive and narrative techniques.
                When asked, blend detailed recollection with a focus on storytelling to help the patient reconstruct memories.
                """
            )
        }
        # A simple reward store for each agent
        self.agent_rewards = { "agent_1": 0, "agent_2": 0, "agent_3": 0 }
    
    async def get_agent_response(self, agent, prompt):
        # Each agent is given the same prompt to generate its response.
        # The conversation history is a simple list with the patient prompt.
        history = [{"role": "user", "content": prompt}]
        response = await asyncio.to_thread(self.client.run, agent, history)
        return response.messages[-1]['content'].strip()
    
    async def generate_responses(self, prompt):
        responses = {}
        for key, agent in self.agents.items():
            responses[key] = await self.get_agent_response(agent, prompt)
        return responses

    def update_agent_instructions(self, chosen_agent_key):
        """
        A simple reinforcement update:
        - The chosen agent receives a positive reward.
        - The other agents are penalized.
        - We simulate "learning" by appending a note to the instructions.
        """
        for key in self.agents:
            if key == chosen_agent_key:
                self.agent_rewards[key] += 1
                # Append positive reinforcement to the chosen agent's instructions.
                self.agents[key].instructions += "\n[Reinforcement Update]: Your responses have been highly effective. Continue emphasizing clarity and detail."
            else:
                self.agent_rewards[key] -= 1
                # Suggest improvements for less effective agents.
                self.agents[key].instructions += "\n[Reinforcement Update]: Consider increasing focus on detailed memory cues."
        print("Updated rewards:", self.agent_rewards)
    
    async def run_reinforcement_cycle(self, prompt):
        # Generate responses from all agents
        responses = await self.generate_responses(prompt)
        print("Agent Responses:")
        for key, response in responses.items():
            print(f"{key}: {response}\n")
        
        # Ask the user to choose the best response
        chosen_agent = input("Enter the key (agent_1, agent_2, or agent_3) for the best response: ").strip()
        if chosen_agent not in self.agents:
            print("Invalid choice. No update performed.")
        else:
            self.update_agent_instructions(chosen_agent)
        return responses

# Example main loop
async def main():
    memory_rl_system = MemoryTherapyRL()
    # Example prompt from a patient
    prompt = "I find it hard to remember the details of my childhood. Can you help me recall some important moments?"
    responses = await memory_rl_system.run_reinforcement_cycle(prompt)
    
    # Display updated instructions for each agent
    print("\nUpdated Agent Instructions:")
    for key, agent in memory_rl_system.agents.items():
        print(f"{key} instructions:\n{agent.instructions}\n")

if __name__ == "__main__":
    asyncio.run(main())
