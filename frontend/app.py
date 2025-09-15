# frontend/app.py
import streamlit as st
import requests

st.set_page_config(page_title="PDF Q&A Chatbot", layout="wide")
st.title("📄 PDF Question Answer Chatbot")

backend_url = "http://127.0.0.1:8000"

# --- UI for PDF Upload ---
with st.sidebar:
    st.header("1. Upload your PDF")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if st.button("Process PDF"):
        if uploaded_file is not None:
            # Show a spinner while the PDF is being processed
            with st.spinner("Processing PDF... this may take a moment."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{backend_url}/upload_pdf/", files=files)
                    if response.status_code == 200:
                        st.success("✅ PDF processed successfully!")
                        st.session_state.pdf_processed = True
                    else:
                        st.error(f"❌ Failed to process PDF: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please upload a PDF file first.")

# --- Chat Interface ---
st.header("2. Ask Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(f'<div style="text-align: right;"><strong>🧑 You:</strong> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div><strong>🤖 Bot:</strong> {msg}</div>', unsafe_allow_html=True)


# Chat input
question = st.chat_input("Ask a question about the PDF...")
if question:
    # Add user's question to the chat history and display it
    st.session_state.messages.append(("You", question))
    st.markdown(f'<div style="text-align: right;"><strong>🧑 You:</strong> {question}</div>', unsafe_allow_html=True)
    
    # Show a spinner while waiting for the bot's response
    with st.spinner("🤖 Thinking..."):
        try:
            response = requests.post(f"{backend_url}/ask/", json={"question": question})
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.messages.append(("Bot", answer))
                # Rerun to display the new message immediately
                st.rerun()
            else:
                st.error(f"Error from backend: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")