# utils/config.py
# Central config — loads all API keys from .env file

import os
from dotenv import load_dotenv

load_dotenv()  # This reads your .env file automatically

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MOMENTO_API_KEY   = os.getenv("MOMENTO_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
SECRET_KEY        = os.getenv("SECRET_KEY", "fallback-secret-key")

# Momento cache name — you can change this
MOMENTO_CACHE_NAME = "riskexplain-cache"