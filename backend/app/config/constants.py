"""
Application constants and configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini/gemini-2.5-flash-lite")

# LLM Parameters
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))


# Validation
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")
