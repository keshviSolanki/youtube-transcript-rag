# YouTube Transcript RAG with LangChain

An AI-powered YouTube Transcript Question Answering application built using Python, LangChain, OpenAI, and FAISS.

This project allows users to ask questions about a YouTube video. It extracts the video's English transcript, converts it into embeddings, retrieves the most relevant transcript sections using vector similarity search, and generates context-aware answers using an LLM.

## 🚀 Features

- Accept YouTube video IDs as input.
- Automatically fetch English video transcripts.
- Split transcripts into manageable text chunks.
- Generate embeddings using OpenAI.
- Store and search embeddings using FAISS.
- Retrieve the four most relevant transcript chunks.
- Ask questions about video content.
- Generate context-aware answers using GPT-4o-mini.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | LLM application framework |
| OpenAI | Embeddings and language model |
| GPT-4o-mini | Answer generation |
| YouTube Transcript API | Transcript extraction |
| FAISS | Vector storage and similarity search |
| Python Dotenv | Environment variable management |

## 🏗️ Architecture

```text
YouTube Video ID
       |
       v
YouTube Transcript API
       |
       v
Transcript Extraction
       |
       v
Text Splitting
       |
       v
OpenAI Embeddings
       |
       v
FAISS Vector Store
       |
       v
Similarity Search
       |
       v
Retrieve Top 4 Chunks
       |
       v
GPT-4o-mini (LLM)
       |
       v
Context-Aware Answer
```

## 📁 Project Structure

```text
youtube-transcript-rag/
│
├── src/
│   └── main.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/langchain-python.git
cd langchain-python/youtube-transcript-rag
```

### 2. Create and Activate Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure API Key

Copy `.env.example` to `.env` and add your OpenAI API key.

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Important:** Never commit `.env` or expose your API key on GitHub.

### 5. Run the Application

Provide a YouTube video ID and an optional question.

```powershell
python src/main.py Gfr50f6ZBvo --question "Can you summarize the video?"
```

You can also ask specific questions about the video content.

## 🔍 How It Works

1. **Transcript Extraction:** Fetches the English transcript using the YouTube Transcript API.
2. **Text Splitting:** Divides the transcript into smaller chunks for efficient processing.
3. **Embeddings Generation:** Converts transcript chunks into numerical vector representations using OpenAI embeddings.
4. **Vector Storage:** Stores embeddings in a FAISS vector store.
5. **Semantic Retrieval:** Searches the vector database and retrieves the four most relevant transcript chunks based on the user's question.
6. **LLM Processing:** Passes the retrieved context and question to GPT-4o-mini.
7. **Answer Generation:** Generates a context-aware response using the retrieved transcript content.

## 💡 Example Usage

**Input:**

```powershell
python src/main.py Gfr50f6ZBvo --question "Can you summarize the video?"
```

**Expected Output:**

```text
Question: Can you summarize the video?

Answer:
An AI-generated response based on the relevant
sections retrieved from the YouTube transcript.
```

*The actual response depends on the selected video and its transcript.*

## 📚 Key Concepts Learned

- Retrieval-Augmented Generation (RAG)
- LangChain document processing
- YouTube transcript extraction
- Text chunking and splitting
- OpenAI embeddings
- FAISS vector databases
- Semantic similarity search
- Context-aware question answering
- LLM integration with GPT-4o-mini

## 📝 Notes

- The project fetches English transcripts using the provided YouTube video ID.
- It uses `YouTubeTranscriptApi().fetch()` instead of the older `get_transcript()` class method.
- The vector store is created from the fetched transcript during execution; no pre-existing vector database is required.
- OpenAI API usage may incur charges.
- Videos without accessible English transcripts may not work.

## 👨‍💻 Author

**Keshvi Solanki**

GitHub: [keshviSolanki](https://github.com/keshviSolanki)

---

**Project Category:** Generative AI | LangChain | RAG | NLP | Python
