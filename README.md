# YouTube Transcript RAG with LangChain

Ask questions about a YouTube video by retrieving relevant sections from its transcript and passing them to an LLM.

## Project structure

```text
youtube-transcript-rag/
├── src/
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. Create and activate a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 3. Configure your API key

Copy `.env.example` to `.env` and add your own OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Never commit `.env` or publish your API key.

## 4. Run

Pass the YouTube video ID (the part after `v=`) and an optional question:

```powershell
python src/main.py Gfr50f6ZBvo --question "Can you summarize the video?"
```

The script fetches the English transcript, splits it into chunks, creates embeddings, stores them in FAISS, retrieves the four most relevant chunks, and generates an answer using `gpt-4o-mini`.

## Notes

- The YouTube Transcript API changed: this project uses `YouTubeTranscriptApi().fetch(...)` rather than the older `get_transcript(...)` class method.
- The project uses a transcript fetched from the video ID you provide. It does not use a separately pasted transcript or a pre-existing vector store.
- OpenAI API usage may incur charges.
