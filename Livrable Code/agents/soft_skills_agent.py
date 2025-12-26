"""Soft Skills Agent - Evaluates interpersonal qualities."""
import groq_patch  # noqa: F401 - Fix for proxies error

from crewai import Agent
from langchain_groq import ChatGroq
from utils.config import GROQ_MODEL, TEMPERATURE


def create_soft_skills_agent(llm=None):
    """Create the Soft Skills Agent."""
    if llm is None:
        from groq_patch import patch_langchain_groq
        patch_langchain_groq()
        from utils.config import GROQ_API_KEY
        llm = ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, api_key=GROQ_API_KEY)
    
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