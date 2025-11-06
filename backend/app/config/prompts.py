"""
LLM prompts for privacy policy evaluation
"""

SYSTEM_PROMPT = """Você é um especialista em privacidade de dados, LGPD (Lei Geral de Proteção de Dados) e políticas de privacidade.
Sua função é analisar políticas de privacidade e identificar riscos reais para os usuários brasileiros.

Você deve ser:
- Objetivo e claro, usando linguagem simples
- Focado em conformidade com a LGPD e proteção do usuário
- Atento a práticas abusivas de compartilhamento de dados
"""


EVALUATION_PROMPT = """Analise a seguinte política de privacidade sob a ótica da LGPD e identifique riscos para o usuário.

POLÍTICA DE PRIVACIDADE:
{policy_text}

Você deve retornar um JSON válido com a seguinte estrutura EXATA:

{{
  "summary": "Resumo em linguagem simples da política, em Markdown, faça de forma clara e sucinta, sem informações extras. SOMENTE OS PONTOS MAIS IMPORTANTES DA POLÍTICA.",
  "risk_score": <número de 0 a 10, onde 0 é muito seguro e 10 é muito arriscado>,
  "risk_points": [
    {{
      "category": "Nome da categoria do risco",
      "description": "Descrição clara e direta do risco identificado",
      "severity": "low, medium ou high"
    }}
  ]
}}

CATEGORIAS DE RISCO (use estas):
1. **Conformidade LGPD**: Falta de informações obrigatórias (DPO/Encarregado, base legal, finalidade clara)
2. **Compartilhamento com Terceiros**: Dados compartilhados com "parceiros", redes de publicidade, afiliados
3. **Linguagem Enganosa**: Uso de "não vendemos dados" mas admite compartilhamento; termos vagos como "interesses legítimos"
4. **Retenção de Dados**: Prazo indefinido, excessivo ou não especificado para guardar dados
5. **Direitos do Titular**: Dificuldade para exercer direitos (acessar, corrigir, excluir dados; revogar consentimento)
6. **Decisões Automatizadas**: Uso de IA/algoritmos sem transparência ou direito de revisão humana
7. **Consentimento**: Falta de clareza sobre o que você está consentindo; finalidade genérica
8. **Transferência Internacional**: Dados enviados para fora do Brasil sem garantias adequadas

CRITÉRIOS PARA RISK_SCORE:
- 0-2: Política transparente, conforme LGPD, favorável ao usuário
- 3-4: Política razoável, pequenas falhas de transparência
- 5-6: Política com pontos de atenção (compartilhamento amplo, linguagem vaga)
- 7-8: Política problemática (múltiplas "red flags", dificulta direitos do usuário)
- 9-10: Política muito arriscada (não conforme LGPD, práticas abusivas)

CRITÉRIOS PARA SEVERITY:
- **low**: Risco menor, prática comum mas que merece atenção
- **medium**: Risco moderado, pode prejudicar privacidade (ex: compartilhamento com parceiros, prazo longo)
- **high**: Risco alto, prática invasiva ou não conforme LGPD (ex: falta de DPO, impossibilidade de excluir dados, linguagem enganosa)

IMPORTANTE:
- Retorne APENAS o JSON, sem texto adicional antes ou depois (não inclua comentários, exemplos ou código fora do JSON)
- O campo summary deve ser sempre uma string Markdown VÁLIDA, entre aspas duplas
- Todos os caracteres especiais, como quebras de linha de Markdown (`\n`), devem estar corretamente escapados para que o JSON permaneça válido
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

