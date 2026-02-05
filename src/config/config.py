import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model Configuration
# Set USE_OLLAMA to True for Ollama (local), False for Groq (cloud/Docker)
# For Docker deployment, set this to False and use Groq
USE_OLLAMA = os.getenv("USE_OLLAMA", "False").lower() == "true"
    
# Ollama Configuration
OLLAMA_MODEL = "qwen3-vl:30b-a3b-instruct"  
OLLAMA_BASE_URL = "http://localhost:11434"  # Default Ollama URL
    
# Groq Configuration (for when you switch back)
GROQ_MODEL = "llama-3.3-70b-versatile"
    
# Active RAG Model (determined by USE_OLLAMA flag)
RAG_MODEL = OLLAMA_MODEL if USE_OLLAMA else GROQ_MODEL