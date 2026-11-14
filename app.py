import re
import subprocess
import sys
from pathlib import Path

import streamlit as st

# Keep this app.py in the project root, beside the src folder.
PROJECT_DIR = Path(__file__).resolve().parent
RAG_SCRIPT = PROJECT_DIR / "src" / "main.py"

st.set_page_config(
    page_title="YouTube Transcript AI",
    page_icon="🎬",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        background: radial-gradient(circle at 10% 5%, #25235a 0, transparent 32%),
                    radial-gradient(circle at 95% 15%, #123b55 0, transparent 28%),
                    #080d19;
        color: #edf2ff;
    }
    .block-container { max-width: 900px; padding-top: 2.3rem; padding-bottom: 3rem; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f8fafc !important; }
    .hero {
        padding: 1.8rem 2rem; border: 1px solid #ffffff20; border-radius: 22px;
        background: linear-gradient(135deg, #202653e8, #101b2ee8);
        box-shadow: 0 20px 60px #0005; margin-bottom: 1.5rem;
    }
    .eyebrow { color: #a5b4fc; font-size: .75rem; letter-spacing: .16em; font-weight: 700; }
    .hero p { color: #cbd5e1; margin-bottom: 0; }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background: #0b1222 !important; color: #f8fafc !important;
        border: 1px solid #334155 !important; border-radius: 12px !important;
    }
    .stButton > button {
        width: 100%; min-height: 2.9rem; border: 0; border-radius: 12px;
        color: white; font-weight: 700;
        background: linear-gradient(90deg, #6366f1, #0ea5e9);
    }
    .stButton > button:hover { border: 0; filter: brightness(1.12); }
    .note { color: #94a3b8; font-size: .86rem; }
    div[data-testid="stChatMessage"] {
        background: #111a2c; border: 1px solid #ffffff14; border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">LANGCHAIN · RAG · FAISS</div>
      <h1 style="font-size:2.5rem; margin:.45rem 0;">YouTube Transcript AI</h1>
      <p>Paste a YouTube video and ask questions about its content.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

def get_video_id(value: str):
    value = value.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value

    patterns = (
        r"(?:youtube\.com/watch\?.*?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
    )
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return None


if "video_id" not in st.session_state:
    st.session_state.video_id = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("1. Choose a YouTube video")
video_input = st.text_input(
    "YouTube URL or video ID",
    placeholder="https://www.youtube.com/watch?v=Gfr50f6ZBvo",
)

if st.button("Load video", key="load_video"):
    new_video_id = get_video_id(video_input)
    if not new_video_id:
        st.error("Please enter a valid YouTube URL or 11-character video ID.")
    elif not RAG_SCRIPT.exists():
        st.error(f"Backend file not found: {RAG_SCRIPT}")
    else:
        st.session_state.video_id = new_video_id
        st.session_state.chat_history = []
        st.success(f"Video selected: {new_video_id}")

if st.session_state.video_id:
    st.markdown(
        f'<p class="note">Selected video ID: <b>{st.session_state.video_id}</b></p>',
        unsafe_allow_html=True,
    )
    st.subheader("2. Ask a question")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about this video...")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Reading the transcript and generating an answer..."):
                command = [
                    sys.executable,
                    str(RAG_SCRIPT),
                    st.session_state.video_id,
                    "--question",
                    question,
                ]
                try:
                    result = subprocess.run(
                        command,
                        cwd=str(PROJECT_DIR),
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=600,
                    )
                    if result.returncode == 0:
                        answer = result.stdout.strip()
                        if not answer:
                            answer = "The backend completed but did not print an answer. Check that src/main.py prints its final response."
                        st.markdown(answer)
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": answer}
                        )
                    else:
                        error_text = result.stderr.strip() or result.stdout.strip()
                        st.error("The RAG backend returned an error.")
                        st.code(error_text or "No error details were returned.")
                except subprocess.TimeoutExpired:
                    st.error("The request took longer than 10 minutes and was stopped.")
                except Exception as exc:
                    st.exception(exc)
else:
    st.info("Paste a YouTube video URL above and click **Load video** to start chatting.")

st.markdown(
    '<p class="note" style="text-align:center; margin-top:2rem;">Powered by your existing Python · LangChain · FAISS backend</p>',
    unsafe_allow_html=True,
)
