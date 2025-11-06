"""
Serviço para avaliação de políticas de privacidade usando LLM (Gemini via LiteLLM).
"""

import os
import json
from typing import Any
from litellm import completion
from app.config.constants import GOOGLE_API_KEY, GOOGLE_MODEL
from app.config.prompts import get_evaluation_prompt, SYSTEM_PROMPT
from app.schemas.evaluator import EvaluateRequest, EvaluateResponse, RiskPoint
import re


class EvaluatorService:
    def __init__(self):
        # Log de debug das variáveis de ambiente

        self.api_key = os.environ.get('GOOGLE_API_KEY')
        self.model = os.environ.get('GOOGLE_MODEL')
        self.temperature = float(os.environ.get('LLM_TEMPERATURE', "0.3"))
        self.max_tokens = int(os.environ.get('LLM_MAX_TOKENS', "8000"))

    def get_prompt(self, policy_text: str) -> str:
        """
        Gera o prompt para o LLM com base no texto da política de privacidade.
        """
        return get_evaluation_prompt(policy_text)

    def get_llm_json(self, prompt: str) -> dict:
        """
        Envia o prompt ao LLM, obtém a resposta e retorna o JSON decodificado como dict.
        Agora robusto para problemas típicos de JSON gerado por LLM com markdown longo.
        """
        
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            api_key=self.api_key
        )
        llm_text = response["choices"][0]["message"]["content"]
        llm_text = llm_text.replace('\r', '').replace('\u200b', '').strip()
        # Corte do primeiro { ao último }
        maybe_start = llm_text.find("{")
        maybe_end = llm_text.rfind("}")
        if maybe_start == -1 or maybe_end == -1 or maybe_end <= maybe_start:
            raise ValueError(f"Não foi possível isolar JSON válido do modelo. Trecho: {llm_text[:100]}...")
        json_str = llm_text[maybe_start:maybe_end + 1].lstrip()
        # Correção para problemas comuns de aspas ou vírgulas
        json_str = json_str.replace('"summary": """', '"summary": "').replace('"""', '"')
        import re
        json_str = re.sub(r',\s*\]', ']', json_str)
        json_str = re.sub(r',\s*\}', '}', json_str)
        try:
            return json.loads(json_str)
        except Exception as e:
            print('### JSON problemático:', json_str[:280])
            raise ValueError(f"JSON inviável após max cleaning: {e}")

    def evaluate_policy(self, text: str) -> EvaluateResponse:
        """
        Pipeline completo:
        1. Gera prompt com o texto da política
        2. Chama o LLM e extrai o JSON da resposta
        3. Valida e retorna EvaluateResponse (Pydantic)
        """
        prompt = self.get_prompt(text)
        llm_json = self.get_llm_json(prompt)
        try:
            return EvaluateResponse(**llm_json)
        except Exception as e:
            raise ValueError(f"Erro ao validar resposta do modelo: {e}\nJSON recebido: {llm_json}")

