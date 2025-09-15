# PDF-Pal: Your Intelligent Document Chatbot 📄🤖

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Frameworks](https://img.shields.io/badge/Frameworks-FastAPI%20%7C%20Streamlit-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

PDF-Pal is a powerful and intuitive chatbot designed to answer questions about any PDF document you provide. It leverages a sophisticated **Retrieval-Augmented Generation (RAG)** pipeline, powered by a local Large Language Model (LLM) via **Ollama**, to deliver accurate, context-aware answers directly from your documents.

This project serves as a practical, end-to-end example of building a modern AI application with a decoupled frontend (Streamlit) and backend (FastAPI).

## 🎥 Demo


![PDF-Pal Demo](./docs/demo.gif)
*A quick look at the user interface.*

---

## ✨ Core Features

* **Dynamic Document Ingestion**: Upload any PDF file through a user-friendly web interface.
* **Intelligent Q&A**: Ask complex questions in natural language and receive precise answers.
* **Context-Aware Responses**: The chatbot uses the content of the PDF as its sole source of truth, preventing hallucinations.
* **Local First**: All processing, including embeddings and language generation, happens locally via Ollama, ensuring data privacy.
* **Scalable Architecture**: A robust backend built with FastAPI handles the heavy AI/ML workload, while a lightweight Streamlit frontend provides a responsive user experience.

---

## 🏗️ How It Works (Architecture)

This application is built on a modern RAG pipeline. The diagram below illustrates the flow of data from user interaction to the final answer.

```mermaid
graph TD
    subgraph Frontend (Streamlit)
        A[User uploads PDF] --> B{Process PDF};
        C[User asks question] --> D{Submit Query};
    end

    subgraph Backend (FastAPI)
        E[/upload_pdf/ endpoint]
        F[/ask/ endpoint]
        G[LangChain RAG Pipeline]
        H[FAISS Vector Store]
    end

    subgraph Local AI (Ollama)
        I[OllamaEmbeddings]
        J[OllamaLLM: Llama 2]
    end

    B --> E;
    D --> F;

    E --> G;
    G -- 1. Chunks & Embeds --> I;
    I -- 2. Creates Vectors --> H;

    F -- 3. Embeds Query --> I;
    F -- 4. Similarity Search --> H;
    H -- 5. Retrieves Relevant Chunks --> G;
    G -- 6. Augments Prompt --> J;
    J -- 7. Generates Answer --> F;
    F -- 8. Returns Answer --> D;
```

### The RAG Pipeline in Detail:

1.  **Ingestion & Indexing (`/upload_pdf/`)**:
    * The user uploads a PDF, which is sent to the FastAPI backend.
    * `PyPDFLoader` loads the document's content.
    * `RecursiveCharacterTextSplitter` breaks the document into smaller, manageable chunks.
    * `OllamaEmbeddings` converts each text chunk into a numerical vector (embedding).
    * These vectors are stored in a `FAISS` vector store, which is saved locally for persistent, efficient searching.

2.  **Retrieval & Generation (`/ask/`)**:
    * The user's question is sent to the backend.
    * The question is converted into an embedding using the same model.
    * `FAISS` performs a similarity search to find the most relevant text chunks from the document.
    * These retrieved chunks (the "context") are combined with the original question into a detailed prompt.
    * This augmented prompt is sent to the `OllamaLLM` (Llama 2), which generates an answer based *only* on the provided context.

---

## 🛠️ Tech Stack

| Component         | Technology                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| **Backend** | [**FastAPI**](https://fastapi.tiangolo.com/), [**Uvicorn**](https://www.uvicorn.org/)                           |
| **Frontend** | [**Streamlit**](https://streamlit.io/)                                                                        |
| **LLM & Embeddings** | [**Ollama**](https://ollama.ai/) (running Llama 2)                                                            |
| **RAG Pipeline** | [**LangChain**](https://www.langchain.com/)                                                                   |
| **Vector Store** | [**FAISS**](https://github.com/facebookresearch/faiss) (from `langchain-community`)                             |
| **PDF Processing**| `PyPDFLoader`                                                                                                 |

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.9+**
* **Git**
* **Ollama**: Ensure Ollama is installed and running on your system. You can download it from [ollama.ai](https://ollama.ai/).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/pdf-qa-chatbot.git](https://github.com/YourUsername/pdf-qa-chatbot.git)
    cd pdf-qa-chatbot
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Pull the Llama 2 model for Ollama:**
    ```bash
    ollama pull llama2
    ```

### Running the Application

You must run the backend and frontend in **two separate terminals**.

1.  **Terminal 1: Start the Backend Server**
    ```bash
    python -m uvicorn backend.backend:app --reload --port 8000
    ```

2.  **Terminal 2: Start the Frontend App**
    ```bash
    streamlit run frontend/app.py
    ```

Once both are running, open your browser and navigate to **`http://localhost:8501`** to use PDF-Pal.

---

## 📂 Project Structure

```
pdf-qa-chatbot/
│
├── backend/
│   └── backend.py      # FastAPI application, RAG logic
│
├── frontend/
│   └── app.py          # Streamlit user interface
│
├── faiss_index/        # (Generated) Stores the FAISS vector index
│
├── .gitignore          # Specifies files for Git to ignore
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

---

## 🗺️ Roadmap & Future Improvements

-   [ ] Support for more document types (e.g., `.docx`, `.txt`, `.md`).
-   [ ] Implement persistent chat history per session.
-   [ ] Allow the user to select different Ollama models from the UI.
-   [ ] Dockerize the entire application for easier deployment.
-   [ ] Add basic user authentication to manage documents.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YourUsername/pdf-qa-chatbot/issues).

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.