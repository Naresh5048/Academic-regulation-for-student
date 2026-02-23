import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
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
        """Load PDFs and Text files from directory, split, and store in ChromaDB."""
        print(f"Syncing data from {DATA_PATH}...")
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            
        all_documents = []
        
        # 1. Load PDF files
        try:
            pdf_loader = DirectoryLoader(DATA_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
            pdf_docs = pdf_loader.load()
            for doc in pdf_docs:
                doc.metadata["source_type"] = "official_notice"
            all_documents.extend(pdf_docs)
            print(f"Loaded {len(pdf_docs)} PDF documents.")
        except Exception as e:
            print(f"Error loading PDFs: {e}")

        # 2. Load Text files (faculty messages, updates)
        try:
            txt_loader = DirectoryLoader(DATA_PATH, glob="./*.txt", loader_cls=TextLoader)
            txt_docs = txt_loader.load()
            for doc in txt_docs:
                doc.metadata["source_type"] = "dynamic_update"
            all_documents.extend(txt_docs)
            print(f"Loaded {len(txt_docs)} Text messages/updates.")
        except Exception as e:
            print(f"Error loading Text files: {e}")
        
        if not all_documents:
            print("No supported files found in data directory.")
            return False

        chunks = self.text_splitter.split_documents(all_documents)
        
        # Remove old DB to re-index fresh
        import shutil
        if os.path.exists(CHROMA_PATH):
            try:
                shutil.rmtree(CHROMA_PATH)
                # Small wait to ensure OS releases directory handle
                import time
                time.sleep(0.5)
            except Exception as e:
                print(f"Warning: Could not remove old DB: {e}")

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=CHROMA_PATH
        )
        
        print(f"Successfully indexed {len(chunks)} chunks.")
        return True

    def get_vector_store(self):
        if self.vector_store is None:
            if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
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
        
        # Advanced Prompt Template handling priority
        template = """
        You are the Official LBRCE Assistant. You provide information to students based on two types of inputs:
        1. Official Notices/Schedules (PDF files)
        2. Dynamic Updates/Messages (Text files dropped by faculty/admins)

        HIERARCHY OF TRUTH:
        - If there is a contradiction, Dynamic Updates take priority over Official Notices.
        - For example: If a PDF says "Period 1 is in Room 201" but a Text message says "Period 1 shifted to Lab 3", you MUST tell the student it is in Lab 3.
        - If a teacher is reported absent in a message, that overrides any existing schedule.

        Context from Data Folder:
        {context}

        Student's Question: {question}

        Instructions:
        1. Analyze the context for any dynamic updates (messages) that might contradict static schedules.
        2. Provide the MOST RECENT and accurate status based on this priority.
        3. If no information is found in either source, say "I'm sorry, I don't have information on that in the official notices or recent updates."
        4. Be concise and professional.

        Answer:"""
        
        self.prompt = PromptTemplate.from_template(template)

    def ask(self, query: str):
        vector_store = self.ingestion_engine.get_vector_store()
        if not vector_store:
            return "System Error: Vector store not initialized. Please ensure documents/messages are in the './data' folder and click 'Sync Now'."

        retriever = vector_store.as_retriever(search_kwargs={"k": 8}) # Increased k to ensure we get both notice and update
        
        def format_docs(docs):
            formatted = []
            for doc in docs:
                source_type = doc.metadata.get("source_type", "unknown")
                source_name = os.path.basename(doc.metadata.get("source", "unknown"))
                content = f"[{source_type.upper()} Source: {source_name}]\n{doc.page_content}"
                formatted.append(content)
            return "\n\n---\n\n".join(formatted)

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

