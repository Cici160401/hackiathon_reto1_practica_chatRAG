import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY")
CHROMA_PERSIST   = os.getenv("CHROMA_PERSIST_DIR", ".chromadb")