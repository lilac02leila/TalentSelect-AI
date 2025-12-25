"""Decider Agent - Aggregates opinions and makes final decisions."""
from crewai import Agent
from utils.config import GROQ_MODEL, TEMPERATURE, GROQ_API_KEY
import os


def create_decider_agent(llm=None):
    """Create the Decider Agent."""
    if llm is None:
        from langchain_groq import ChatGroq
        api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment. Please set it in your .env file")
        llm = ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, api_key=api_key)
    
    return Agent(
        role="Agent Décideur - Directeur du Recrutement",
        goal="Agréger les évaluations de tous les agents, établir un classement final des candidats "
             "avec des scores justifiés, et générer un rapport explicable pour le recruteur.",
        backstory="Vous êtes le directeur du recrutement avec une vision globale. Vous synthétisez "
                 "les avis de tous les experts (RH, Profil, Technique, Soft Skills) pour prendre "
                 "une décision éclairée. Vous êtes responsable de la transparence et de l'explicabilité "
                 "du processus de sélection. Vous générez des rapports détaillés avec des justifications "
                 "claires pour chaque classement.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )