"""Configuration settings for the candidate selection system."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration - Groq
# Try to get from Streamlit secrets first (for Streamlit Cloud)
try:
    import streamlit as st
    if hasattr(st, 'secrets') and st.secrets:
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
        GROQ_MODEL = st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    else:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
except (ImportError, RuntimeError, AttributeError):
    # Not in Streamlit context, use environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Fallback to environment variables if secrets are empty
if not GROQ_API_KEY:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_MODEL:
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Supported models: llama-3.3-70b-versatile, llama-3.1-70b-versatile, llama-3.1-8b-instant, qwen2.5-32b-instruct

# Paths
DATA_DIR = "data"
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
JOB_DESCRIPTIONS_DIR = os.path.join(DATA_DIR, "job_descriptions")
CHROMA_DB_PATH = "chroma_db"

# Agent Configuration
MAX_ITERATIONS = 3
TEMPERATURE = 0.7

# RAG Configuration - Using local embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_CANDIDATES = 10
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Scoring Weights
TECHNICAL_WEIGHT = 0.35
SOFT_SKILLS_WEIGHT = 0.25
PROFILE_WEIGHT = 0.25
CULTURAL_FIT_WEIGHT = 0.15

