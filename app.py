# EduTranslate AI: Gradio-based Subtitle Generator

import gradio as gr
import os
from backend.transcriber import transcribe_audio
from backend.translator import translate_text
from backend.subtitle_writer import write_srt_file
import tempfile


def process_video(file):
    if file is None:
        return "No video uploaded.", None, None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(file.read())
        temp_video_path = temp_video.name

    # Transcribe
    segments, full_text = transcribe_audio(temp_video_path)

    # Translate
    translated_segments = [translate_text(seg['text'], "ur") for seg in segments]

    # Generate Subtitles
    english_srt_path = os.path.join("output", "english.srt")
    urdu_srt_path = os.path.join("output", "urdu.srt")

    write_srt_file(segments, [seg['text'] for seg in segments], english_srt_path)
    write_srt_file(segments, translated_segments, urdu_srt_path)

    return full_text, english_srt_path, urdu_srt_path


def launch_app():
    with gr.Blocks(css=".gradio-container { font-family: 'Segoe UI'; max-width: 900px; margin: auto; }") as demo:
        gr.Markdown("""
        # 🌍 EduTranslate AI
        ### Professional Subtitle Generator with AI Transcription & Translation
        Upload your lecture video/audio file and download English + Urdu subtitles.
        """)

        with gr.Row():
            input_file = gr.File(label="Upload Lecture Video (MP4, MP3, WAV)", file_types=[".mp4", ".mp3", ".wav"])

        with gr.Row():
            transcribed_text = gr.Textbox(label="English Transcript", lines=10)

        with gr.Row():
            english_srt = gr.File(label="⬇️ Download English Subtitles")
            urdu_srt = gr.File(label="⬇️ Download Urdu Subtitles")

        input_file.change(fn=process_video, inputs=input_file, outputs=[transcribed_text, english_srt, urdu_srt])

    demo.launch()


if __name__ == "__main__":
    launch_app()

