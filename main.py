# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import asyncio
from datetime import datetime

from orchestration import TherapyAgents, Session, SessionAggregator, append_session_log

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

therapy_agents = TherapyAgents()

# In this single-turn scenario, we may not even need session_states if each session is ephemeral.
# But if you want to log each single-turn session, you can store aggregator in memory keyed by session_id.
session_states: Dict[str, SessionAggregator] = {}

# ----------------------------------------
# Pydantic Models
# ----------------------------------------
class PromptRequest(BaseModel):
    prompt: str
    patient_id: Optional[str] = "patient_1"

class AIResponseItem(BaseModel):
    response_id: str
    text: str

class StartSessionResponse(BaseModel):
    session_id: str
    prompt: str
    responses: List[AIResponseItem]

class FeedbackItem(BaseModel):
    response_id: str
    text: str
    rank: Optional[int] = None
    ratings: Dict[str, Optional[int]] = {}
    feedback: str = ""

class PilotFeedback(BaseModel):
    session_id: str
    patient_id: str
    prompt: str
    ai_responses: List[FeedbackItem]

# ----------------------------------------
# Helper: Append data to JSON
# ----------------------------------------
async def append_to_file(new_data: dict, file_path: str, root_key: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {root_key: []}

    if root_key not in data or not isinstance(data[root_key], list):
        data[root_key] = []

    data[root_key].append(new_data)

    await asyncio.to_thread(
        lambda: json.dump(data, open(file_path, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    )
    return "Data appended successfully."

# ----------------------------------------
# 1) /start_session
# ----------------------------------------
@app.post("/start_session", response_model=StartSessionResponse)
async def start_session(data: PromptRequest):
    """
    Single-turn scenario: generate multiple responses from an agent, return them, 
    optionally store in aggregator if you want session logs.
    """
    session_id = f"session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    aggregator = SessionAggregator(session_id, data.patient_id)
    session_obj = Session(therapy_agents)

    # Generate multiple responses from your agent
    responses = await session_obj.generate_multiple_responses("srt_agent", data.prompt, 3)

    # Store them in aggregator if you want to log this single-turn session
    single_segment = {
        "segment_id": 1,
        "modality": "srt_agent",
        "start_time": datetime.utcnow().isoformat() + "Z",
        "end_time": None,
        "prompt": data.prompt,
        "candidate_responses": [
            {"response_id": f"res{i+1}", "text": resp}
            for i, resp in enumerate(responses)
        ],
        "chosen_response": None
    }
    aggregator.add_dialogue_segment(single_segment)

    # Optionally keep aggregator in memory if you want to finalize or do more with it
    session_states[session_id] = aggregator

    return {
        "session_id": session_id,
        "prompt": data.prompt,
        "responses": [
            {"response_id": f"res{i+1}", "text": resp}
            for i, resp in enumerate(responses)
        ]
    }

# ----------------------------------------
# 2) /submit_feedback
# ----------------------------------------
@app.post("/submit_feedback")
async def submit_feedback(feedback: PilotFeedback):
    """
    Single-turn feedback. The front-end sends chosen response rank, ratings, etc.
    We can store it in logs or 'expert_feedback.json'.
    """
    aggregator = session_states.get(feedback.session_id)
    if aggregator:
        # Mark session end
        aggregator.set_end_time()

        # If there's a top-ranked item (rank=1), store it in aggregator
        top_item = next((item for item in feedback.ai_responses if item.rank == 1), None)
        if top_item:
            aggregator.data["dialogue_segments"][0]["chosen_response"] = top_item.response_id

        # Append aggregator to session logs if you want
        await append_session_log(aggregator.get_session_data())

    # Also store the feedback in an "expert_feedback.json"
    enriched_feedback = {
        "session_id": feedback.session_id,
        "patient_id": feedback.patient_id,
        "prompt": feedback.prompt,
        "ai_responses": [item.dict() for item in feedback.ai_responses],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    result = await append_to_file(enriched_feedback, "data/expert_feedback.json", "feedbacks")

    return {"message": "Feedback submitted", "result": result}

@app.get("/")
def root():
    return {"message": "MemoryBridge single-turn API running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
