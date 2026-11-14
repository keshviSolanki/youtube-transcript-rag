# 🎬 YouTube Transcript RAG with LangChain

An AI-powered **YouTube Transcript Question Answering System** built using Python, LangChain, Groq, HuggingFace Embeddings, FAISS, and Streamlit.

This project allows users to enter a YouTube video URL or video ID and ask questions about its content. It automatically extracts available English or Hindi transcripts, converts transcript chunks into vector embeddings, retrieves the most relevant information using FAISS similarity search, and generates context-aware answers using an LLM.

The application provides both a **command-line interface (CLI)** and an interactive **Streamlit web interface**.

## 🚀 Features

- 🎥 Accept YouTube video URLs or video IDs.
- 📝 Automatically extract available English or Hindi transcripts.
- 🌐 Support manually created and auto-generated transcripts.
- 🔄 Prefer English transcripts and fall back to Hindi.
- ✂️ Split transcripts into manageable text chunks.
- 🧠 Generate embeddings using HuggingFace Sentence Transformers.
- 🗄️ Store and retrieve vectors using FAISS.
- 🔍 Retrieve the four most relevant transcript chunks.
- 🤖 Generate context-aware answers using Groq LLM.
- 💬 Ask multiple questions about a selected video through the Streamlit interface.
- 🖥️ Interactive and styled Streamlit UI.
- 🔐 Secure API key management using environment variables.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | RAG pipeline and LLM orchestration |
| Groq | LLM inference |
| GPT-OSS-120B | Answer generation through Groq |
| HuggingFace Embeddings | Text vector generation |
| all-MiniLM-L6-v2 | Sentence embedding model |
| FAISS | Vector storage and similarity search |
| YouTube Transcript API | YouTube transcript extraction |
| Streamlit | Interactive web interface |
| Python Dotenv | Environment variable management |

## 🏗️ System Architecture

### RAG Workflow

```text
              YouTube Video URL / ID
                        |
                        v
             YouTube Transcript API
                        |
                        v
                Transcript Fetching
                 (English / Hindi)
                        |
                        v
                 Text Processing
                        |
                        v
                 Text Splitting
              (Chunk: 1000 characters
               Overlap: 200 characters)
                        |
                        v
              HuggingFace Embeddings
                 all-MiniLM-L6-v2
                        |
                        v
                  FAISS Vector Store
                        |
                        v
                  User Question
                        |
                        v
                Semantic Retrieval
                  (Top 4 Chunks)
                        |
                        v
                Retrieved Context
                        |
                        v
                 RAG Prompt Template
                        |
                        v
                  Groq LLM
                 GPT-OSS-120B
                        |
                        v
                Context-Aware Answer
```

### Application Workflow

```text
             User
              |
              v
        Streamlit UI
           app.py
              |
              v
       Extract YouTube ID
              |
              v
       User Question
              |
              v
       Python Subprocess
              |
              v
         src/main.py
              |
              v
          RAG Pipeline
              |
              v
        Groq LLM Response
              |
              v
       Display Answer in UI
```

## 📁 Project Structure

```text
youtube-transcript-rag/
│
├── src/
│   └── main.py              # RAG backend and CLI
│
├── app.py                   # Streamlit frontend
│
├── .env                     # API keys (not committed)
├── .env.example             # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/keshviSolanki/youtube-transcript-rag.git

cd youtube-transcript-rag
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Important:** Never upload your `.env` file or expose your API keys on GitHub.

### 5. Run the Application

**Option A: Streamlit Web Interface**

```powershell
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

Paste a YouTube URL, click **Load Video**, and start asking questions.

**Option B: Command-Line Interface**

```powershell
python src/main.py jNJH6uD5LQE --question "What is this video about?"
```

You can replace the video ID and question with your own.

## 🔍 How It Works

1. **Transcript Extraction:** Uses the YouTube Transcript API to fetch available English or Hindi transcripts, preferring English and falling back to Hindi.
2. **Text Splitting:** Uses LangChain's `RecursiveCharacterTextSplitter` to divide transcripts into chunks of 1000 characters with 200 characters of overlap.
3. **Embedding Generation:** Uses HuggingFace's `all-MiniLM-L6-v2` model to convert text chunks into numerical vector representations.
4. **Vector Storage:** Stores transcript embeddings in a FAISS vector store.
5. **Semantic Retrieval:** Retrieves the four most relevant transcript chunks based on the user's question.
6. **Prompt Construction:** Combines retrieved transcript context with the user's question using a LangChain prompt template.
7. **LLM Processing:** Sends the prompt to the Groq-hosted GPT-OSS-120B model.
8. **Answer Generation:** Generates a context-aware answer using the retrieved transcript information.
9. **UI Response:** Displays the generated answer in the Streamlit chat interface.

## 💡 Example Usage

**YouTube Video:**

```text
https://www.youtube.com/watch?v=jNJH6uD5LQE
```

**Example Questions:**

```text
What is this video about?

Explain the main concepts discussed in this video.

What is the difference between Generative AI and Agentic AI?

Summarize the important points of this video.
```

**Example Output:**

```text
Answer:

The video explains Generative AI, Large Language Models,
AI agents, and Agentic AI. It discusses how LLMs generate
content and how AI agents use external tools and APIs
to perform tasks.
```

*Actual responses depend on the selected video's transcript and the question.*

## 📚 Key Concepts Learned

- Retrieval-Augmented Generation (RAG)
- LangChain architecture and runnable chains
- YouTube Transcript API integration
- Multilingual transcript extraction
- Text splitting and chunk overlap
- HuggingFace Sentence Transformers
- Text embeddings and vector representations
- FAISS vector databases
- Semantic similarity search
- Context-aware question answering
- Groq LLM integration
- Prompt engineering
- Streamlit application development
- Python subprocess integration

## 📝 Important Notes

- English transcripts are preferred; Hindi transcripts are used as a fallback.
- The application requires accessible transcripts for the selected video.
- The vector store is generated dynamically from the transcript during execution.
- No persistent vector database is required.
- HuggingFace embeddings run locally.
- Groq API access is required for answer generation.
- LLM responses are restricted to the retrieved transcript context by the RAG prompt.
- Model availability and API usage are subject to Groq's service limits.

## 🔮 Future Improvements

- Support additional transcript languages.
- Add persistent vector storage.
- Improve retrieval with reranking.
- Add conversation memory for follow-up questions.
- Support multiple YouTube videos in one knowledge base.
- Add source citations with transcript timestamps.

## 👨‍💻 Author

**Keshvi Solanki**

- GitHub: [@keshviSolanki](https://github.com/keshviSolanki)

---

**Project Category:** Generative AI | Retrieval-Augmented Generation | LangChain | NLP | Python | Vector Databases
