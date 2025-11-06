"""
Application constants and configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini/gemini-1.5-pro")

# LLM Parameters
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))

# Risk Categories (baseadas na LGPD e principais riscos identificados)
RISK_CATEGORIES = [
    "Conformidade LGPD",  # Falta de informações obrigatórias (DPO, base legal, etc)
    "Compartilhamento com Terceiros",  # "Parceiros" e redes de publicidade
    "Linguagem Enganosa",  # "Não vendemos" mas compartilhamos, termos vagos
    "Retenção de Dados",  # Prazo indefinido ou excessivo
    "Direitos do Titular",  # Dificuldade para acessar, corrigir ou excluir dados
    "Decisões Automatizadas",  # Uso de IA/algoritmos sem transparência
    "Consentimento",  # Falta de clareza sobre finalidade e base legal
    "Transferência Internacional"  # Dados enviados para fora do Brasil
]

# Severity Levels
SEVERITY_LEVELS = ["low", "medium", "high"]

# Validation
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")
