"""Vector store implementation using ChromaDB for RAG."""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os
from utils.config import CHROMA_DB_PATH, EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer


class VectorStore:
    """Manages vector embeddings and similarity search for candidates."""
    
    def __init__(self, collection_name: str = "candidates"):
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize SentenceTransformer for local embeddings
        try:
            print(f"Loading embedding model: {EMBEDDING_MODEL}")
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
            print("Embedding model loaded successfully!")
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            self.embedding_model = None
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using SentenceTransformer."""
        if not self.embedding_model:
            print("Error: Embedding model not initialized")
            return []
        
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            return []
    
    def add_candidates(self, candidates: List[Dict[str, str]]):
        """Add candidate documents to the vector store."""
        if not candidates:
            return
        
        texts = []
        ids = []
        metadatas = []
        
        for candidate in candidates:
            candidate_id = candidate.get('candidate_id', '')
            content = candidate.get('cleaned_content', candidate.get('content', ''))
            
            if content:
                texts.append(content)
                ids.append(candidate_id)
                metadatas.append({
                    'filename': candidate.get('filename', ''),
                    'candidate_id': candidate_id
                })
        
        if texts:
            print(f"Creating embeddings for {len(texts)} candidates...")
            embeddings = self.create_embeddings(texts)
            if embeddings:
                self.collection.add(
                    embeddings=embeddings,
                    documents=texts,
                    ids=ids,
                    metadatas=metadatas
                )
                print(f"Successfully added {len(texts)} candidates to vector store!")
    
    def search_similar(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for similar candidates based on query."""
        if not query:
            return []
        
        # Create query embedding
        query_embedding = self.create_embeddings([query])
        if not query_embedding:
            return []
        
        # Search in collection
        try:
            collection_size = self.collection.count()
            if collection_size == 0:
                print("Warning: Collection is empty")
                return []
            
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=min(top_k, collection_size)
            )
        except Exception as e:
            print(f"Error searching collection: {e}")
            return []
        
        # Format results
        candidates = []
        if results['ids'] and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                candidates.append({
                    'candidate_id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else 0.0
                })
        
        return candidates
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print("Collection cleared successfully!")
        except Exception as e:
            print(f"Error clearing collection: {e}")
    
    def get_collection_size(self) -> int:
        """Get the number of documents in the collection."""
        try:
            return self.collection.count()
        except:
            return 0