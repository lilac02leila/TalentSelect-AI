"""Exploratory Data Analysis module for candidate data."""
import pandas as pd
import numpy as np
from typing import List, Dict
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


class ExploratoryAnalysis:
    """Performs exploratory data analysis on candidate dataset."""
    
    def __init__(self):
        self.candidates_df = None
    
    def create_dataframe(self, processed_candidates: List[Dict]) -> pd.DataFrame:
        """Create a pandas DataFrame from processed candidates."""
        records = []
        
        for candidate in processed_candidates:
            record = {
                'candidate_id': candidate.get('candidate_id', ''),
                'filename': candidate.get('filename', ''),
                'word_count': candidate.get('text_metrics', {}).get('word_count', 0),
                'sentence_count': candidate.get('text_metrics', {}).get('sentence_count', 0),
                'vocabulary_richness': candidate.get('text_metrics', {}).get('vocabulary_richness', 0),
                'experience_years': candidate.get('experience_years', 0),
                'num_technical_skills': len(candidate.get('technical_skills', [])),
                'num_soft_skills': len(candidate.get('soft_skills', [])),
                'technical_skills': ', '.join(candidate.get('technical_skills', [])),
                'soft_skills': ', '.join(candidate.get('soft_skills', []))
            }
            records.append(record)
        
        self.candidates_df = pd.DataFrame(records)
        return self.candidates_df
    
    def generate_summary_statistics(self) -> Dict:
        """Generate summary statistics for the dataset."""
        if self.candidates_df is None or self.candidates_df.empty:
            return {}
        
        summary = {
            'total_candidates': len(self.candidates_df),
            'avg_experience_years': self.candidates_df['experience_years'].mean(),
            'avg_word_count': self.candidates_df['word_count'].mean(),
            'avg_technical_skills': self.candidates_df['num_technical_skills'].mean(),
            'avg_soft_skills': self.candidates_df['num_soft_skills'].mean(),
            'experience_range': {
                'min': self.candidates_df['experience_years'].min(),
                'max': self.candidates_df['experience_years'].max()
            }
        }
        
        return summary
    
    def analyze_skill_distribution(self) -> Dict:
        """Analyze the distribution of skills across candidates."""
        if self.candidates_df is None or self.candidates_df.empty:
            return {}
        
        # Technical skills distribution
        all_technical = []
        for skills_str in self.candidates_df['technical_skills']:
            if skills_str:
                all_technical.extend([s.strip() for s in skills_str.split(',')])
        
        technical_counter = Counter(all_technical)
        
        # Soft skills distribution
        all_soft = []
        for skills_str in self.candidates_df['soft_skills']:
            if skills_str:
                all_soft.extend([s.strip() for s in skills_str.split(',')])
        
        soft_counter = Counter(all_soft)
        
        return {
            'top_technical_skills': dict(technical_counter.most_common(10)),
            'top_soft_skills': dict(soft_counter.most_common(10)),
            'technical_skills_diversity': len(set(all_technical)),
            'soft_skills_diversity': len(set(all_soft))
        }
    
    def generate_visualizations(self, output_dir: str = "data/processed"):
        """Generate visualization plots for the dataset."""
        if self.candidates_df is None or self.candidates_df.empty:
            return
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
        # 1. Experience distribution
        plt.figure()
        self.candidates_df['experience_years'].hist(bins=10, edgecolor='black')
        plt.title('Distribution des Années d\'Expérience')
        plt.xlabel('Années d\'Expérience')
        plt.ylabel('Nombre de Candidats')
        plt.savefig(f'{output_dir}/experience_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Skills count distribution
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        self.candidates_df['num_technical_skills'].hist(bins=10, ax=axes[0], edgecolor='black')
        axes[0].set_title('Distribution des Compétences Techniques')
        axes[0].set_xlabel('Nombre de Compétences Techniques')
        axes[0].set_ylabel('Nombre de Candidats')
        
        self.candidates_df['num_soft_skills'].hist(bins=10, ax=axes[1], edgecolor='black')
        axes[1].set_title('Distribution des Soft Skills')
        axes[1].set_xlabel('Nombre de Soft Skills')
        axes[1].set_ylabel('Nombre de Candidats')
        plt.savefig(f'{output_dir}/skills_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Word count vs Experience
        plt.figure()
        plt.scatter(self.candidates_df['experience_years'], 
                   self.candidates_df['word_count'], 
                   alpha=0.6)
        plt.title('Relation entre Expérience et Longueur du CV')
        plt.xlabel('Années d\'Expérience')
        plt.ylabel('Nombre de Mots')
        plt.savefig(f'{output_dir}/experience_vs_wordcount.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_report(self) -> str:
        """Generate a text report of the exploratory analysis."""
        if self.candidates_df is None or self.candidates_df.empty:
            return "Aucune donnée disponible pour l'analyse."
        
        summary = self.generate_summary_statistics()
        skill_dist = self.analyze_skill_distribution()
        
        report = f"""
=== RAPPORT D'ANALYSE EXPLORATOIRE ===

1. STATISTIQUES GÉNÉRALES
   - Nombre total de candidats: {summary.get('total_candidates', 0)}
   - Expérience moyenne: {summary.get('avg_experience_years', 0):.2f} ans
   - Nombre moyen de mots par CV: {summary.get('avg_word_count', 0):.0f}
   - Compétences techniques moyennes: {summary.get('avg_technical_skills', 0):.2f}
   - Soft skills moyens: {summary.get('avg_soft_skills', 0):.2f}
   - Plage d'expérience: {summary.get('experience_range', {}).get('min', 0):.1f} - {summary.get('experience_range', {}).get('max', 0):.1f} ans

2. DISTRIBUTION DES COMPÉTENCES
   - Diversité des compétences techniques: {skill_dist.get('technical_skills_diversity', 0)}
   - Diversité des soft skills: {skill_dist.get('soft_skills_diversity', 0)}
   
   Top 5 Compétences Techniques:
"""
        for skill, count in list(skill_dist.get('top_technical_skills', {}).items())[:5]:
            report += f"   - {skill}: {count} candidats\n"
        
        report += "\n   Top 5 Soft Skills:\n"
        for skill, count in list(skill_dist.get('top_soft_skills', {}).items())[:5]:
            report += f"   - {skill}: {count} candidats\n"
        
        return report

