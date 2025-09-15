# backend/backend.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import os # <-- ADDED

app = FastAPI()

# --- MODIFIED ---
# Instead of a global variable, we'll use file paths to check for the database
FAISS_INDEX_PATH = "faiss_index"
# Initialize embeddings globally as it's a constant
embeddings = OllamaEmbeddings(model="llama2")
# --- END MODIFIED ---

class QueryRequest(BaseModel):
    question: str

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_pdf_path = "temp.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(await file.read())

    # Load and process the PDF
    loader = PyPDFLoader(temp_pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # Create and save the FAISS vector store
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(FAISS_INDEX_PATH) # <-- CHANGED: Save the DB to disk

    # Clean up the temporary PDF file
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)

    return {"status": "PDF processed and indexed successfully"}

@app.post("/ask/")
async def ask_question(request: QueryRequest):
    # --- MODIFIED ---
    # Check if the FAISS index exists on disk
    if not os.path.exists(FAISS_INDEX_PATH):
        return {"answer": "Database not found. Please upload a PDF first!"}

    # Load the FAISS index from disk
    db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    # --- END MODIFIED ---

    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(request.question)
    
    # Initialize the LLM
    llm = OllamaLLM(model="llama2")
    
    # Create the context and prompt
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"Answer the question based ONLY on the following context. If the answer is not in the context, say 'I don't know'.\n\nContext:\n{context}\n\nQuestion: {request.question}\nAnswer:"
    
    # Get the answer from the LLM
    answer = llm.invoke(prompt)

    return {"answer": answer}