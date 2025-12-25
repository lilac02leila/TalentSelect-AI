"""RAG retriever for candidate search."""
from typing import List, Dict
from rag.vector_store import VectorStore


class RAGRetriever:
    """Retrieves relevant candidates using RAG."""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def retrieve_by_job_requirements(self, job_description: str, top_k: int = 10) -> List[Dict]:
        """Retrieve candidates matching job requirements."""
        # Create a query from job description
        query = f"Recherche de candidats avec les compétences suivantes: {job_description}"
        return self.vector_store.search_similar(query, top_k=top_k)
    
    def retrieve_by_skills(self, required_skills: List[str], top_k: int = 10) -> List[Dict]:
        """Retrieve candidates with specific skills."""
        query = f"Compétences requises: {', '.join(required_skills)}"
        return self.vector_store.search_similar(query, top_k=top_k)
    
    def retrieve_by_experience(self, min_experience: float, top_k: int = 10) -> List[Dict]:
        """Retrieve candidates with minimum experience."""
        query = f"Candidat avec au moins {min_experience} ans d'expérience"
        return self.vector_store.search_similar(query, top_k=top_k)

