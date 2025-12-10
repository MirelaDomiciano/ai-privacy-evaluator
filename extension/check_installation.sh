#!/bin/bash

# Script de verificação da extensão e API

echo "🔍 Verificando instalação da extensão..."
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar estrutura de arquivos
echo "📁 Verificando estrutura de arquivos..."

files=(
    "extension/manifest.json"
    "extension/popup/popup.html"
    "extension/popup/popup.js"
    "extension/popup/popup.css"
    "extension/icons/icon16.png"
    "extension/icons/icon48.png"
    "extension/icons/icon128.png"
    "extension/README.md"
)

all_files_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file (FALTANDO)"
        all_files_exist=false
    fi
done

echo ""

# 2. Verificar se a API está rodando
echo "🌐 Verificando API..."

api_url="http://localhost:8000/health"

if curl -s "$api_url" > /dev/null 2>&1; then
    response=$(curl -s "$api_url")
    echo -e "${GREEN}✓${NC} API está rodando"
    echo "   Resposta: $response"
else
    echo -e "${RED}✗${NC} API não está acessível em $api_url"
    echo ""
    echo -e "${YELLOW}💡 Para iniciar a API:${NC}"
    echo "   cd backend"
    echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
fi

echo ""

# 3. Verificar endpoint de avaliação
echo "🔬 Testando endpoint de avaliação..."

eval_url="http://localhost:8000/api/v1/evaluate"
test_payload='{"text":"Esta é uma política de privacidade de teste. Coletamos seus dados pessoais incluindo nome, email e endereço. Compartilhamos essas informações com parceiros terceiros. Você tem o direito de solicitar a exclusão dos seus dados."}'

if curl -s -X POST "$eval_url" \
    -H "Content-Type: application/json" \
    -d "$test_payload" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Endpoint de avaliação está funcionando"
else
    echo -e "${YELLOW}⚠${NC} Endpoint de avaliação não respondeu (pode ser normal se a API não estiver configurada)"
fi

echo ""
echo "=" "=" "=" "=" "=" "=" "=" "=" "=" "="
echo ""

# 4. Resumo
echo "📋 Resumo:"
echo ""

if [ "$all_files_exist" = true ]; then
    echo -e "${GREEN}✓${NC} Todos os arquivos da extensão estão presentes"
else
    echo -e "${RED}✗${NC} Alguns arquivos estão faltando"
fi

echo ""
echo "🚀 Próximos passos:"
echo ""
echo "1. Certifique-se de que a API está rodando:"
echo "   cd backend && uvicorn app.main:app --reload"
echo ""
echo "2. Instale a extensão no Chrome/Edge:"
echo "   - Acesse chrome://extensions/"
echo "   - Ative o 'Modo do desenvolvedor'"
echo "   - Clique em 'Carregar sem compactação'"
echo "   - Selecione a pasta 'extension'"
echo ""
echo "3. Teste a extensão:"
echo "   - Clique no ícone da extensão"
echo "   - Cole uma política de privacidade"
echo "   - Clique em 'Analisar Política'"
echo ""
echo "📖 Documentação completa: extension/README.md"
echo ""

