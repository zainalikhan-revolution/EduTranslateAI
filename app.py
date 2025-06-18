import gradio as gr
import os
import tempfile

from backend.transcriber import transcribe_audio
from backend.translator import translate_text
from backend.subtitle_writer import write_srt_file


def process_video(file):
    if file is None:
        return "⚠️ No video uploaded.", None, None

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(file.read())
        temp_path = temp_file.name

    # Transcription
    segments, full_text = transcribe_audio(temp_path)

    # Urdu Translation
    translated_segments = [translate_text(seg['text'], "ur") for seg in segments]

    # Generate subtitle files
    os.makedirs("output", exist_ok=True)
    english_srt_path = os.path.join("output", "english.srt")
    urdu_srt_path = os.path.join("output", "urdu.srt")

    write_srt_file(segments, [seg['text'] for seg in segments], english_srt_path)
    write_srt_file(segments, translated_segments, urdu_srt_path)

    return full_text, english_srt_path, urdu_srt_path


def launch_gradio_app():
    with gr.Blocks(css=".gradio-container { font-family: 'Segoe UI'; max-width: 900px; margin: auto; }") as demo:
        gr.Markdown("""
        # 🌍 EduTranslateAI
        ### AI-Powered Subtitle Generator for Education
        Upload your lecture video/audio file, get instant English & Urdu subtitles, and download `.srt` files.
        """)

        with gr.Row():
            file_input = gr.File(label="📁 Upload Lecture Video", file_types=[".mp4", ".mp3", ".wav"])

        with gr.Row():
            english_textbox = gr.Textbox(label="📄 English Transcript", lines=12, interactive=False)

        with gr.Row():
            english_srt_file = gr.File(label="⬇️ Download English Subtitles (.srt)")
            urdu_srt_file = gr.File(label="⬇️ Download Urdu Subtitles (.srt)")

        file_input.change(
            fn=process_video,
            inputs=file_input,
            outputs=[english_textbox, english_srt_file, urdu_srt_file]
        )

        gr.Markdown("---")
        gr.Markdown("<center><small>Made with 💖 in Pakistan 🇵🇰 by Zain Ali Khan</small></center>")

    demo.launch()


if __name__ == "__main__":
    launch_gradio_app()

