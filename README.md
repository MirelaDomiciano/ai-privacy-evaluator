# 🔒 AI Privacy Policy Evaluator

Ferramenta de avaliação automática de políticas de privacidade usando Inteligência Artificial. O sistema analisa documentos sob a ótica da **LGPD (Lei Geral de Proteção de Dados)** e identifica riscos para a privacidade dos usuários.

## 📋 Sobre o Projeto

Este é um projeto acadêmico desenvolvido para a disciplina de **Informática e Sociedade** da UNIFEI. A ferramenta utiliza o modelo **Google Gemini** via LiteLLM para realizar análises detalhadas de políticas de privacidade, identificando:

- ✅ Conformidade com a LGPD
- ⚠️ Pontos de risco e vulnerabilidades
- 📊 Classificação de severidade (Alto, Médio, Baixo)
- 📝 Resumo executivo em Markdown

## 🏗️ Arquitetura

O projeto é dividido em dois componentes principais:

### Backend (FastAPI)
- **Framework**: FastAPI + Pydantic
- **LLM**: Google Gemini via LiteLLM
- **Logging**: Estruturado em JSON
- **API**: RESTful com endpoint `/api/v1/evaluate`

### Frontend (Streamlit)
- **Framework**: Streamlit
- **Interface**: Responsiva com layout em colunas
- **Features**: Métricas visuais, expanders dinâmicos, análise em tempo real

## 🚀 Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI** - Framework web para APIs
- **Streamlit** - Interface web interativa
- **LiteLLM** - Interface unificada para LLMs
- **Google Gemini** - Modelo de linguagem para análise
- **Pydantic** - Validação de dados
- **Docker & Docker Compose** - Containerização
- **Uvicorn** - Servidor ASGI

## 📦 Estrutura do Projeto

```
ai-privacy-evaluator/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   │   ├── constants.py      # Variáveis de ambiente e constantes
│   │   │   └── prompts.py        # Prompts para o LLM
│   │   ├── routers/
│   │   │   └── evaluator_routers.py  # Endpoints da API
│   │   ├── schemas/
│   │   │   └── evaluator.py      # Modelos Pydantic
│   │   ├── services/
│   │   │   └── evaluator_service.py  # Lógica de negócio
│   │   ├── utils/
│   │   │   └── logger.py         # Sistema de logging
│   │   └── main.py               # Aplicação FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env                      # Variáveis de ambiente (não versionado)
├── frontend/
│   ├── streamlit_app.py          # Aplicação Streamlit
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## ⚙️ Configuração e Instalação

### Pré-requisitos

- Docker e Docker Compose instalados
- Chave de API do Google Gemini ([obter aqui](https://makersuite.google.com/app/apikey))

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd ai-privacy-evaluator
```

### 2. Configure as Variáveis de Ambiente

Crie o arquivo `backend/.env`:

```env
# Google Gemini API
GOOGLE_API_KEY=sua_chave_api_aqui
GOOGLE_MODEL=gemini/gemini-1.5-flash

# LLM Configuration
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=8000

# Environment
ENVIRONMENT=development
```

### 3. Execute com Docker Compose

```bash
docker compose up --build
```

### 4. Acesse a Aplicação

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend (FastAPI)**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 🔧 Desenvolvimento Local (sem Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 📡 API Endpoints

### POST `/api/v1/evaluate`

Avalia uma política de privacidade.

**Request Body:**
```json
{
  "text": "Texto completo da política de privacidade..."
}
```

**Response:**
```json
{
  "summary": "# Resumo da Política\n\nTexto em Markdown...",
  "risk_score": 8.0,
  "risk_points": [
    {
      "category": "Compartilhamento de Dados",
      "description": "A política permite compartilhamento amplo...",
      "severity": "high"
    }
  ]
}
```

### GET `/health`

Verifica o status da API.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🎯 Categorias de Risco Avaliadas

A ferramenta analisa políticas de privacidade com base nas seguintes categorias da LGPD:

1. **Identificação do Encarregado (DPO)**
2. **Finalidade e Base Legal**
3. **Prazo de Retenção de Dados**
4. **Compartilhamento com Terceiros**
5. **Direitos do Titular**
6. **Uso de Termos Vagos**
7. **Dark Patterns na Interface**
8. **Decisões Automatizadas (IA)**
9. **Transferência Internacional de Dados**

## 📊 Sistema de Pontuação

- **0-3**: 🟢 Baixo Risco - Política adequada e transparente
- **4-6**: 🟠 Risco Moderado - Alguns pontos de atenção
- **7-10**: 🔴 Alto Risco - Problemas graves de privacidade

## 🛠️ Tecnologias de Logging

O backend utiliza logging estruturado em JSON para facilitar debugging e monitoramento:

```json
{
  "timestamp": "2025-11-06T10:30:00Z",
  "level": "INFO",
  "message": "Policy evaluation completed",
  "metadata": {
    "risk_score": 8.0,
    "risk_points_count": 9
  }
}
```

## 🐳 Docker

### Comandos Úteis

```bash
# Iniciar os serviços
docker compose up -d

# Ver logs
docker compose logs -f backend
docker compose logs -f frontend

# Parar os serviços
docker compose down

# Rebuild completo
docker compose down
docker compose build --no-cache
docker compose up
```

## 🧪 Testando a API

### Com curl

```bash
curl -X POST "http://localhost:8000/api/v1/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Esta é uma política de privacidade de exemplo..."
  }'
```

### Com Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/evaluate",
    json={"text": "Texto da política..."}
)

print(response.json())
```

## 📝 Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

## 👥 Autores

Projeto desenvolvido como parte da disciplina de **Informática e Sociedade** - UNIFEI

## 🙏 Agradecimentos

- **Google Gemini** - Modelo de linguagem
- **LiteLLM** - Interface unificada para LLMs
- **FastAPI** - Framework web moderno
- **Streamlit** - Framework para interfaces interativas

---

**⚠️ Nota**: Esta ferramenta é um projeto acadêmico e não substitui análise jurídica profissional de políticas de privacidade.
