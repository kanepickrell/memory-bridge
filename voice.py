# voice.py

import os
from openai import OpenAI

class VoiceManager:
    """
    A minimal class to handle audio transcription with OpenAI's Whisper API.
    In a typical web scenario, you receive an UploadFile from FastAPI and pass it to 'transcribe_audio'.
    """

    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)

    def transcribe_audio(self, file_obj, filename="recording.wav", mime="audio/wav"):
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, file_obj, mime),
            response_format="text"
        )
        return transcription

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY not set in environment variables")
    voice_manager = VoiceManager(api_key)
