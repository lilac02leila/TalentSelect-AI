"""Text processing and NLP utilities for candidate documents."""
import re
import spacy
from typing import List, Dict, Set
from collections import Counter


class TextProcessor:
    """Processes and extracts information from candidate texts."""
    
    def __init__(self, language: str = "fr"):
        try:
            if language == "fr":
                self.nlp = spacy.load("fr_core_news_sm")
            else:
                self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print(f"Warning: spaCy model not found. Install with: python -m spacy download {language}_core_news_sm")
            self.nlp = None
        
        # Technical skills keywords
        self.technical_skills = {
            'python', 'java', 'javascript', 'sql', 'r', 'scala', 'go', 'c++', 'c#',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
            'machine learning', 'deep learning', 'neural networks', 'nlp', 'cv',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github',
            'power bi', 'tableau', 'qlik', 'excel', 'spark', 'hadoop',
            'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch'
        }
        
        # Soft skills keywords
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving',
            'creativity', 'adaptability', 'time management', 'organization', 'analytical',
            'critical thinking', 'presentation', 'negotiation', 'mentoring', 'coaching'
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep accents
        text = re.sub(r'[^\w\sàâäéèêëïîôùûüÿç]', ' ', text, flags=re.UNICODE)
        return text.strip()
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text using spaCy."""
        if not self.nlp:
            return {'PERSON': [], 'ORG': [], 'LOC': [], 'DATE': []}
        
        doc = self.nlp(text)
        entities = {
            'PERSON': [],
            'ORG': [],
            'LOC': [],
            'DATE': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities
    
    def extract_skills(self, text: str) -> Dict[str, Set[str]]:
        """Extract technical and soft skills from text."""
        text_lower = text.lower()
        
        technical_found = set()
        soft_found = set()
        
        # Check for technical skills
        for skill in self.technical_skills:
            if skill in text_lower:
                technical_found.add(skill)
        
        # Check for soft skills
        for skill in self.soft_skills:
            if skill in text_lower:
                soft_found.add(skill)
        
        return {
            'technical': technical_found,
            'soft': soft_found
        }
    
    def extract_experience_years(self, text: str) -> float:
        """Extract years of experience from text."""
        # Patterns like "2 ans", "2 years", "2+ ans", etc.
        patterns = [
            r'(\d+)\s*\+?\s*(?:ans?|years?|années?)',
            r'(?:expérience|experience).*?(\d+)\s*(?:ans?|years?|années?)',
            r'(\d+)\s*(?:ans?|years?|années?)\s*(?:d\'?expérience|of experience)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    return float(matches[0])
                except:
                    continue
        
        return 0.0
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information."""
        education_keywords = [
            'diplôme', 'master', 'licence', 'bachelor', 'doctorat', 'phd',
            'école', 'university', 'université', 'ingénieur', 'engineer',
            'baccalauréat', 'bac', 'bts', 'dut', 'mba'
        ]
        
        sentences = re.split(r'[.!?]', text.lower())
        education = []
        
        for sentence in sentences:
            for keyword in education_keywords:
                if keyword in sentence:
                    education.append(sentence.strip())
                    break
        
        return education
    
    def calculate_text_metrics(self, text: str) -> Dict[str, float]:
        """Calculate various text metrics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_words_per_sentence': len(words) / max(len([s for s in sentences if s.strip()]), 1),
            'unique_words': len(set(words)),
            'vocabulary_richness': len(set(words)) / max(len(words), 1)
        }
    
    def process_candidate(self, candidate_data: Dict[str, str]) -> Dict:
        """Process a candidate's documents and extract features."""
        content = candidate_data.get('content', '')
        cleaned_content = self.clean_text(content)
        
        entities = self.extract_entities(cleaned_content)
        skills = self.extract_skills(cleaned_content)
        experience_years = self.extract_experience_years(cleaned_content)
        education = self.extract_education(cleaned_content)
        metrics = self.calculate_text_metrics(cleaned_content)
        
        return {
            'candidate_id': candidate_data.get('candidate_id', ''),
            'filename': candidate_data.get('filename', ''),
            'raw_content': content,
            'cleaned_content': cleaned_content,
            'entities': entities,
            'technical_skills': list(skills['technical']),
            'soft_skills': list(skills['soft']),
            'experience_years': experience_years,
            'education': education,
            'text_metrics': metrics
        }

