# Structure du Projet

```
projet machine learning candidate selection/
│
├── agents/                          # Agents Multi-Agents
│   ├── __init__.py
│   ├── hr_agent.py                 # Agent RH - Analyse des postes
│   ├── profile_agent.py            # Agent Profil - Analyse CVs
│   ├── technical_agent.py          # Agent Technique - Compétences tech
│   ├── soft_skills_agent.py        # Agent Soft Skills - Qualités interpersonnelles
│   └── decider_agent.py            # Agent Décideur - Décision finale
│
├── preprocessing/                   # Prétraitement et EDA
│   ├── __init__.py
│   ├── data_loader.py              # Chargement des documents
│   ├── text_processor.py           # Traitement NLP (NER, extraction)
│   └── exploratory_analysis.py     # Analyse exploratoire
│
├── rag/                             # Système RAG
│   ├── __init__.py
│   ├── vector_store.py              # Stockage vectoriel (ChromaDB)
│   └── retriever.py                # Recherche sémantique
│
├── utils/                           # Utilitaires
│   ├── __init__.py
│   └── config.py                   # Configuration centralisée
│
├── data/                            # Données
│   ├── raw/                        # CVs et lettres brutes
│   │   ├── candidate_001.txt
│   │   ├── candidate_002.txt
│   │   ├── candidate_003.txt
│   │   ├── candidate_004.txt
│   │   └── candidate_005.txt
│   ├── processed/                  # Données prétraitées
│   └── job_descriptions/           # Descriptions de postes
│       └── data_scientist.txt
│
├── docs/                            # Documentation
│   └── theoretical_foundation.md    # Fondements théoriques
│
├── app.py                           # Interface Streamlit principale
├── candidate_selection_system.py    # Orchestration multi-agents
│
├── requirements.txt                 # Dépendances Python
├── README.md                        # Documentation principale
├── SETUP.md                         # Guide d'installation
├── USAGE_GUIDE.md                   # Guide d'utilisation
├── PROJECT_SUMMARY.md               # Résumé du projet
├── STRUCTURE.md                     # Ce fichier
└── .gitignore                       # Fichiers à ignorer
```

## Description des Modules

### Agents (`agents/`)
Chaque agent est spécialisé dans un aspect de l'évaluation :
- **HR Agent** : Comprend les besoins du recruteur
- **Profile Agent** : Analyse les parcours professionnels
- **Technical Agent** : Évalue les compétences techniques
- **Soft Skills Agent** : Évalue les qualités interpersonnelles
- **Decider Agent** : Synthétise et décide

### Preprocessing (`preprocessing/`)
Modules de traitement des données :
- **data_loader** : Charge PDF, DOCX, TXT
- **text_processor** : NER, extraction de compétences, métriques
- **exploratory_analysis** : Statistiques et visualisations

### RAG (`rag/`)
Système de recherche augmentée :
- **vector_store** : Gestion des embeddings et recherche vectorielle
- **retriever** : Interface de recherche par critères

### Utils (`utils/`)
Configuration et utilitaires partagés.

### Data (`data/`)
- **raw/** : Documents candidats bruts
- **processed/** : Données prétraitées (générées automatiquement)
- **job_descriptions/** : Descriptions de postes

### Documentation (`docs/`)
Fondements théoriques complets du système.

## Fichiers Principaux

- **app.py** : Point d'entrée Streamlit
- **candidate_selection_system.py** : Orchestration du workflow
- **requirements.txt** : Toutes les dépendances
- **README.md** : Documentation générale

