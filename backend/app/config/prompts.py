"""
LLM prompts for privacy policy evaluation
"""

SYSTEM_PROMPT = """Você é um especialista em privacidade de dados, LGPD (Lei Geral de Proteção de Dados) e políticas de privacidade.
Sua função é analisar políticas de privacidade e identificar riscos reais para os usuários brasileiros.
"""


EVALUATION_PROMPT = """Analise a seguinte política de privacidade sob a ótica da LGPD e identifique riscos para o usuário.

POLÍTICA DE PRIVACIDADE:
{policy_text}

Você deve retornar um JSON válido com a seguinte estrutura EXATA:

{{
  "summary": "Resumo em linguagem simples da política, em Markdown, faça de forma clara e sucinta, sem informações extras. SOMENTE OS PONTOS MAIS IMPORTANTES DA POLÍTICA.",
  "risk_score": <número de 0 a 5, onde 5 é muito seguro e 0 é muito arriscado>,
  "risk_points": [
    {{
      "category": "Nome da categoria do risco",
      "description": "Descrição clara e direta do risco identificado",
      "severity": "low, medium ou high"
    }}
  ]
}}

CATEGORIAS DE RISCO (use APENAS estas 4 categorias):
1. **Conformidade LGPD**: Falta de informações obrigatórias, base legal, DPO/Encarregado, finalidade clara
2. **Compartilhamento e Uso de Dados**: Como os dados são usados, compartilhados com terceiros, vendidos ou cedidos
3. **Direitos do Usuário**: Facilidade para acessar, corrigir, excluir dados; clareza sobre consentimento
4. **Transparência e Clareza**: Linguagem enganosa, termos vagos, informações ocultas ou confusas

CRITÉRIOS PARA SEVERITY:
- **low**: Risco menor, prática comum mas que merece atenção
- **medium**: Risco moderado, pode prejudicar privacidade
- **high**: Risco alto, prática invasiva ou não conforme LGPD

CRITÉRIOS PARA RISK_SCORE:
- 5: Política excelente, transparente, conforme LGPD, muito favorável ao usuário
- 4: Política boa, pequenas ressalvas mas geralmente segura
- 3: Política razoável, alguns pontos de atenção (compartilhamento moderado, linguagem às vezes vaga)
- 2: Política problemática, vários problemas significativos, dificulta direitos do usuário
- 1: Política ruim, múltiplos problemas graves, práticas questionáveis
- 0: Política muito arriscada, não conforme LGPD, práticas abusivas

IMPORTANTE:
- Retorne APENAS o JSON, sem texto adicional antes ou depois
- O campo summary deve ser uma string CURTA (máximo 300 caracteres)
- Identifique entre 2 a 5 risk_points principais (não exagere na quantidade)
- Seja objetivo e direto nas descrições
"""


def get_evaluation_prompt(policy_text: str) -> str:
    """
    Generate the evaluation prompt with the policy text
    
    Args:
        policy_text: The privacy policy text to evaluate
        
    Returns:
        Formatted prompt string
    """
    return EVALUATION_PROMPT.format(policy_text=policy_text)

