import os
import tempfile
import streamlit as st
from streamlit_chat import message  # Ensure you have imported this correctly from your package
from rag import ChatPDF  # Assuming this is the correct import path for your ChatPDF class

st.set_page_config(page_title="ChatPDF")

def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            if user_text.lower() == "compare pdfs":
                agent_text = st.session_state["assistant"].compare_pdfs()
            else:
                agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))

def read_and_save_file():
    st.session_state["assistant"].clear()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    uploaded_files = st.session_state.file_uploader
    folder_path = st.session_state.folder_path

    if folder_path:
        folder_path = folder_path.strip()
        if os.path.exists(folder_path):
            with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting documents from folder"):
                st.session_state["assistant"].ingest_pdf(folder_path=folder_path)
        else:
            st.error("Folder path does not exist.")

    if uploaded_files:
        file_paths = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as tf:
                tf.write(uploaded_file.read())
                file_paths.append(tf.name)

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting documents"):
            if any(file.name.endswith(".pdf") for file in uploaded_files):
                st.session_state["assistant"].ingest_pdf(pdf_file_paths=file_paths)
            elif any(file.name.endswith(".csv") for file in uploaded_files):
                for file_path in file_paths:
                    if file_path.endswith(".csv"):
                        df = st.session_state["assistant"].ingest_csv(file_path)
                        st.session_state["df_preview"] = df.head(3)  # Save the first few rows for display
        for file_path in file_paths:
            os.remove(file_path)

def page():
    if "assistant" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatPDF()

    st.header("Chat PDF/CSV")
    st.subheader("Upload documents or specify a folder")
    st.file_uploader("Upload documents", type=["pdf", "csv"],
        key="file_uploader", on_change=read_and_save_file,
        label_visibility="collapsed", accept_multiple_files=True  # Allow multiple files
    )
    st.text_input("Folder path", key="folder_path", on_change=read_and_save_file)
    st.session_state["ingestion_spinner"] = st.empty()

    if "df_preview" in st.session_state:
        st.subheader("CSV Preview")
        st.dataframe(st.session_state["df_preview"], use_container_width=True)

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)

if __name__ == "__main__":
    page()
