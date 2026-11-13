
import os
import argparse

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


def fetch_transcript(video_id: str) -> str:
    """Fetch an English YouTube transcript and return plain text."""

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en"])

    return " ".join(item.text for item in transcript)


def format_docs(documents) -> str:
    """Combine retrieved documents into one context string."""

    return "\n\n".join(
        document.page_content for document in documents
    )


def build_chain(transcript: str):

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    # Step 1: Split transcript into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.create_documents([transcript])

    # Step 2: Create HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Step 3: Store embeddings in FAISS
    vector_store = FAISS.from_documents(
        chunks,
        embeddings,
    )

    # Step 4: Create retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    # Step 5: Initialize Groq LLM
    llm = ChatGroq(
    model="openai/gpt-oss-120b",
        temperature=0.2,
    )

    # Step 6: Create RAG prompt
    prompt = PromptTemplate(
        template=(
            "You are a helpful assistant.\n"
            "Answer only using the provided transcript context. "
            "If the context does not contain the answer, "
            "say you don't know.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n"
            "Answer:"
        ),
        input_variables=["context", "question"],
    )

    # Step 7: Build RAG chain
    parallel_chain = RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
    )

    final_chain = (
        parallel_chain
        | prompt
        | llm
        | StrOutputParser()
    )

    return final_chain


def main():

    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Ask questions about a YouTube video's transcript."
    )

    parser.add_argument(
        "video_id",
        help="YouTube video ID, not the full URL",
    )

    parser.add_argument(
        "--question",
        default="Can you summarize the video?",
        help="Question to ask about the video",
    )

    args = parser.parse_args()

    try:
        transcript_text = fetch_transcript(args.video_id)

    except TranscriptsDisabled:
        raise SystemExit(
            "This video does not have captions available."
        )

    except Exception as exc:
        raise SystemExit(
            f"Could not fetch transcript: {exc}"
        )

    print(
        f"Fetched transcript ({len(transcript_text)} characters)."
    )

    chain = build_chain(transcript_text)

    answer = chain.invoke(args.question)

    print("\nAnswer:\n")
    print(answer)


if __name__ == "__main__":
    main()
