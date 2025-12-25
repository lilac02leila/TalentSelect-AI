"""Soft Skills Agent - Evaluates interpersonal qualities."""
from crewai import Agent
from langchain_groq import ChatGroq
from utils.config import GROQ_MODEL, TEMPERATURE


def create_soft_skills_agent(llm=None):
    """Create the Soft Skills Agent."""
    if llm is None:
        from utils.config import GROQ_API_KEY
        llm = ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, groq_api_key=GROQ_API_KEY)
    
    return Agent(
        role="Agent Soft Skills - Expert en Qualités Interpersonnelles",
        goal="Évaluer les soft skills des candidats: communication, leadership, travail d'équipe, "
             "motivation, adaptabilité et adéquation culturelle avec l'entreprise.",
        backstory="Vous êtes un psychologue du travail spécialisé dans l'évaluation des compétences "
                 "comportementales. Vous analysez les lettres de motivation, les descriptions de "
                 "projets et les expériences pour identifier les qualités interpersonnelles et "
                 "l'adéquation culturelle des candidats.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )