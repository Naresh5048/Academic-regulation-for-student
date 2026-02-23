import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Configuration
DATA_PATH = "./data"
CHROMA_PATH = "./chroma_db"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class IngestionEngine:
    def __init__(self):
        # Using local free embeddings
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            raise e
            
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        self.vector_store = None

    def sync_data(self):
        """Load PDFs from directory, split, and store in ChromaDB."""
        print(f"Syncing data from {DATA_PATH}...")
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            
        loader = DirectoryLoader(DATA_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        if not documents:
            print("No PDF files found in data directory.")
            return False

        chunks = self.text_splitter.split_documents(documents)
        
        # Remove old DB to re-index fresh
        import shutil
        if os.path.exists(CHROMA_PATH):
            try:
                shutil.rmtree(CHROMA_PATH)
            except Exception as e:
                print(f"Warning: Could not remove old DB: {e}")

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=CHROMA_PATH
        )
        # In newer Chroma, persist() is often automatic or no longer needed, 
        # but kept for compatibility.
        if hasattr(self.vector_store, 'persist'):
            self.vector_store.persist()
            
        print(f"Successfully indexed {len(chunks)} chunks.")
        return True

    def get_vector_store(self):
        if self.vector_store is None:
            if os.path.exists(CHROMA_PATH) and len(os.listdir(CHROMA_PATH)) > 0:
                self.vector_store = Chroma(
                    persist_directory=CHROMA_PATH,
                    embedding_function=self.embeddings
                )
            else:
                return None
        return self.vector_store

class ChatEngine:
    def __init__(self):
        self.ingestion_engine = IngestionEngine()
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=GROQ_API_KEY
        )
        
        # Custom Prompt Template
        template = """
        You are the Official LBRCE Assistant. Your goal is to provide accurate information to students based on the provided campus notices and documents.
        
        Context: {context}
        Question: {question}
        
        Instructions:
        1. Use ONLY the provided context to answer. If the answer isn't in the context, say "I'm sorry, I don't have information on that in the official notices."
        2. If a year is missing in a document (e.g., "Holiday on Dec 25"), assume the current year is 2026.
        3. Be concise, professional, and helpful.
        
        Answer:"""
        
        self.prompt = PromptTemplate.from_template(template)

    def ask(self, query: str):
        vector_store = self.ingestion_engine.get_vector_store()
        if not vector_store:
            return "System Error: Vector store not initialized. Please ensure PDFs are in the './data' folder and click 'Sync Now' in the sidebar."

        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Build LCEL Chain
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        try:
            answer = rag_chain.invoke(query)
            return answer
        except Exception as e:
            return f"Error communicating with Groq: {str(e)}"
