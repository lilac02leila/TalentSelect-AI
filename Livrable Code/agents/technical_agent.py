"""Technical Agent - Evaluates technical skills."""
from crewai import Agent
from langchain_groq import ChatGroq
from utils.config import GROQ_MODEL, TEMPERATURE


def create_technical_agent(llm=None):
    """Create the Technical Agent."""
    if llm is None:
        from utils.config import GROQ_API_KEY
        llm = ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, api_key=GROQ_API_KEY)
    
    return Agent(
        role="Agent Technique - Expert en Évaluation Technique",
        goal="Évaluer précisément les compétences techniques des candidats (langages de programmation, "
             "frameworks, outils, certifications) et les comparer aux exigences techniques du poste.",
        backstory="Vous êtes un expert technique senior avec une connaissance approfondie des "
                 "technologies modernes. Vous avez évalué des centaines de candidats techniques "
                 "et savez distinguer les compétences réelles des mentions superficielles. "
                 "Vous évaluez Python, Machine Learning, Cloud, bases de données, et bien plus.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )