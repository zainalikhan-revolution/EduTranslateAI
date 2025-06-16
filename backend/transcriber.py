import whisper

def transcribe_audio(path):
    model = whisper.load_model("base")
    result = model.transcribe(path, verbose=False)
    return result["segments"], result["text"]
