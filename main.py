# main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import asyncio
from datetime import datetime
import os
import tempfile
import io
import subprocess  # for ffmpeg conversion
import requests

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env if present

# Import your existing code
from orchestration import TherapyAgents, Session, SessionAggregator, append_session_log
from voice import VoiceManager  # your VoiceManager that calls OpenAI Whisper

########################################
# ElevenLabs TTS Class
########################################
class ElevenLabsTTS:
    def __init__(self, api_key: str, voice_id: str):
        self.api_key = api_key
        self.voice_id = voice_id

    def synthesize_speech(self, text: str) -> bytes:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.content  # MP3 bytes

########################################
# FFmpeg Conversion Helper
########################################
def convert_to_wav(input_path: str, output_path: str):
    # Check if the input file is empty
    if os.stat(input_path).st_size == 0:
        raise Exception(f"Input file {input_path} is empty. Recording might have failed.")

    result = subprocess.run(
        ["ffmpeg", "-y", "-f", "webm", "-i", input_path, "-vn", "-acodec", "pcm_s16le", output_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"ffmpeg conversion failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
    return output_path

########################################
# FastAPI App
########################################
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weekly_performance")
def get_weekly_performance():
    try:
        file_path = os.path.join("data", "weekly_performance.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading weekly_performance.json: {str(e)}")

########################################
# Therapy Setup
########################################
therapy_agents = TherapyAgents()
session_states: Dict[str, SessionAggregator] = {}

########################################
# Pydantic Models
########################################
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

########################################
# Helper: append_to_file
########################################
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

########################################
# /start_session endpoint
########################################
@app.post("/start_session", response_model=StartSessionResponse)
async def start_session(data: PromptRequest):
    session_id = f"session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    aggregator = SessionAggregator(session_id, data.patient_id)
    session_obj = Session(therapy_agents)
    responses = await session_obj.generate_multiple_responses("srt_agent", data.prompt, 3)
    single_segment = {
        "segment_id": 1,
        "modality": "srt_agent",
        "start_time": datetime.utcnow().isoformat() + "Z",
        "end_time": None,
        "prompt": data.prompt,
        "candidate_responses": [
            {"response_id": f"res{i+1}", "text": resp} for i, resp in enumerate(responses)
        ],
        "chosen_response": None
    }
    aggregator.add_dialogue_segment(single_segment)
    session_states[session_id] = aggregator
    return {
        "session_id": session_id,
        "prompt": data.prompt,
        "responses": [
            {"response_id": f"res{i+1}", "text": resp} for i, resp in enumerate(responses)
        ]
    }

########################################
# /submit_feedback endpoint
########################################
@app.post("/submit_feedback")
async def submit_feedback(feedback: PilotFeedback):
    aggregator = session_states.get(feedback.session_id)
    if aggregator:
        aggregator.set_end_time()
        top_item = next((item for item in feedback.ai_responses if item.rank == 1), None)
        if top_item:
            aggregator.data["dialogue_segments"][0]["chosen_response"] = top_item.response_id
        await append_session_log(aggregator.get_session_data())
    enriched_feedback = {
        "session_id": feedback.session_id,
        "patient_id": feedback.patient_id,
        "prompt": feedback.prompt,
        "ai_responses": [item.dict() for item in feedback.ai_responses],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    result = await append_to_file(enriched_feedback, "data/expert_feedback.json", "feedbacks")
    return {"message": "Feedback submitted", "result": result}

########################################
# /voice_chat endpoint: Transcribe + Orchestrate + TTS
########################################
@app.post("/voice_chat")
async def voice_chat(
    audio_file: UploadFile = File(...),
    session_id: Optional[str] = None,
    patient_id: Optional[str] = "patient_1"
):
    # 1) Save the uploaded audio file temporarily (likely .webm)
    contents = await audio_file.read()
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(contents)
        tmp.flush()
        webm_path = tmp.name

    wav_path = webm_path + ".wav"
    try:
        # 2) Convert .webm -> .wav with ffmpeg (forcing WebM input)
        convert_to_wav(webm_path, wav_path)
        # 3) Transcribe using VoiceManager
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY")
        vm = VoiceManager(openai_api_key=OPENAI_API_KEY)
        with open(wav_path, "rb") as f:
            transcript = vm.transcribe_audio(f, filename="recording.wav", mime="audio/wav")
    finally:
        try:
            os.remove(webm_path)
            os.remove(wav_path)
        except Exception as e:
            print("Error cleaning up temporary files:", e)


    # 4) Retrieve or create aggregator for multi-turn usage
    if not session_id:
        session_id = f"session_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    aggregator = session_states.get(session_id)
    if not aggregator:
        aggregator = SessionAggregator(session_id, patient_id)
        session_states[session_id] = aggregator

    # 5) Orchestrate therapy
    session_obj = Session(therapy_agents)
    agent_replies = await session_obj.generate_multiple_responses("multi_agent", transcript, 1)
    agent_response = agent_replies[0] if agent_replies else "No response."
    seg_id = len(aggregator.data["dialogue_segments"]) + 1
    aggregator.add_dialogue_segment({
        "segment_id": seg_id,
        "modality": "voice_chat",
        "start_time": datetime.utcnow().isoformat() + "Z",
        "end_time": datetime.utcnow().isoformat() + "Z",
        "prompt": transcript,
        "candidate_responses": [{"response_id": "res1", "text": agent_response}],
        "chosen_response": "res1",
        "agent_decisions": "multi_agent used for voice chat"
    })

    # 6) ElevenLabs TTS - create the MP3
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_KEY")
    ELEVENLABS_VOICE_KEY = os.getenv("ELEVENLABS_VOICE_KEY", "YOUR_CLONED_VOICE_ID")
    tts = ElevenLabsTTS(api_key=ELEVENLABS_API_KEY, voice_id=ELEVENLABS_VOICE_KEY)
    mp3_data = tts.synthesize_speech(agent_response)

    # 7) Return the MP3 as a streaming response
    return StreamingResponse(
        io.BytesIO(mp3_data),
        media_type="audio/mpeg",
        headers={"session-id": session_id, "transcript": transcript.strip()}
    )

@app.get("/")
def root():
    return {"message": "MemoryBridge single-turn API running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
