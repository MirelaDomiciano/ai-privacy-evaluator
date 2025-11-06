"""
Serviço para avaliação de políticas de privacidade usando LLM (Gemini via LiteLLM).
"""

import os
import json
from typing import Any
from litellm import completion
import litellm
from app.config.constants import GOOGLE_API_KEY, GOOGLE_MODEL
from app.config.prompts import get_evaluation_prompt, SYSTEM_PROMPT
from app.schemas.evaluator import EvaluateRequest, EvaluateResponse, RiskPoint
from app.utils.logger import JsonLogger
import re

# Desabilitar logs verbosos do LiteLLM
litellm.suppress_debug_info = True
litellm.set_verbose = False


class EvaluatorService:
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        self.model = os.environ.get('GOOGLE_MODEL')
        self.temperature = float(os.environ.get('LLM_TEMPERATURE', "0.3"))
        self.max_tokens = int(os.environ.get('LLM_MAX_TOKENS', "8000"))
        
        JsonLogger.log(
            level="INFO",
            message="EvaluatorService initialized",
            metadata={
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "api_key_present": bool(self.api_key)
            }
        )

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
        JsonLogger.log(
            level="INFO",
            message="Sending request to LLM",
            metadata={"model": self.model, "max_tokens": self.max_tokens}
        )
        
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            api_key=self.api_key,
            max_tokens=self.max_tokens
        )
        llm_text = response["choices"][0]["message"]["content"]
        
        JsonLogger.log(
            level="DEBUG",
            message="LLM response received",
            metadata={"response_length": len(llm_text)}
        )
        llm_text = llm_text.replace('\r', '').replace('\u200b', '').strip()
        # Corte do primeiro { ao último }
        maybe_start = llm_text.find("{")
        maybe_end = llm_text.rfind("}")
        if maybe_start == -1 or maybe_end == -1 or maybe_end <= maybe_start:
            JsonLogger.log(
                level="ERROR",
                message="Failed to isolate valid JSON from LLM response",
                metadata={"response_preview": llm_text[:200]}
            )
            raise ValueError(f"Não foi possível isolar JSON válido do modelo. Trecho: {llm_text[:100]}...")
        json_str = llm_text[maybe_start:maybe_end + 1].lstrip()
        
        JsonLogger.log(
            level="DEBUG",
            message="JSON extracted from response",
            metadata={"json_length": len(json_str)}
        )
        
        # Correção para problemas comuns de aspas ou vírgulas
        json_str = json_str.replace('"summary": """', '"summary": "').replace('"""', '"')
        import re
        json_str = re.sub(r',\s*\]', ']', json_str)
        json_str = re.sub(r',\s*\}', '}', json_str)
        try:
            parsed_json = json.loads(json_str)
            JsonLogger.log(
                level="INFO",
                message="JSON parsed successfully",
                metadata={"has_summary": "summary" in parsed_json, "has_risk_score": "risk_score" in parsed_json}
            )
            return parsed_json
        except Exception as e:
            JsonLogger.log(
                level="ERROR",
                message="JSON parsing failed",
                metadata={"error": str(e), "json_preview": json_str[:280]}
            )
            raise ValueError(f"JSON inviável após max cleaning: {e}")

    def evaluate_policy(self, text: str) -> EvaluateResponse:
        """
        Pipeline completo:
        1. Gera prompt com o texto da política
        2. Chama o LLM e extrai o JSON da resposta
        3. Valida e retorna EvaluateResponse (Pydantic)
        """
        JsonLogger.log(
            level="INFO",
            message="Starting policy evaluation",
            metadata={"text_length": len(text)}
        )
        
        prompt = self.get_prompt(text)
        llm_json = self.get_llm_json(prompt)
        
        try:
            response = EvaluateResponse(**llm_json)
            JsonLogger.log(
                level="INFO",
                message="Policy evaluation completed successfully",
                metadata={
                    "risk_score": response.risk_score,
                    "risk_points_count": len(response.risk_points)
                }
            )
            return response
        except Exception as e:
            JsonLogger.log(
                level="ERROR",
                message="Pydantic validation failed",
                metadata={"error": str(e), "json_keys": list(llm_json.keys())}
            )
            raise ValueError(f"Erro ao validar resposta do modelo: {e}\nJSON recebido: {llm_json}")

