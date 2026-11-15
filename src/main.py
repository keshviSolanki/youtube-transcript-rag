
import os
import re
import streamlit as st

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

st.set_page_config(
    page_title="YouTube Transcript RAG",
    page_icon="🎥",
    layout="wide",
)


# -------------------------
# Custom UI
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #111827);
    color: white;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #aab4c8;
    font-size: 17px;
    margin-bottom: 30px;
}

div.stButton > button {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 700;
    width: 100%;
}

div.stButton > button:hover {
    border: 1px solid #a78bfa;
    color: white;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# Transcript helpers
# -------------------------
def extract_video_id(url):
    url = url.strip()

    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    if re.fullmatch(r"[a-zA-Z0-9_-]{11}", url):
        return url

    return None


@st.cache_data(show_spinner=False)
def fetch_transcript(video_id: str) -> str:
    """Fetch English transcript, or Hindi if English is unavailable."""

    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    try:
        transcript = transcript_list.find_transcript(["en", "hi"])
    except Exception:
        transcript = transcript_list.find_generated_transcript(["en", "hi"])

    fetched = transcript.fetch()

    return " ".join(item.text for item in fetched)


def format_docs(documents):
    return "\n\n".join(
        document.page_content for document in documents
    )


# -------------------------
# RAG pipeline
# -------------------------
@st.cache_resource(show_spinner="Loading embedding model...")
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_chain(transcript):

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is missing in Render environment variables.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.create_documents([transcript])

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embeddings,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        max_tokens=800,
    )

    prompt = PromptTemplate(
        template=(
            "You are a helpful YouTube transcript assistant.\n"
            "Answer only using the provided transcript context. "
            "If the context does not contain the answer, say you don't know.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n"
            "Answer:"
        ),
        input_variables=["context", "question"],
    )

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    })

    return parallel_chain | prompt | llm | StrOutputParser()


# -------------------------
# Streamlit application
# -------------------------
def main():

    st.markdown(
        '<div class="main-title">🎥 YouTube Transcript RAG</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">Ask questions about any YouTube video using AI-powered RAG.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 🔗 Enter YouTube Video")

    video_url = st.text_input(
        "YouTube URL or Video ID",
        placeholder="https://www.youtube.com/watch?v=XXXXXXXXXXX",
    )

    question = st.text_area(
        "Ask your question",
        value="Can you summarize this video?",
        placeholder="What is this video about?",
        height=100,
    )

    if st.button("🚀 Generate Answer"):

        video_id = extract_video_id(video_url)

        if not video_id:
            st.error("Please enter a valid YouTube URL or video ID.")
            return

        if not question.strip():
            st.warning("Please enter a question.")
            return

        try:
            with st.spinner("Fetching YouTube transcript..."):
                transcript = fetch_transcript(video_id)

            if not transcript.strip():
                st.error("No transcript content found for this video.")
                return

            st.success(
                f"Transcript fetched successfully! "
                f"{len(transcript)} characters."
            )

            with st.spinner("Building RAG pipeline and generating answer..."):
                chain = build_chain(transcript)
                answer = chain.invoke(question.strip())

            st.markdown("### 💡 AI Answer")
            st.markdown(answer)

            with st.expander("📄 View Transcript"):
                st.write(transcript)

        except TranscriptsDisabled:
            st.error("This video does not have captions available.")

        except Exception as exc:
            st.error(f"Something went wrong: {exc}")


if __name__ == "__main__":
    main()
