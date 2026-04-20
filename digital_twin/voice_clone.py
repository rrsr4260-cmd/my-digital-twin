from TTS.api import TTS
from config import VOICE_SAMPLE, VOICE_OUTPUT

print("Loading voice cloning model...")

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

def speak_clone(text):
    try:
        print("Generating cloned voice...")

        tts.tts_to_file(
            text=text,
            speaker_wav=VOICE_SAMPLE,
            language="en",
            file_path=VOICE_OUTPUT
        )

        print("Voice saved:", VOICE_OUTPUT)

    except Exception as e:
        print("Voice clone error:", e)