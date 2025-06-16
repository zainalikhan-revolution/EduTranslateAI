from gtts import gTTS
import os

def text_to_speech(text, lang="ur", output_path="output/voice.mp3"):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        return output_path
    except Exception as e:
        print("TTS Error:", e)
        return None
