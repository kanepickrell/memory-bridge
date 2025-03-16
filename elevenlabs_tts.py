# elevenlabs_tts.py
import requests

class ElevenLabsTTS:
    def __init__(self, api_key: str, voice_id: str):
        """
        :param api_key: Your ElevenLabs API key
        :param voice_id: The ID of the cloned voice from ElevenLabs
        """
        self.api_key = api_key
        self.voice_id = voice_id

    def synthesize_speech(self, text: str) -> bytes:
        """
        Calls ElevenLabs TTS API to convert `text` into an MP3 in your cloned voice.
        Returns the MP3 bytes.
        """
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # raises error if request failed
        return response.content  # MP3 bytes
