import os
import pandas as pd
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOllama
from langchain.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from difflib import SequenceMatcher

class ChatPDF:
    def __init__(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None 
        self.model = ChatOllama(model="llama3")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know.  

            When responding to CSV content, consider the column headers and the corresponding data. Understand that each row represents a record and each column represents a field. [/INST] </s> 

            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )
        self.df = None  # Store the DataFrame for CSV data
        self.documents = []  # Store all documents from multiple PDFs
        self.pdf_texts = []  # Store raw text of multiple PDFs

    def ingest_pdf(self, pdf_file_paths: list = None, folder_path: str = None):
        self.pdf_texts = []  # Clear any previous PDF texts
        all_chunks = []
        
        # Get PDF file paths from the specified folder
        if folder_path:
            pdf_file_paths = self._get_pdfs_from_folder(folder_path)
        
        if not pdf_file_paths:
            return "No PDF files to ingest."
        
        for pdf_file_path in pdf_file_paths:
            docs = PyPDFLoader(file_path=pdf_file_path).load()
            chunks = self.text_splitter.split_documents(docs)
            chunks = filter_complex_metadata(chunks)
            all_chunks.extend(chunks)
            self.pdf_texts.append(" ".join([chunk.page_content for chunk in chunks]))
        self._create_vector_store(all_chunks)
    
    def _get_pdfs_from_folder(self, folder_path: str):
        return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]

    def ingest_csv(self, csv_file_path: str):
        self.df = pd.read_csv(csv_file_path)
        docs = self._convert_df_to_documents(self.df)
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        self._create_vector_store(chunks)
        return self.df  # Return the dataframe for display purposes

    def _convert_df_to_documents(self, df):
        documents = []
        headers = ", ".join(df.columns)
        for index, row in df.iterrows():
            content = f"Row {index + 1}\nHeaders: {headers}\n" + "\n".join([f"{col}: {row[col]}" for col in df.columns])
            documents.append(Document(page_content=content))
        return documents

    def _create_vector_store(self, chunks):
        self.vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 5, "score_threshold": 0.3}
        )
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()} | self.prompt | self.model | StrOutputParser())

    def compare_pdfs(self):
        if len(self.pdf_texts) != 2:
            return "Please, add exactly two PDFs to compare."
        
        text1, text2 = self.pdf_texts
        similarity_ratio = SequenceMatcher(None, text1, text2).ratio()
        return f"The similarity ratio between the two PDFs is: {similarity_ratio:.2f}"

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a document first."
        
        if self.df is not None and any(keyword in query.lower() for keyword in ['calculate', 'summarize', 'compute']):
            # Handle calculation questions based on CSV data
            return self._handle_calculation_query(query)
        else:
            # Handle non-calculation questions or other queries
            return self.chain.invoke(query)

    def _handle_calculation_query(self, query):
        # Implement logic to interpret and answer calculation-related queries based on self.df
        # Example logic:
        if 'sum' in query.lower():
            return str(self.df.sum())
        elif 'mean' in query.lower():
            return str(self.df.mean())
        else:
            return "I'm sorry, I couldn't understand the calculation request."

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.df = None
        self.documents = []  # Clear stored documents
        self.pdf_texts = []  # Clear stored PDF texts
