import gradio as gr
import os
import tempfile

from backend.transcriber import transcribe_audio
from backend.translator import translate_text
from backend.subtitle_writer import write_srt_file


def process_video(file, target_lang):
    if file is None:
        return "⚠️ No file uploaded.", None, None, None, None, None

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(file.read())
        temp_path = temp_file.name

    # Transcription
    segments, full_text = transcribe_audio(temp_path)

    # Translation
    translated_segments = [translate_text(seg['text'], target_lang) for seg in segments]
    translated_text = "\n\n".join(translated_segments)

    # Generate subtitle files
    os.makedirs("output", exist_ok=True)
    english_srt_path = os.path.join("output", "english.srt")
    translated_srt_path = os.path.join("output", f"{target_lang}.srt")

    write_srt_file(segments, [seg['text'] for seg in segments], english_srt_path)
    write_srt_file(segments, translated_segments, translated_srt_path)

    return (
        full_text,
        translated_text,
        temp_path,
        english_srt_path,
        translated_srt_path,
        f"✅ Done! Subtitles translated to {target_lang.upper()}."
    )


def launch_gradio_app():
    with gr.Blocks(css=".gradio-container { font-family: 'Segoe UI'; max-width: 950px; margin: auto; }") as demo:
        gr.Markdown("""
        # 🌍 EduTranslateAI
        ### AI-Powered Subtitle Generator for Education  
        Upload your video/audio, generate English & translated subtitles, and download `.srt` files.
        """)

        with gr.Row():
            file_input = gr.File(label="📁 Upload Lecture File (MP4, MP3, WAV)", file_types=[".mp4", ".mp3", ".wav"])
            lang_dropdown = gr.Dropdown(
                label="🌐 Translate to",
                choices=["ur", "hi", "ar", "fr", "zh"],
                value="ur",
                interactive=True
            )

        with gr.Row():
            video_player = gr.Video(label="🎥 Preview Uploaded File", interactive=False)

        with gr.Tab("📄 English Transcript"):
            english_box = gr.Textbox(label="English Transcript", lines=12, interactive=False)

        with gr.Tab("🌐 Translated Subtitles"):
            translated_box = gr.Textbox(label="Translated Transcript", lines=12, interactive=False)

        with gr.Row():
            eng_srt_file = gr.File(label="⬇️ Download English Subtitles (.srt)")
            translated_srt_file = gr.File(label="⬇️ Download Translated Subtitles (.srt)")

        status = gr.Textbox(label="✅ Status", interactive=False)

        file_input.change(
            fn=process_video,
            inputs=[file_input, lang_dropdown],
            outputs=[english_box, translated_box, video_player, eng_srt_file, translated_srt_file, status]
        )

        gr.Markdown("---")
        gr.Markdown("<center><small>Made with 💖 in Pakistan 🇵🇰 by Zain Ali Khan</small></center>")

    demo.launch()


if __name__ == "__main__":
    launch_gradio_app()

