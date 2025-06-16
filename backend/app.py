import streamlit as st
from backend.transcriber import transcribe_audio
from backend.translator import translate_text
from backend.subtitle_writer import write_srt_file

st.title("EduTranslate AI 🌍 - Professional Subtitle Generator")

video = st.file_uploader("Upload Lecture Video", type=["mp4", "mp3", "wav"])

if video:
    with open("uploaded_video.mp4", "wb") as f:
        f.write(video.read())
    
    st.video("uploaded_video.mp4")
    st.write("🔄 Transcribing...")
    segments, full_text = transcribe_audio("uploaded_video.mp4")
    st.success("✅ Transcription Complete")
    
    st.subheader("English Transcript")
    st.write(full_text)

    st.write("🌍 Translating to Urdu...")
    
    # ✅ FIX: Translate each segment using your translate_text function
    translated_segments = [translate_text(seg['text'], "ur") for seg in segments]
    
    st.success("✅ Translation Done")

    write_srt_file(segments, translated_segments, "output/urdu.srt")
    st.download_button("⬇️ Download Urdu Subtitles", open("output/urdu.srt", "rb"), "urdu.srt")

    write_srt_file(segments, [seg['text'] for seg in segments], "output/english.srt")
    st.download_button("⬇️ Download English Subtitles", open("output/english.srt", "rb"), "english.srt")

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

