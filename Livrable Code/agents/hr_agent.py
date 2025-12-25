"""HR Agent - Reads job descriptions and recruiter criteria."""
from crewai import Agent
from utils.config import GROQ_MODEL, TEMPERATURE, GROQ_API_KEY
import os


def create_hr_agent(llm=None):
    """Create the HR Agent."""
    if llm is None:
        from langchain_groq import ChatGroq
        api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment. Please set it in your .env file")
        llm = ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, api_key=api_key)
    
    return Agent(
        role="Agent RH - Spécialiste en Recrutement",
        goal="Analyser et comprendre les besoins du recruteur, extraire les critères essentiels "
             "du poste et les exigences spécifiques pour guider l'évaluation des candidats.",
        backstory="Vous êtes un expert RH avec plus de 15 ans d'expérience dans le recrutement "
                 "technique. Vous avez une compréhension approfondie des besoins des entreprises "
                 "et savez identifier les critères essentiels pour un poste donné.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

