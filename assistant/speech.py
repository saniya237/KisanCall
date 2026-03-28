import whisper
import os
import tempfile
import uuid
from gtts import gTTS

# Load Whisper model once
model = whisper.load_model("base")

def speech_to_text(audio_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        result = model.transcribe(tmp_path)
        os.unlink(tmp_path)
        return result["text"].strip()

    except Exception as e:
        return f"STT Error: {str(e)}"


def text_to_speech(response_text):
    try:
        filename = f"response_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join("media", filename)
        os.makedirs("media", exist_ok=True)

        tts = gTTS(text=response_text, lang='en', slow=False)
        tts.save(output_path)
        return output_path

    except Exception as e:
        return f"TTS Error: {str(e)}"