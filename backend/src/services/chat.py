from langchain.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from config.settings import settings
from typing import List, Dict, Optional

class ChatService:
    def __init__(self):
        self.llm = Ollama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE
        )
        self.embeddings = OllamaEmbeddings(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.MODEL_NAME
        )
        
    async def chat_without_rag(self, message: str, history: List[Dict] = None) -> str:
        """Simple chat without RAG"""
        if history:
            context = "\n".join([f"{m['role']}: {m['content']}" for m in history])
            prompt = f"{context}\nUser: {message}\nAssistant:"
        else:
            prompt = f"User: {message}\nAssistant:"
            
        response = self.llm.predict(prompt)
        return response

    async def create_vector_store(self, text: str) -> Chroma:
        """Create a vector store from text"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_text(text)
        
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings
        )
        return vectorstore

    async def chat_with_rag(
        self,
        message: str,
        vectorstore: Chroma,
        history: List[Dict] = None
    ) -> tuple[str, List[Dict]]:
        """Chat with RAG"""
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )
        
        result = qa_chain({"question": message, "chat_history": history or []})
        
        sources = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in result["source_documents"]
        ]
        
        return result["answer"], sources 