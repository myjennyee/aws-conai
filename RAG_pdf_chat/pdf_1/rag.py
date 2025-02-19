from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOllama
from langchain.embeddings import OllamaEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
import concurrent.futures
import asyncio
import aiofiles
import tempfile

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
            to answer the question. If you don't know the answer, just say that you don't know. Use ten sentences
            maximum and keep the answer concise [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

    async def read_file_async(self, file_path):
        async with aiofiles.open(file_path, mode='rb') as file:
            content = await file.read()
        return content

    def ingest(self, pdf_file_path: str):
        try:
            # Load the PDF
            docs = PyPDFLoader(file_path=pdf_file_path).load()
            print("PDF loaded successfully.")
            
            # Split the documents
            chunks = self.text_splitter.split_documents(docs)
            print(f"Documents split into {len(chunks)} chunks.")
            
            # Filter metadata
            chunks = filter_complex_metadata(chunks)
            print("Metadata filtered.")
            
            # Initialize embedding
            embedding = OllamaEmbeddings()
            print("Embedding model instantiated.")
            
            # Create vector store in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_vector_store = executor.submit(
                    Chroma.from_documents, documents=chunks, embedding=embedding
                )
                self.vector_store = future_vector_store.result()
            print("Vector store created successfully.")
            
            # Create retriever
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"k": 5, "score_threshold": 0.3}
            )
            print("Retriever created successfully.")
            
            # Initialize processing chain
            self.chain = ({"context": self.retriever, "question": RunnablePassthrough()} | self.prompt | self.model | StrOutputParser())
            print("Processing chain initialized successfully.")
            
        except Exception as e:
            print(f"Error during ingestion: {e}")
            self.vector_store = None
            self.retriever = None
            self.chain = None

    def ask(self, query: str):
        if not self.chain:
            print("Processing chain not initialized. Please call ingest() first.")
            return "Processing chain not initialized. Please call ingest() first."
        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
