"""Configuration settings for the candidate selection system."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration - Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Supported models: llama-3.3-70b-versatile, llama-3.1-70b-versatile, llama-3.1-8b-instant, qwen2.5-32b-instruct
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

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

