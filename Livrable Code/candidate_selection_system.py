"""Main orchestration system for multi-agent candidate selection."""
# IMPORTANT: Import groq_patch FIRST to fix proxies error
# This must be imported before any groq or langchain_groq imports
import groq_patch  # noqa: F401
# Apply patch immediately
from groq_patch import patch_langchain_groq

from crewai import Crew, Task
from typing import List, Dict, Optional
import json
import os

from agents.hr_agent import create_hr_agent
from agents.profile_agent import create_profile_agent
from agents.technical_agent import create_technical_agent
from agents.soft_skills_agent import create_soft_skills_agent
from agents.decider_agent import create_decider_agent
from utils.config import GROQ_MODEL, TEMPERATURE, GROQ_API_KEY


class CandidateSelectionSystem:
    """Main system orchestrating the multi-agent candidate selection process."""
    
    def __init__(self):
        # Initialize LLM with Groq
        try:
            # Ensure patch is applied before importing ChatGroq
            patch_langchain_groq()
            
            from langchain_groq import ChatGroq
            
            api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment. Please set it in your .env file")
            
            # Initialize ChatGroq with correct parameters (no proxies)
            self.llm = ChatGroq(
                model=GROQ_MODEL,
                temperature=TEMPERATURE,
                api_key=api_key
            )
            print(f"✅ Groq LLM initialized with model: {GROQ_MODEL}")
        except Exception as e:
            print(f"❌ Error initializing Groq LLM: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # Initialize agents
        try:
            self.hr_agent = create_hr_agent(self.llm)
            self.profile_agent = create_profile_agent(self.llm)
            self.technical_agent = create_technical_agent(self.llm)
            self.soft_skills_agent = create_soft_skills_agent(self.llm)
            self.decider_agent = create_decider_agent(self.llm)
            print("✅ All agents initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing agents: {e}")
            raise
    
    def analyze_job_requirements(self, job_description: str) -> Task:
        """Task 1: HR Agent analyzes job requirements."""
        task = Task(
            description=f"""
            Analysez la description de poste suivante et extrayez les critères essentiels:
            
            {job_description}
            
            Fournissez:
            1. Le titre du poste
            2. Les compétences techniques requises
            3. Les années d'expérience requises
            4. Les soft skills recherchés
            5. Les critères spécifiques du recruteur
            
            Format de réponse: JSON avec les clés: title, technical_skills, experience_years, soft_skills, specific_criteria
            """,
            agent=self.hr_agent,
            expected_output="Un dictionnaire JSON structuré avec tous les critères du poste"
        )
        return task
    
    def evaluate_profile(self, candidate_data: Dict, job_requirements: str) -> Task:
        """Task 2: Profile Agent evaluates candidate profile."""
        candidate_content = candidate_data.get('cleaned_content', candidate_data.get('content', ''))
        candidate_id = candidate_data.get('candidate_id', 'Unknown')
        
        # Limit content to avoid token limits
        content_preview = candidate_content[:3000] if len(candidate_content) > 3000 else candidate_content
        
        task = Task(
            description=f"""
            Analysez le profil du candidat {candidate_id}:
            
            CONTENU DU CV/LETTRE:
            {content_preview}
            
            EXIGENCES DU POSTE:
            {job_requirements}
            
            Évaluez:
            1. La cohérence du parcours professionnel
            2. La pertinence de l'expérience par rapport au poste
            3. La qualité de la formation
            4. Les réalisations marquantes
            5. Un score global de profil (0-100)
            
            Format de réponse: JSON avec les clés: coherence_score, experience_relevance, education_quality, achievements, profile_score, justification
            """,
            agent=self.profile_agent,
            expected_output="Un dictionnaire JSON avec l'évaluation du profil et un score"
        )
        return task
    
    def evaluate_technical_skills(self, candidate_data: Dict, technical_requirements: str) -> Task:
        """Task 3: Technical Agent evaluates technical skills."""
        candidate_content = candidate_data.get('cleaned_content', candidate_data.get('content', ''))
        candidate_id = candidate_data.get('candidate_id', 'Unknown')
        technical_skills = ', '.join(candidate_data.get('technical_skills', []))
        
        content_preview = candidate_content[:3000] if len(candidate_content) > 3000 else candidate_content
        
        task = Task(
            description=f"""
            Évaluez les compétences techniques du candidat {candidate_id}:
            
            COMPÉTENCES TECHNIQUES DU CANDIDAT:
            {technical_skills}
            
            CONTENU DU CV (extrait):
            {content_preview}
            
            EXIGENCES TECHNIQUES DU POSTE:
            {technical_requirements}
            
            Évaluez:
            1. La maîtrise de chaque compétence requise (0-100)
            2. La profondeur des connaissances techniques
            3. L'expérience pratique avec les technologies
            4. Les certifications et formations techniques pertinentes
            5. Un score technique global (0-100)
            
            Format de réponse: JSON avec les clés: skill_scores, knowledge_depth, practical_experience, certifications, technical_score, justification
            """,
            agent=self.technical_agent,
            expected_output="Un dictionnaire JSON avec l'évaluation technique détaillée"
        )
        return task
    
    def evaluate_soft_skills(self, candidate_data: Dict, soft_requirements: str) -> Task:
        """Task 4: Soft Skills Agent evaluates interpersonal qualities."""
        candidate_content = candidate_data.get('cleaned_content', candidate_data.get('content', ''))
        candidate_id = candidate_data.get('candidate_id', 'Unknown')
        soft_skills = ', '.join(candidate_data.get('soft_skills', []))
        
        content_preview = candidate_content[:3000] if len(candidate_content) > 3000 else candidate_content
        
        task = Task(
            description=f"""
            Évaluez les soft skills du candidat {candidate_id}:
            
            SOFT SKILLS IDENTIFIÉS:
            {soft_skills}
            
            CONTENU DU CV/LETTRE DE MOTIVATION (extrait):
            {content_preview}
            
            SOFT SKILLS RECHERCHÉS:
            {soft_requirements}
            
            Évaluez:
            1. La communication (qualité de l'écrit, clarté)
            2. Le leadership et le travail d'équipe
            3. La motivation et l'engagement
            4. L'adaptabilité et la résilience
            5. L'adéquation culturelle
            6. Un score soft skills global (0-100)
            
            Format de réponse: JSON avec les clés: communication_score, leadership_score, motivation_score, adaptability_score, cultural_fit_score, soft_skills_score, justification
            """,
            agent=self.soft_skills_agent,
            expected_output="Un dictionnaire JSON avec l'évaluation des soft skills"
        )
        return task
    
    def make_final_decision(self, candidate_id: str, all_evaluations: str) -> Task:
        """Task 5: Decider Agent makes final decision."""
        task = Task(
            description=f"""
            En tant qu'agent décideur, synthétisez toutes les évaluations pour le candidat {candidate_id}:
            
            ÉVALUATIONS DES AGENTS:
            {all_evaluations}
            
            Générez:
            1. Un score final agrégé (0-100)
            2. Un classement relatif (nombre entier)
            3. Les points forts du candidat (liste de strings)
            4. Les points faibles ou à améliorer (liste de strings)
            5. Une justification détaillée et explicable du score (string)
            6. Une recommandation (Recommandé / À considérer / Non recommandé)
            
            IMPORTANT: Vous DEVEZ répondre UNIQUEMENT avec un objet JSON valide, sans texte avant ou après.
            Le JSON doit être au format suivant (sans markdown, sans code blocks, juste le JSON brut):
            
            {{
                "final_score": <nombre entre 0 et 100>,
                "ranking": <nombre entier>,
                "strengths": ["point fort 1", "point fort 2", ...],
                "weaknesses": ["point faible 1", "point faible 2", ...],
                "detailed_justification": "<texte de justification>",
                "recommendation": "Recommandé" ou "À considérer" ou "Non recommandé"
            }}
            
            Répondez SEULEMENT avec le JSON, rien d'autre.
            """,
            agent=self.decider_agent,
            expected_output="Un objet JSON valide (sans markdown ni code blocks) avec les clés: final_score (0-100), ranking (entier), strengths (liste), weaknesses (liste), detailed_justification (string), recommendation (string)"
        )
        return task
    
    def evaluate_candidate(self, candidate_data: Dict, job_description: str) -> Dict:
        """Evaluate a single candidate through all agents."""
        try:
            print(f"\n🔄 Evaluating candidate: {candidate_data.get('candidate_id', 'Unknown')}")
            
            # Task 1: Analyze job requirements
            print("  📋 Step 1: Analyzing job requirements...")
            hr_task = self.analyze_job_requirements(job_description)
            hr_crew = Crew(agents=[self.hr_agent], tasks=[hr_task], verbose=False)
            job_analysis = hr_crew.kickoff()
            
            # Extract job requirements from analysis
            job_requirements = str(job_analysis)
            
            # Tasks 2-4: Individual agent evaluations
            print("  👤 Step 2: Profile evaluation...")
            profile_task = self.evaluate_profile(candidate_data, job_requirements)
            
            print("  💻 Step 3: Technical evaluation...")
            technical_task = self.evaluate_technical_skills(candidate_data, job_requirements)
            
            print("  🤝 Step 4: Soft skills evaluation...")
            soft_skills_task = self.evaluate_soft_skills(candidate_data, job_requirements)
            
            evaluation_crew = Crew(
                agents=[self.profile_agent, self.technical_agent, self.soft_skills_agent],
                tasks=[profile_task, technical_task, soft_skills_task],
                verbose=False
            )
            
            evaluations = evaluation_crew.kickoff()
            
            # Task 5: Final decision
            print("  ⚖️  Step 5: Making final decision...")
            all_evaluations_str = f"""
            Évaluation Profil: {profile_task.output if hasattr(profile_task, 'output') else 'N/A'}
            Évaluation Technique: {technical_task.output if hasattr(technical_task, 'output') else 'N/A'}
            Évaluation Soft Skills: {soft_skills_task.output if hasattr(soft_skills_task, 'output') else 'N/A'}
            """
            
            decision_task = self.make_final_decision(candidate_data.get('candidate_id', 'Unknown'), all_evaluations_str)
            decision_crew = Crew(agents=[self.decider_agent], tasks=[decision_task], verbose=False)
            final_decision = decision_crew.kickoff()
            
            # Extract the actual text content from CrewAI response
            # CrewAI can return different formats, so we try multiple approaches
            final_decision_str = None
            if hasattr(final_decision, 'raw'):
                final_decision_str = str(final_decision.raw)
            elif hasattr(final_decision, 'content'):
                final_decision_str = str(final_decision.content)
            elif hasattr(final_decision, 'output'):
                final_decision_str = str(final_decision.output)
            elif isinstance(final_decision, dict):
                final_decision_str = final_decision.get('output', str(final_decision))
            else:
                final_decision_str = str(final_decision)
            
            print(f"  ✅ Evaluation complete for candidate {candidate_data.get('candidate_id', 'Unknown')}")
            
            return {
                'candidate_id': candidate_data.get('candidate_id', 'Unknown'),
                'job_analysis': str(job_analysis),
                'profile_evaluation': str(profile_task.output) if hasattr(profile_task, 'output') else str(evaluations),
                'technical_evaluation': str(technical_task.output) if hasattr(technical_task, 'output') else str(evaluations),
                'soft_skills_evaluation': str(soft_skills_task.output) if hasattr(soft_skills_task, 'output') else str(evaluations),
                'final_decision': final_decision_str
            }
        except Exception as e:
            print(f"  ❌ Error evaluating candidate: {e}")
            return {
                'candidate_id': candidate_data.get('candidate_id', 'Unknown'),
                'error': str(e)
            }
    
    def evaluate_all_candidates(self, candidates: List[Dict], job_description: str) -> List[Dict]:
        """Evaluate all candidates and return ranked results."""
        results = []
        
        for i, candidate in enumerate(candidates, 1):
            print(f"\n{'='*60}")
            print(f"Evaluating candidate {i}/{len(candidates)}")
            print(f"{'='*60}")
            try:
                evaluation = self.evaluate_candidate(candidate, job_description)
                results.append(evaluation)
            except Exception as e:
                print(f"❌ Error evaluating candidate {candidate.get('candidate_id', 'Unknown')}: {e}")
                continue
        
        return results