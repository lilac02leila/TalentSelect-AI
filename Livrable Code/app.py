"""Streamlit interface for the Candidate Selection System."""
# IMPORTANT: Import groq_patch FIRST to fix proxies error
import groq_patch  # noqa: F401
# Apply patch immediately
from groq_patch import patch_langchain_groq
patch_langchain_groq()

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Get the base directory (where app.py is located)
BASE_DIR = Path(__file__).parent.resolve()

import streamlit as st
import pandas as pd
import json
import re
import plotly.express as px
import plotly.graph_objects as go

from preprocessing.data_loader import DataLoader
from preprocessing.text_processor import TextProcessor
from preprocessing.exploratory_analysis import ExploratoryAnalysis
from rag.vector_store import VectorStore
from rag.retriever import RAGRetriever
from candidate_selection_system import CandidateSelectionSystem

# Page configuration
st.set_page_config(
    page_title="TalentSelect AI - Sélection Intelligente de Candidats",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Main styling */
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
        color: #667eea;
        font-weight: 700;
        font-size: 1.8rem;
        padding: 1rem 0;
        border-bottom: 3px solid #667eea;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1.5rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card h3 {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .metric-value {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Text input styling */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Success/Error/Warning message styling */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #047857;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #b91c1c;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #b45309;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #1d4ed8;
    }
    
    /* Agent card styling */
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-top: 3px solid #667eea;
    }
    
    .agent-card h4 {
        color: #667eea;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Step indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        margin: 0 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-top: 3px solid #667eea;
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.5rem;
        font-weight: 700;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 8px;
        font-weight: 600;
        color: #667eea;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border: none;
    }
    
    /* Section header */
    .section-header {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_candidates' not in st.session_state:
    st.session_state.processed_candidates = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'evaluation_results' not in st.session_state:
    st.session_state.evaluation_results = []


def load_and_process_candidates():
    """Load and process candidate documents."""
    # Use path relative to app.py location
    data_dir = BASE_DIR / "data" / "raw"
    loader = DataLoader(str(data_dir))
    processor = TextProcessor()
    
    candidates = loader.load_all_candidates()
    processed = []
    
    for candidate in candidates:
        processed_candidate = processor.process_candidate(candidate)
        processed.append(processed_candidate)
    
    return processed


def initialize_vector_store(candidates):
    """Initialize the vector store with candidates."""
    vector_store = VectorStore()
    vector_store.clear_collection()
    vector_store.add_candidates(candidates)
    return vector_store


def main():
    # Professional Header
    st.markdown("""
        <div class="main-header">
            <h1>🎀 TalentSelect AI</h1>
            <p>Système Multi-Agents pour la Sélection Intelligente de Candidats</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Professional Sidebar
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #667eea; font-size: 1.8rem; font-weight: 700; margin-bottom: 2rem;">
                Navigation
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.radio(
        "Choisir une section",
        ["🏠 Accueil", "Analyse Exploratoire", "Évaluation Multi-Agents", "📈 Résultats"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Sidebar info
    if st.session_state.processed_candidates:
        st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; color: white; margin-top: 2rem;">
                <strong>📊 Statut</strong><br>
                <small>{len(st.session_state.processed_candidates)} candidats chargés</small>
            </div>
        """, unsafe_allow_html=True)
    
    if page == "🏠 Accueil":
        show_home_page()
    elif page == "Analyse Exploratoire":
        show_exploratory_analysis()
    elif page == "Évaluation Multi-Agents":
        show_evaluation_page()
    elif page == "📈 Résultats":
        show_results_page()


def show_home_page():
    """Display the home page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 3rem;">
                <h2 style="color: #667eea; font-size: 2rem; font-weight: 700;">
                    Bienvenue dans TalentSelect AI
                </h2>
                <p style="color: #6b7280; font-size: 1.1rem; margin-top: 1rem;">
                    Solution intelligente de recrutement basée sur l'intelligence artificielle
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Objective Card
    st.markdown("""
        <div class="info-card">
            <h3 style="color: #667eea; margin-bottom: 1rem; font-size: 1.5rem;">🎯 Objectif du Système</h3>
            <p style="color: #4b5563; line-height: 1.8; font-size: 1.05rem;">
                TalentSelect AI utilise une architecture multi-agents avancée pour automatiser et expliquer 
                le processus de sélection des candidats à partir de CVs, lettres de motivation et profils LinkedIn. 
                Notre système combine l'intelligence artificielle avec la transparence pour vous aider à prendre 
                les meilleures décisions de recrutement.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Agents Section
    st.markdown('<div class="section-header"> Architecture Multi-Agents</div>', unsafe_allow_html=True)
    
    agents_data = [
        {"name": "Agent RH", "icon": "👔", "description": "Analyse les descriptions de poste et les critères du recruteur", "color": "#667eea"},
        {"name": "Agent Profil", "icon": "📋", "description": "Analyse les CVs et lettres de motivation (NER, scoring, extraction de compétences)", "color": "#10b981"},
        {"name": "Agent Technique", "icon": "💻", "description": "Évalue les compétences techniques selon les exigences du poste", "color": "#3b82f6"},
        {"name": "Agent Soft Skills", "icon": "🤝", "description": "Évalue les qualités interpersonnelles et l'adéquation culturelle", "color": "#f59e0b"},
        {"name": "Agent Décideur", "icon": "⚖️", "description": "Agrège les avis et génère un rapport final explicable", "color": "#8b5cf6"}
    ]
    
    # Display agents in a grid
    for i in range(0, len(agents_data), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(agents_data):
                agent = agents_data[i + j]
                with col:
                    st.markdown(f"""
                        <div class="agent-card" style="border-top-color: {agent['color']};">
                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                <span style="font-size: 2rem; margin-right: 0.5rem;">{agent['icon']}</span>
                                <h4 style="color: {agent['color']}; margin: 0;">{agent['name']}</h4>
                            </div>
                            <p style="color: #6b7280; margin: 0; line-height: 1.6;">{agent['description']}</p>
                        </div>
                    """, unsafe_allow_html=True)
    
    # How to Use Section
    st.markdown('<div class="section-header">📖 Guide d\'utilisation</div>', unsafe_allow_html=True)
    
    steps = [
        {"number": "1", "title": "Analyse Exploratoire", "description": "Chargez vos données et explorez les statistiques détaillées de vos candidats", "icon": "📊"},
        {"number": "2", "title": "Évaluation Multi-Agents", "description": "Définissez un poste et laissez nos agents IA évaluer les candidats", "icon": "🤖"},
        {"number": "3", "title": "Résultats", "description": "Consultez le classement final avec justifications détaillées pour chaque candidat", "icon": "📈"}
    ]
    
    step_cols = st.columns(3)
    for idx, (col, step) in enumerate(zip(step_cols, steps)):
        with col:
            st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                           box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-align: center; 
                           border-top: 3px solid #667eea; height: 100%;">
                    <div style="width: 50px; height: 50px; border-radius: 50%; 
                               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               color: white; display: flex; align-items: center; 
                               justify-content: center; margin: 0 auto 1rem; font-weight: 700; font-size: 1.5rem;">
                        {step['number']}
                    </div>
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{step['icon']}</div>
                    <h4 style="color: #667eea; margin-bottom: 0.5rem; font-size: 1.2rem;">{step['title']}</h4>
                    <p style="color: #6b7280; font-size: 0.95rem; line-height: 1.6;">{step['description']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Data Structure Section
    st.markdown('<div class="section-header">📁 Structure des Données</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="info-card" style="border-left-color: #10b981;">
                <h4 style="color: #10b981; margin-bottom: 1rem;">📄 Fichiers de Candidats</h4>
                <p style="color: #4b5563; margin-bottom: 0.5rem;"><strong>Emplacement:</strong> <code>data/raw/</code></p>
                <p style="color: #4b5563; margin-bottom: 0.5rem;"><strong>Formats supportés:</strong> PDF, DOCX, TXT</p>
                <p style="color: #4b5563; margin: 0;"><strong>Nommage suggéré:</strong> <code>candidate_001.pdf</code>, <code>CV_002.pdf</code></p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card" style="border-left-color: #3b82f6;">
                <h4 style="color: #3b82f6; margin-bottom: 1rem;">💼 Descriptions de Postes</h4>
                <p style="color: #4b5563; margin-bottom: 0.5rem;"><strong>Emplacement:</strong> <code>data/job_descriptions/</code></p>
                <p style="color: #4b5563; margin-bottom: 0.5rem;"><strong>Format:</strong> Fichiers texte (.txt)</p>
                <p style="color: #4b5563; margin: 0;">Vous pouvez également saisir directement la description dans l'interface.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Credits Section
    st.markdown("""
        <hr style="border: none; height: 2px; background: linear-gradient(90deg, transparent, #667eea, transparent); margin: 3rem 0;">
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
                   padding: 2rem; border-radius: 15px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                   margin-top: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="color: #667eea; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">
                    👨‍💻 Développé par
                </h3>
            </div>
    """, unsafe_allow_html=True)
    
    # Display developers in a grid using Streamlit columns
    dev_cols = st.columns(4)
    
    developers = [
        {"name": "Laila AIT BIHI", "email": "laila.aitbihi@centrale-casablanca.ma", "color": "#667eea"},
        {"name": "Chaymae DAHHASSI", "email": "chaymae.dahhassi@centrale-casablanca.ma", "color": "#10b981"},
        {"name": "Salma BOUCHAMA", "email": "salma.bouchama@centrale-casablanca.ma", "color": "#3b82f6"},
        {"name": "Chaima AL AYACHI", "email": "chaima.alayachi@centrale-casablanca.ma", "color": "#f59e0b"}
    ]
    
    for col, dev in zip(dev_cols, developers):
        with col:
            st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                           box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-align: center;
                           border-top: 3px solid {dev['color']}; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">👩‍💻</div>
                    <h4 style="color: {dev['color']}; margin-bottom: 0.5rem; font-size: 1.1rem;">{dev['name']}</h4>
                    <p style="color: #6b7280; font-size: 0.9rem; margin: 0;">
                        <a href="mailto:{dev['email']}" 
                           style="color: {dev['color']}; text-decoration: none;">
                            {dev['email']}
                        </a>
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
            <div style="text-align: center; padding-top: 2rem; border-top: 2px solid #e5e7eb;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       padding: 2.5rem; border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); 
                       color: white; text-align: center; margin: 2rem 0;">
                <p style="color: white; font-size: 1.8rem; font-weight: 700; margin: 0;">
                    École Centrale Casablanca
                </p>
                <p style="color: rgba(255, 255, 255, 0.95); font-size: 1.2rem; margin-top: 0.8rem; margin-bottom: 0;">
                    Grande École d'Ingénieurs
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)


def show_exploratory_analysis():
    """Display exploratory analysis page."""
    st.markdown('<div class="section-header"> Analyse Exploratoire des Données</div>', unsafe_allow_html=True)
    
    # Load Data Section
    st.markdown("""
        <div class="info-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">📥 Chargement des Données</h3>
            <p style="color: #6b7280; margin-bottom: 1rem;">
                Chargez et traitez les candidats depuis le dossier <code>data/raw/</code>. 
                Le système analysera automatiquement tous les documents disponibles.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Charger et Traiter les Candidats", type="primary", use_container_width=True):
            with st.spinner("Chargement et traitement des candidats en cours..."):
                # Debug: Check if directory exists (using BASE_DIR)
                data_path = BASE_DIR / "data" / "raw"
                if not data_path.exists():
                    st.error(f"❌ Le dossier '{data_path}' n'existe pas!")
                    st.info(f"📁 Répertoire de base (app.py): {BASE_DIR}")
                    st.info(f"📁 Répertoire actuel: {os.getcwd()}")
                    st.info(f"📂 Contenu du répertoire de base: {', '.join(os.listdir(BASE_DIR)) if BASE_DIR.exists() else 'N/A'}")
                else:
                    files_in_dir = [f.name for f in data_path.iterdir() if f.is_file()]
                    if not files_in_dir:
                        st.warning(f"⚠️ Le dossier '{data_path}' existe mais est vide!")
                        st.info("💡 Assurez-vous que les fichiers candidate_*.txt sont dans le dépôt GitHub.")
                    else:
                        st.info(f"📁 Fichiers trouvés dans {data_path}: {', '.join(files_in_dir[:5])}{'...' if len(files_in_dir) > 5 else ''}")
                
                candidates = load_and_process_candidates()
                st.session_state.processed_candidates = candidates
                
                if candidates:
                    st.success(f"✅ {len(candidates)} candidats chargés avec succès!")
                    
                    # Initialize vector store
                    st.session_state.vector_store = initialize_vector_store(candidates)
                    st.success("✅ Base vectorielle initialisée!")
                    st.rerun()
                else:
                    st.warning("⚠️ Aucun candidat trouvé. Vérifiez que les fichiers sont dans data/raw/")
                    st.info("💡 Les fichiers doivent être dans le dépôt GitHub pour être disponibles sur Streamlit Cloud.")
    
    if st.session_state.processed_candidates:
        st.markdown('<div class="section-header">📈 Statistiques des Candidats</div>', unsafe_allow_html=True)
        
        # Create DataFrame
        analysis = ExploratoryAnalysis()
        df = analysis.create_dataframe(st.session_state.processed_candidates)
        
        # Display summary
        summary = analysis.generate_summary_statistics()
        
        # Enhanced Metrics
        col1, col2, col3 = st.columns(3)
        metrics = [
            ("Total Candidats", summary.get('total_candidates', 0), "👥", "#667eea"),
            ("Compétences Techniques Moy.", f"{summary.get('avg_technical_skills', 0):.1f}", "💻", "#3b82f6"),
            ("Soft Skills Moy.", f"{summary.get('avg_soft_skills', 0):.1f}", "🤝", "#f59e0b")
        ]
        
        for col, (label, value, icon, color) in zip([col1, col2, col3], metrics):
            with col:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                               padding: 1.5rem; border-radius: 10px; color: white; 
                               text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                        <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">{value}</div>
                        <div style="font-size: 0.9rem; opacity: 0.9;">{label}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">📋 Données des Candidats</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Skill distribution
        st.markdown('<div class="section-header">🎯 Analyse des Compétences</div>', unsafe_allow_html=True)
        skill_dist = analysis.analyze_skill_distribution()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <h4 style="color: #667eea; margin-bottom: 1rem; font-size: 1.3rem;">
                    💻 Top Compétences Techniques
                </h4>
            """, unsafe_allow_html=True)
            if skill_dist.get('top_technical_skills'):
                tech_df = pd.DataFrame(
                    list(skill_dist['top_technical_skills'].items()),
                    columns=['Compétence', 'Nombre de Candidats']
                )
                fig = px.bar(
                    tech_df, 
                    x='Compétence', 
                    y='Nombre de Candidats',
                    color='Nombre de Candidats',
                    color_continuous_scale='blues',
                    title=""
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#4b5563'),
                    showlegend=False,
                    height=400
                )
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée de compétences techniques disponible")
        
        with col2:
            st.markdown("""
                <h4 style="color: #667eea; margin-bottom: 1rem; font-size: 1.3rem;">
                    🤝 Top Soft Skills
                </h4>
            """, unsafe_allow_html=True)
            if skill_dist.get('top_soft_skills'):
                soft_df = pd.DataFrame(
                    list(skill_dist['top_soft_skills'].items()),
                    columns=['Compétence', 'Nombre de Candidats']
                )
                fig = px.bar(
                    soft_df, 
                    x='Compétence', 
                    y='Nombre de Candidats',
                    color='Nombre de Candidats',
                    color_continuous_scale='greens',
                    title=""
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#4b5563'),
                    showlegend=False,
                    height=400
                )
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Aucune donnée de soft skills disponible")
        
        # Generate report
        st.markdown('<div class="section-header">📄 Rapport d\'Analyse</div>', unsafe_allow_html=True)
        if st.button("📄 Générer Rapport d'Analyse Complet", type="primary"):
            with st.spinner("Génération du rapport en cours..."):
                report = analysis.generate_report()
                st.markdown("""
                    <div class="info-card">
                        <h4 style="color: #667eea; margin-bottom: 1rem;">Rapport d'Analyse</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.text_area("", report, height=400, label_visibility="collapsed")


def show_evaluation_page():
    """Display the evaluation page."""
    st.markdown('<div class="section-header"> Évaluation Multi-Agents</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-card">
            <p style="color: #6b7280; line-height: 1.8; margin: 0;">
                Définissez votre poste à pourvoir et laissez nos 5 agents IA spécialisés analyser 
                et évaluer vos candidats de manière transparente et explicable.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Job description input
    st.markdown("""
        <h3 style="color: #667eea; margin: 2rem 0 1rem; font-size: 1.5rem;">
            📝 Description du Poste
        </h3>
    """, unsafe_allow_html=True)
    
    # Load available job descriptions (using BASE_DIR)
    job_descriptions_dir = BASE_DIR / "data" / "job_descriptions"
    available_jobs = []
    if job_descriptions_dir.exists():
        available_jobs = [f.name for f in job_descriptions_dir.iterdir() if f.is_file() and f.suffix == '.txt']
        available_jobs.sort()
    
    # Initialize job description in session state if not exists
    if 'current_job_description' not in st.session_state:
        st.session_state.current_job_description = ""
    if 'last_selected_job' not in st.session_state:
        st.session_state.last_selected_job = None
    
    # Job description selection
    if available_jobs:
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_job_file = st.selectbox(
                "📋 Choisir une description de poste existante:",
                ["-- Nouvelle description --"] + available_jobs,
                help="Sélectionnez une description de poste pré-définie ou créez-en une nouvelle",
                key="job_selector"
            )
        
        with col2:
            if st.button("🔄 Recharger"):
                st.session_state.current_job_description = ""
                st.session_state.last_selected_job = None
                st.rerun()
        
        # Load selected job description
        if selected_job_file and selected_job_file != "-- Nouvelle description --":
            # Load only if a different file is selected
            if st.session_state.last_selected_job != selected_job_file:
                loader = DataLoader()
                job_file_path = BASE_DIR / "data" / "job_descriptions" / selected_job_file
                loaded_description = loader.load_text(str(job_file_path)) if job_file_path.exists() else ""
                if loaded_description:
                    st.session_state.current_job_description = loaded_description
                    st.session_state.last_selected_job = selected_job_file
                    st.success(f"✅ Description chargée : {selected_job_file}")
                else:
                    st.warning(f"⚠️ Impossible de charger {selected_job_file}")
            else:
                # Ensure we have the description loaded
                if not st.session_state.current_job_description:
                    loader = DataLoader()
                    job_file_path = BASE_DIR / "data" / "job_descriptions" / selected_job_file
                    loaded_description = loader.load_text(str(job_file_path)) if job_file_path.exists() else ""
                    if loaded_description:
                        st.session_state.current_job_description = loaded_description
            
            # Display the loaded file info
            st.caption(f"📄 Fichier actuel : {selected_job_file}")
            
            # Show preview of loaded description (read-only)
            if st.session_state.current_job_description:
                with st.expander("📋 Aperçu de la description chargée", expanded=False):
                    st.text(st.session_state.current_job_description[:500] + ("..." if len(st.session_state.current_job_description) > 500 else ""))
            
            # Use the loaded description directly
            current_job_desc = st.session_state.current_job_description.strip()
        else:
            # Reset if "Nouvelle description" is selected
            if st.session_state.last_selected_job is not None:
                st.session_state.current_job_description = ""
                st.session_state.last_selected_job = None
            
            # Show text area only for manual input
            st.subheader("📝 Saisie manuelle de la description")
            job_description = st.text_area(
                "Description du poste et critères de sélection:",
                value=st.session_state.current_job_description,
                height=200,
                placeholder="Exemple: Data Scientist avec 2 ans d'expérience, maîtrise Python et Power BI...",
                help="Saisissez la description du poste et les critères de sélection",
                key="job_description_input"
            )
            
            # Update session state when user edits
            st.session_state.current_job_description = job_description if job_description else ""
            
            # Use the manually entered description
            current_job_desc = job_description.strip() if job_description else ""
    else:
        st.info("ℹ️ Aucune description de poste trouvée dans data/job_descriptions/")
        # Show text area for manual input if no files available
        job_description = st.text_area(
            "📝 Description du poste et critères de sélection:",
            value=st.session_state.current_job_description,
            height=200,
            placeholder="Exemple: Data Scientist avec 2 ans d'expérience, maîtrise Python et Power BI...",
            help="Saisissez la description du poste et les critères de sélection",
            key="job_description_input"
        )
        # Update session state
        st.session_state.current_job_description = job_description if job_description else ""
        current_job_desc = job_description.strip() if job_description else ""
    
    # RAG-based candidate retrieval
    if st.session_state.vector_store and current_job_desc:
        st.markdown("""
            <h3 style="color: #667eea; margin: 2rem 0 1rem; font-size: 1.5rem;">
                🔍 Recherche de Candidats Pertinents (RAG)
            </h3>
        """, unsafe_allow_html=True)
        
        retriever = RAGRetriever(st.session_state.vector_store)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            top_k = st.slider(
                "Nombre de candidats à évaluer", 
                1, len(st.session_state.processed_candidates), 5,
                help="Sélectionnez le nombre de candidats que vous souhaitez évaluer"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔎 Rechercher Candidats Pertinents", use_container_width=True, type="primary"):
                with st.spinner("Recherche de candidats pertinents en cours..."):
                    retrieved = retriever.retrieve_by_job_requirements(current_job_desc, top_k=top_k)
                    
                    if retrieved:
                        st.success(f"✅ {len(retrieved)} candidats pertinents trouvés!")
                        
                        # Show retrieved candidates
                        for i, candidate in enumerate(retrieved, 1):
                            with st.expander(f"🎯 Candidat {candidate['candidate_id']} (Score de pertinence: {1-candidate['distance']:.2%})"):
                                st.markdown(f"""
                                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; 
                                               border-left: 3px solid #667eea;">
                                        <p style="color: #4b5563; line-height: 1.8;">
                                            {candidate['content'][:500]}...
                                        </p>
                                    </div>
                                """, unsafe_allow_html=True)
    
    # Evaluation
    st.markdown("""
        <h3 style="color: #667eea; margin: 2rem 0 1rem; font-size: 1.5rem;">
            ⚙️ Évaluation des Candidats
        </h3>
    """, unsafe_allow_html=True)
    
    if not st.session_state.processed_candidates:
        st.warning("⚠️ Veuillez d'abord charger les candidats dans la section 'Analyse Exploratoire'")
    else:
        # Select candidates to evaluate
        st.markdown("""
            <div class="info-card">
                <p style="color: #6b7280; margin: 0;">
                    Sélectionnez les candidats que vous souhaitez évaluer. 
                    Notre système multi-agents analysera chaque candidat de manière approfondie.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        candidate_ids = [c['candidate_id'] for c in st.session_state.processed_candidates]
        selected_ids = st.multiselect(
            "Sélectionner les candidats à évaluer",
            candidate_ids,
            default=candidate_ids[:min(5, len(candidate_ids))],
            help="Vous pouvez sélectionner plusieurs candidats pour évaluation"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Lancer l'Évaluation Multi-Agents", type="primary", use_container_width=True):
                # Get the current job description from session state (always up to date)
                eval_job_description = st.session_state.current_job_description.strip()
                
                if not eval_job_description:
                    st.error("❌ Veuillez entrer une description de poste ou sélectionner un fichier")
                elif not selected_ids:
                    st.error("❌ Veuillez sélectionner au moins un candidat")
                else:
                    selected_candidates = [
                        c for c in st.session_state.processed_candidates
                        if c['candidate_id'] in selected_ids
                    ]
                    
                    # Initialize system
                    try:
                        with st.spinner("Initialisation du système multi-agents..."):
                            # Ensure patch is applied before initialization
                            patch_langchain_groq()
                            system = CandidateSelectionSystem()
                    except Exception as e:
                        error_msg = str(e)
                        error_info = parse_rate_limit_error(error_msg)
                        
                        # Check for rate limit error first
                        if error_info.get('is_rate_limit'):
                            st.error("""
                            ## ⏰ Quota API Dépassé
                            
                            **Le quota quotidien de l'API a été atteint.**
                            
                            Veuillez patienter avant de relancer une évaluation. Le quota se réinitialise automatiquement.
                            """)
                            
                            if error_info.get('wait_time'):
                                st.info(f"⏱️ **Temps d'attente estimé :** {error_info['wait_time']}")
                            
                            if error_info.get('limit') and error_info.get('used'):
                                st.info(f"📊 **Quota :** {error_info['used']} / {error_info['limit']} tokens utilisés aujourd'hui")
                            
                            st.markdown("""
                            ---
                            **Que faire ?**
                            - ⏳ Attendez quelques minutes et réessayez
                            - 🔄 Le quota se réinitialise à minuit (UTC)
                            - 💡 Pour une limite plus élevée, contactez l'administrateur du système
                            """)
                        else:
                            st.error(f"❌ Erreur lors de l'initialisation: {error_msg}")
                            
                            # Provide specific help based on error type
                            if 'proxies' in error_msg.lower():
                                st.error("""
                                **Erreur liée aux proxies détectée.**
                                
                                Cette erreur est causée par une incompatibilité entre `langchain-groq` et `groq`.
                                Le patch devrait normalement corriger ce problème. Si l'erreur persiste :
                                
                                1. Vérifiez que `groq_patch.py` est bien importé en premier
                                2. Redéployez l'application
                                3. Vérifiez que les versions dans `requirements.txt` sont correctes
                                """)
                            elif 'GROQ_API_KEY' in error_msg or 'api_key' in error_msg.lower():
                                st.info("💡 Assurez-vous que GROQ_API_KEY est défini dans vos secrets Streamlit (Streamlit Cloud) ou dans votre fichier .env (local)")
                            else:
                                st.info("💡 Vérifiez les logs pour plus de détails sur l'erreur")
                            
                            import traceback
                            with st.expander("🔍 Détails de l'erreur"):
                                st.code(traceback.format_exc())
                        return
                    
                    # Evaluate candidates
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results = []
                    for i, candidate in enumerate(selected_candidates):
                        status_text.text(f"Évaluation du candidat {candidate['candidate_id']} ({i+1}/{len(selected_candidates)})...")
                        progress_bar.progress((i + 1) / len(selected_candidates))
                        
                        try:
                            evaluation = system.evaluate_candidate(candidate, eval_job_description)
                            results.append(evaluation)
                        except Exception as e:
                            error_info = parse_rate_limit_error(e)
                            
                            if error_info['is_rate_limit']:
                                # Display user-friendly rate limit message
                                st.error("""
                                ## ⏰ Quota API Dépassé
                                
                                **Le quota quotidien de l'API a été atteint.**
                                
                                Veuillez patienter avant de relancer une évaluation. Le quota se réinitialise automatiquement.
                                """)
                                
                                if error_info.get('wait_time'):
                                    st.info(f"⏱️ **Temps d'attente estimé :** {error_info['wait_time']}")
                                
                                if error_info.get('limit') and error_info.get('used'):
                                    st.info(f"📊 **Quota :** {error_info['used']} / {error_info['limit']} tokens utilisés aujourd'hui")
                                
                                st.markdown("""
                                ---
                                **Que faire ?**
                                - ⏳ Attendez quelques minutes et réessayez
                                - 🔄 Le quota se réinitialise à minuit (UTC)
                                - 💡 Pour une limite plus élevée, contactez l'administrateur du système
                                """)
                                
                                # Stop evaluation process
                                break
                            else:
                                # Other errors
                                st.error(f"❌ Erreur lors de l'évaluation du candidat {candidate['candidate_id']}: {str(e)[:200]}")
                            continue
                    
                    st.session_state.evaluation_results = results
                    if results:
                        st.success(f"✅ Évaluation terminée pour {len(results)} candidats!")
                        # Show results immediately
                        show_evaluation_results(results)
                    else:
                        # Check if we stopped due to rate limit
                        rate_limit_detected = any(
                            'error' in r and parse_rate_limit_error(r.get('error', '')).get('is_rate_limit', False)
                            for r in results
                        )
                        if not rate_limit_detected:
                            st.warning("⚠️ Aucune évaluation n'a pu être complétée")


def parse_rate_limit_error(error_msg):
    """Parse rate limit error and extract useful information for users."""
    error_str = str(error_msg)
    
    # Check if it's a rate limit error (429 or rate_limit_exceeded)
    is_rate_limit = (
        '429' in error_str or 
        'rate limit' in error_str.lower() or 
        'Rate limit' in error_str or
        'rate_limit_exceeded' in error_str.lower()
    )
    
    if is_rate_limit:
        # Try to extract wait time (format: "20m12.192s" or "20m 12s" etc.)
        wait_time_match = re.search(r'Please try again in ([\dhm\s.]+s?)', error_str, re.IGNORECASE)
        if not wait_time_match:
            # Try alternative format
            wait_time_match = re.search(r'try again in ([\dhm\s.]+s?)', error_str, re.IGNORECASE)
        wait_time = wait_time_match.group(1).strip() if wait_time_match else None
        
        # Try to extract limit info
        limit_match = re.search(r'Limit (\d+)', error_str)
        used_match = re.search(r'Used (\d+)', error_str)
        
        limit = limit_match.group(1) if limit_match else None
        used = used_match.group(1) if used_match else None
        
        return {
            'is_rate_limit': True,
            'wait_time': wait_time,
            'limit': limit,
            'used': used
        }
    
    return {'is_rate_limit': False}


def parse_final_decision(final_decision_str):
    """Parse the final decision JSON string into a readable format."""
    if not final_decision_str or final_decision_str == 'N/A':
        return None
    
    # Convert to string if it's not already
    if not isinstance(final_decision_str, str):
        final_decision_str = str(final_decision_str)
    
    # Remove HTML tags
    final_decision_str = re.sub(r'<[^>]+>', '', final_decision_str)
    
    # Remove markdown code blocks if present
    final_decision_str = re.sub(r'```json\s*', '', final_decision_str)
    final_decision_str = re.sub(r'```\s*', '', final_decision_str)
    
    # Try multiple strategies to extract JSON
    json_candidates = []
    
    # Strategy 1: Try to parse the entire string as JSON
    try:
        return json.loads(final_decision_str.strip())
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Strategy 2: Find JSON object using balanced braces
    brace_count = 0
    start_idx = -1
    for i, char in enumerate(final_decision_str):
        if char == '{':
            if brace_count == 0:
                start_idx = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_idx != -1:
                json_candidates.append(final_decision_str[start_idx:i+1])
                start_idx = -1
    
    # Strategy 3: Use regex as fallback (less reliable but catches edge cases)
    if not json_candidates:
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', final_decision_str, re.DOTALL)
        if json_match:
            json_candidates.append(json_match.group(0))
    
    # Try to parse each candidate
    for json_str in json_candidates:
        try:
            # Clean up common issues
            json_str = json_str.strip()
            # Remove trailing commas before closing braces/brackets
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            
            decision_data = json.loads(json_str)
            if isinstance(decision_data, dict) and len(decision_data) > 0:
                return decision_data
        except (json.JSONDecodeError, ValueError):
            continue
    
    # If all strategies fail, try to extract key-value pairs manually
    try:
        # Extract final_score
        score_match = re.search(r'"final_score"\s*:\s*(\d+(?:\.\d+)?)', final_decision_str)
        ranking_match = re.search(r'"ranking"\s*:\s*(\d+)', final_decision_str)
        recommendation_match = re.search(r'"recommendation"\s*:\s*"([^"]+)"', final_decision_str)
        
        if score_match or ranking_match or recommendation_match:
            result = {}
            if score_match:
                result['final_score'] = float(score_match.group(1))
            if ranking_match:
                result['ranking'] = int(ranking_match.group(1))
            if recommendation_match:
                result['recommendation'] = recommendation_match.group(1)
            if result:
                return result
    except Exception:
        pass
    
    # Last resort: return None to trigger fallback
    return None


def show_evaluation_results(results):
    """Display evaluation results."""
    if not results:
        return
    
    st.markdown("""
        <h3 style="color: #667eea; margin: 2rem 0 1rem; font-size: 1.8rem;">
            📊 Résultats de l'Évaluation
        </h3>
    """, unsafe_allow_html=True)
    
    # Extract and parse scores from final_decision
    results_df = []
    for result in results:
        candidate_id = result.get('candidate_id', 'Unknown')
        final_decision = result.get('final_decision', result.get('error', 'N/A'))
        
        # Check if there's an error
        if 'error' in result:
            error_info = parse_rate_limit_error(result.get('error', ''))
            if error_info.get('is_rate_limit'):
                results_df.append({
                    'Candidat': candidate_id,
                    'Score Final': 'Quota dépassé',
                    'Rang': 'N/A',
                    'Statut': '⏰ Quota API atteint'
                })
            else:
                results_df.append({
                    'Candidat': candidate_id,
                    'Score Final': 'Erreur',
                    'Rang': 'N/A',
                    'Statut': 'Erreur d\'évaluation'
                })
            continue
        
        # Parse the decision
        decision_data = parse_final_decision(final_decision)
        
        # Extract readable information
        if decision_data and isinstance(decision_data, dict):
            score = decision_data.get('final_score', decision_data.get('score', None))
            ranking = decision_data.get('ranking', decision_data.get('rank', None))
            status = decision_data.get('recommendation', decision_data.get('status', None))
            
            # Format the status nicely
            if isinstance(status, list) and len(status) > 0:
                status = status[0]
            if isinstance(status, str):
                status = status.replace('_', ' ').title()
            
            # Format ranking
            if isinstance(ranking, (int, float)):
                ranking = f"Rang {int(ranking)}"
            elif isinstance(ranking, str) and ranking.lower() != 'n/a':
                ranking = ranking.title()
            else:
                ranking = 'N/A'
            
            # Format score
            if isinstance(score, (int, float)):
                score_str = f"{int(score)}/100"
            elif score is not None:
                score_str = str(score)
            else:
                score_str = 'N/A'
            
            results_df.append({
                'Candidat': candidate_id,
                'Score Final': score_str,
                'Rang': ranking,
                'Statut': status if status else 'N/A'
            })
        else:
            # Fallback if parsing fails - try to show raw data for debugging
            # Log the issue for debugging (only in development)
            import sys
            if hasattr(sys, '_getframe'):
                print(f"⚠️ Warning: Could not parse final_decision for candidate {candidate_id}")
                print(f"   Raw decision (first 200 chars): {str(final_decision)[:200]}")
            
            results_df.append({
                'Candidat': candidate_id,
                'Score Final': 'N/A',
                'Rang': 'N/A',
                'Statut': 'Format invalide'
            })
    
    # Display summary table
    summary_df = pd.DataFrame(results_df)
    if not summary_df.empty:
        # Sort by score if available
        if 'Score Final' in summary_df.columns:
            summary_df['Score_Num'] = summary_df['Score Final'].str.extract(r'(\d+)').astype(float)
            summary_df = summary_df.sort_values('Score_Num', ascending=False, na_position='last')
            summary_df = summary_df.drop('Score_Num', axis=1)
        
        st.dataframe(summary_df, use_container_width=True, height=300)
    
    # Detailed view
    st.markdown("""
        <h3 style="color: #667eea; margin: 2rem 0 1rem; font-size: 1.8rem;">
            📋 Détails par Candidat
        </h3>
    """, unsafe_allow_html=True)
    
    for result in results:
        candidate_id = result.get('candidate_id', 'Unknown')
        with st.expander(f"👤 Candidat {candidate_id} - Voir les détails", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div style="background: white; padding: 1rem; border-radius: 8px; 
                               border-left: 3px solid #667eea; margin-bottom: 1rem;">
                        <h4 style="color: #667eea; margin-bottom: 0.5rem;">👔 Analyse du Poste</h4>
                    </div>
                """, unsafe_allow_html=True)
                job_analysis = result.get('job_analysis', 'N/A')
                if isinstance(job_analysis, str):
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{job_analysis[:500]}{'...' if len(job_analysis) > 500 else ''}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{str(job_analysis)[:500]}</p>", unsafe_allow_html=True)
                
                st.markdown("""
                    <div style="background: white; padding: 1rem; border-radius: 8px; 
                               border-left: 3px solid #10b981; margin-bottom: 1rem;">
                        <h4 style="color: #10b981; margin-bottom: 0.5rem;">📋 Évaluation Profil</h4>
                    </div>
                """, unsafe_allow_html=True)
                profile_eval = result.get('profile_evaluation', 'N/A')
                if isinstance(profile_eval, str):
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{profile_eval[:500]}{'...' if len(profile_eval) > 500 else ''}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{str(profile_eval)[:500]}</p>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div style="background: white; padding: 1rem; border-radius: 8px; 
                               border-left: 3px solid #3b82f6; margin-bottom: 1rem;">
                        <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">💻 Évaluation Technique</h4>
                    </div>
                """, unsafe_allow_html=True)
                tech_eval = result.get('technical_evaluation', 'N/A')
                if isinstance(tech_eval, str):
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{tech_eval[:500]}{'...' if len(tech_eval) > 500 else ''}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{str(tech_eval)[:500]}</p>", unsafe_allow_html=True)
                
                st.markdown("""
                    <div style="background: white; padding: 1rem; border-radius: 8px; 
                               border-left: 3px solid #f59e0b; margin-bottom: 1rem;">
                        <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">🤝 Évaluation Soft Skills</h4>
                    </div>
                """, unsafe_allow_html=True)
                soft_eval = result.get('soft_skills_evaluation', 'N/A')
                if isinstance(soft_eval, str):
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{soft_eval[:500]}{'...' if len(soft_eval) > 500 else ''}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.8;'>{str(soft_eval)[:500]}</p>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
                    <h4 style="color: white; margin-bottom: 0.5rem;">⚖️ Décision Finale</h4>
                </div>
            """, unsafe_allow_html=True)
            
            final_decision = result.get('final_decision', result.get('error', 'N/A'))
            
            # Check for errors first
            if 'error' in result:
                error_msg = result.get('error', 'Erreur inconnue')
                error_info = parse_rate_limit_error(error_msg)
                
                if error_info.get('is_rate_limit'):
                    st.error("""
                    ## ⏰ Quota API Dépassé
                    
                    **Le quota quotidien de l'API a été atteint pour ce candidat.**
                    
                    Veuillez patienter avant de relancer une évaluation. Le quota se réinitialise automatiquement.
                    """)
                    
                    if error_info.get('wait_time'):
                        st.info(f"⏱️ **Temps d'attente estimé :** {error_info['wait_time']}")
                    
                    if error_info.get('limit') and error_info.get('used'):
                        st.info(f"📊 **Quota :** {error_info['used']} / {error_info['limit']} tokens utilisés aujourd'hui")
                    
                    st.markdown("""
                    ---
                    **Que faire ?**
                    - ⏳ Attendez quelques minutes et réessayez
                    - 🔄 Le quota se réinitialise à minuit (UTC)
                    - 💡 Pour une limite plus élevée, contactez l'administrateur du système
                    """)
                else:
                    st.error(f"❌ Erreur lors de l'évaluation: {str(error_msg)[:200]}")
                return
            
            decision_data = parse_final_decision(final_decision)
            
            if decision_data and isinstance(decision_data, dict):
                # Display parsed decision in a readable format
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    score = decision_data.get('final_score', decision_data.get('score', 'N/A'))
                    score_color = '#10b981' if isinstance(score, (int, float)) and score >= 80 else '#f59e0b' if isinstance(score, (int, float)) and score >= 60 else '#ef4444'
                    st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                                   box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-align: center;
                                   border-top: 3px solid {score_color};">
                            <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 0.5rem;">Score Final</div>
                            <div style="font-size: 2rem; font-weight: 700; color: {score_color};">
                                {score if score != 'N/A' else 'N/A'}
                                {('/100' if isinstance(score, (int, float)) else '')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    ranking = decision_data.get('ranking', decision_data.get('rank', 'N/A'))
                    if isinstance(ranking, (int, float)):
                        ranking_display = f"Rang {int(ranking)}"
                    else:
                        ranking_display = str(ranking).title() if ranking != 'N/A' else 'N/A'
                    
                    st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                                   box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-align: center;
                                   border-top: 3px solid #3b82f6;">
                            <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 0.5rem;">Rang</div>
                            <div style="font-size: 1.5rem; font-weight: 700; color: #3b82f6;">
                                {ranking_display}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    status = decision_data.get('status', decision_data.get('recommendation', 'N/A'))
                    if isinstance(status, list) and len(status) > 0:
                        status = status[0]
                    if isinstance(status, str) and status != 'N/A':
                        status_display = status.replace('_', ' ').title()
                    else:
                        status_display = 'N/A'
                    
                    status_color = '#10b981' if 'recommand' in status_display.lower() else '#f59e0b'
                    st.markdown(f"""
                        <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                                   box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); text-align: center;
                                   border-top: 3px solid {status_color};">
                            <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 0.5rem;">Statut</div>
                            <div style="font-size: 1.2rem; font-weight: 700; color: {status_color};">
                                {status_display}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Display strengths and weaknesses if available
                strengths = decision_data.get('strengths', decision_data.get('strong_points', []))
                weaknesses = decision_data.get('weaknesses', decision_data.get('weak_points', []))
                
                if strengths or weaknesses:
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_strength, col_weakness = st.columns(2)
                    
                    with col_strength:
                        if strengths:
                            st.markdown("""
                                <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; 
                                           border-left: 3px solid #10b981;">
                                    <h4 style="color: #10b981; margin-bottom: 0.5rem;">✅ Points Forts</h4>
                                </div>
                            """, unsafe_allow_html=True)
                            if isinstance(strengths, list):
                                for strength in strengths:
                                    st.markdown(f"<p style='color: #4b5563; margin: 0.5rem 0;'>• {strength}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p style='color: #4b5563; margin: 0.5rem 0;'>{strengths}</p>", unsafe_allow_html=True)
                    
                    with col_weakness:
                        if weaknesses:
                            st.markdown("""
                                <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; 
                                           border-left: 3px solid #f59e0b;">
                                    <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">⚠️ Points à Améliorer</h4>
                                </div>
                            """, unsafe_allow_html=True)
                            if isinstance(weaknesses, list):
                                for weakness in weaknesses:
                                    st.markdown(f"<p style='color: #4b5563; margin: 0.5rem 0;'>• {weakness}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p style='color: #4b5563; margin: 0.5rem 0;'>{weaknesses}</p>", unsafe_allow_html=True)
                
                # Display conclusion if available
                conclusion = decision_data.get('conclusion', decision_data.get('summary', ''))
                if conclusion:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("""
                        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; 
                                   border-left: 3px solid #667eea; margin-top: 1rem;">
                            <h4 style="color: #667eea; margin-bottom: 0.5rem;">📝 Conclusion</h4>
                            <p style="color: #4b5563; line-height: 1.8; margin: 0;">
                                {conclusion}
                            </p>
                        </div>
                    """.format(conclusion=conclusion), unsafe_allow_html=True)
            else:
                # Fallback: display as text if parsing fails
                st.warning("⚠️ Impossible de parser la décision finale au format JSON. Affichage du contenu brut:")
                
                # Clean HTML tags before displaying
                clean_decision = re.sub(r'<[^>]+>', '', str(final_decision))
                # Remove excessive whitespace
                clean_decision = re.sub(r'\s+', ' ', clean_decision).strip()
                
                st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; 
                               margin-top: 0.5rem; border-left: 3px solid #f59e0b;">
                        <p style="color: #4b5563; line-height: 1.8; margin: 0; font-family: monospace; font-size: 0.9rem;">
                            {clean_decision[:1000]}{'...' if len(clean_decision) > 1000 else ''}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Show raw data in expander for debugging
                with st.expander("🔍 Voir les données brutes (debug)"):
                    st.code(str(final_decision)[:2000], language='text')


def show_results_page():
    """Display results page."""
    st.markdown('<div class="section-header">📈 Résultats et Classement Final</div>', unsafe_allow_html=True)
    
    if not st.session_state.evaluation_results:
        st.markdown("""
            <div class="info-card" style="text-align: center; padding: 3rem;">
                <h3 style="color: #667eea; margin-bottom: 1rem;">Aucun résultat disponible</h3>
                <p style="color: #6b7280; font-size: 1.1rem;">
                    Veuillez effectuer une évaluation dans la section 'Évaluation Multi-Agents'
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    results = st.session_state.evaluation_results
    
    # Display evaluation results (same as in evaluation page)
    show_evaluation_results(results)
    
    # Export results
    st.markdown("""
        <h3 style="color: #667eea; margin: 2rem 0 1rem; font-size: 1.8rem;">
            💾 Export des Résultats
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📥 Exporter les Résultats", type="primary", use_container_width=True):
            results_json = json.dumps(results, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Télécharger JSON",
                data=results_json,
                file_name="evaluation_results.json",
                mime="application/json",
                use_container_width=True
            )


if __name__ == "__main__":
    main()

