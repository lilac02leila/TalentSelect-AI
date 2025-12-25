"""Profile Agent - Analyzes CVs and cover letters."""
from crewai import Agent
from langchain_groq import ChatGroq
from utils.config import GROQ_MODEL, TEMPERATURE


def create_profile_agent(llm=None):
    """Create the Profile Agent."""
    if llm is None:
        from utils.config import GROQ_API_KEY
        llm = ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, groq_api_key=GROQ_API_KEY)
    
    return Agent(
        role="Agent Profil - Analyste de Profils Candidats",
        goal="Analyser en profondeur les CVs et lettres de motivation pour extraire les informations "
             "clés: expérience, formation, compétences, réalisations et cohérence du parcours professionnel.",
        backstory="Vous êtes un analyste spécialisé dans l'évaluation de profils candidats. "
                 "Vous maîtrisez les techniques de NER (Named Entity Recognition), l'extraction "
                 "de compétences et le scoring de profils. Vous êtes capable d'identifier les "
                 "points forts et les lacunes dans un parcours professionnel.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )