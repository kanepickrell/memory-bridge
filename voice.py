import sounddevice as sd
from openai import OpenAI
import numpy as np
import io
from scipy.io.wavfile import write

class VoiceChat:
    def __init__(self):
        self.client = OpenAI(api_key='ADD_KEY_LATER')

    # Record audio from microphone
    def record_audio(self, duration, fs):
        print("Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        return audio

    # Prepare audio for transcription
    def audio_to_buffer(self, audio, fs):
        buffer = io.BytesIO()
        write(buffer, fs, audio)
        buffer.seek(0)
        return buffer

    # Transcribe audio using Whisper
    def transcribe_audio(self, buffer):
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", buffer),
            response_format="text"
        )
        return transcription

    # Chat with GPT-4o
    def chat_with_gpt(self, prompt):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

if __name__ == "__main__":
    vc = VoiceChat()

    # Recording parameters
    duration = 4  # seconds
    fs = 44100     # sample rate

    # Record audio
    audio = vc.record_audio(duration, fs)

    # Process audio and transcribe
    buffer = vc.audio_to_buffer(audio, fs)
    transcription = vc.transcribe_audio(buffer)

    print("You said:", transcription)

    # GPT-4o chat response
    response = vc.chat_with_gpt(transcription)
    print("GPT-4o response:", response)

