# 🔒 AI Privacy Policy Evaluator - Extensão de Navegador

Extensão de navegador para avaliar políticas de privacidade usando Inteligência Artificial.

## 📋 Descrição

Esta extensão permite que você analise políticas de privacidade de websites diretamente no seu navegador. Basta colar o texto ou selecionar uma seção da página e a IA irá avaliar a política em diversas categorias, identificar problemas e fornecer recomendações.

## ✨ Funcionalidades

- ✅ **Análise com IA**: Avaliação automática usando modelos de linguagem
- 📊 **Pontuação detalhada**: Avaliação por categorias (coleta de dados, uso, compartilhamento, etc.)
- ⚠️ **Identificação de riscos**: Detecta problemas e práticas questionáveis
- 💡 **Recomendações**: Sugestões para melhorar a privacidade
- 🎨 **Interface moderna**: Design limpo e intuitivo
- 🔄 **Duas formas de entrada**: Cole o texto ou selecione diretamente da página

## 🚀 Instalação

### Pré-requisitos

1. **Navegador**: Google Chrome, Microsoft Edge, ou Brave (Manifest V3)
2. **API Backend**: A API deve estar rodando localmente

### Instalar o Backend (API)

```bash
# Navegue até o diretório do backend
cd backend

# Instale as dependências
pip install -r requirements.txt

# Execute a API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

### Instalar a Extensão no Navegador

1. **Abra o Chrome/Edge**

2. **Acesse a página de extensões**:
   - Chrome: Digite `chrome://extensions/` na barra de endereços
   - Edge: Digite `edge://extensions/` na barra de endereços

3. **Ative o "Modo do desenvolvedor"**:
   - Encontre o botão/toggle no canto superior direito da página
   - Ative-o

4. **Carregue a extensão**:
   - Clique no botão **"Carregar sem compactação"** ou **"Load unpacked"**
   - Navegue até a pasta `extension` deste projeto
   - Selecione a pasta e clique em **"Selecionar pasta"**

5. **Pronto!** 🎉
   - A extensão aparecerá na barra de ferramentas
   - Você pode fixá-la clicando no ícone de puzzle 🧩 e depois no pin 📌

## 📖 Como Usar

### Método 1: Colar Texto

1. Clique no ícone da extensão na barra de ferramentas
2. Cole o texto da política de privacidade no campo de texto
3. Clique em **"🔍 Analisar Política"**
4. Aguarde a análise (pode levar alguns segundos)
5. Veja os resultados detalhados

### Método 2: Selecionar Texto da Página

1. Acesse um site com política de privacidade
2. Selecione o texto da política (clique e arraste)
3. Clique no ícone da extensão
4. Clique em **"📄 Usar Texto Selecionado"**
5. Clique em **"🔍 Analisar Política"**
6. Veja os resultados

## 📊 O que é Avaliado?

A extensão analisa as políticas em múltiplas categorias:

- 📦 **Coleta de Dados**: Quais dados são coletados
- 🎯 **Uso de Dados**: Como os dados são utilizados
- 🤝 **Compartilhamento**: Com quem os dados são compartilhados
- ⚖️ **Direitos do Usuário**: Direitos de acesso, exclusão, portabilidade
- 🔐 **Segurança**: Medidas de proteção dos dados
- 🔍 **Transparência**: Clareza e completude da política
- 📜 **Conformidade Legal**: Aderência a leis como LGPD/GDPR

## 🎨 Interface

A extensão mostra:

- **Pontuação Geral**: De 0 a 100
- **Pontuações por Categoria**: Visualização em barras coloridas
- **Problemas Identificados**: Com nível de severidade (alta/média/baixa)
- **Recomendações**: Sugestões práticas
- **Resumo**: Visão geral da análise
- **Status da API**: Indicador de conexão

## 🔧 Configuração Avançada

### Alterar URL da API

Se sua API estiver em outro endereço, edite o arquivo:

```
extension/popup/popup.js
```

Linha 2:
```javascript
const API_URL = 'http://localhost:8000/api/v1/evaluate';
```

Altere para o endereço desejado.

### Personalizar Aparência

Edite o arquivo `extension/popup/popup.css` para customizar cores, fontes e estilos.

## 🐛 Solução de Problemas

### API Desconectada

**Problema**: Status mostra "Desconectado" (ponto vermelho)

**Solução**:
- Verifique se a API está rodando: `http://localhost:8000/docs`
- Certifique-se que o backend foi iniciado corretamente
- Verifique o console do navegador (F12) para erros de CORS

### Erro ao Analisar

**Problema**: "Erro ao avaliar política"

**Possíveis causas**:
- API não está rodando
- Texto muito curto (mínimo 100 caracteres)
- Erro no modelo de IA (verifique logs da API)
- Problemas de CORS

**Solução**:
- Reinicie a API
- Verifique os logs no terminal onde a API está rodando
- Certifique-se que o texto da política está completo

### Texto Selecionado Não Funciona

**Problema**: Botão "Usar Texto Selecionado" não captura o texto

**Solução**:
- Certifique-se de que você selecionou texto na página atual
- Algumas páginas bloqueiam scripts externos (páginas do Chrome, por exemplo)
- Tente usar o método de colar o texto manualmente

## 🔒 Privacidade

- A extensão **NÃO armazena** nenhum dado permanentemente
- Todo o processamento é feito localmente na sua máquina (via API local)
- Nenhuma informação é enviada para servidores externos (exceto se configurado)
- O texto analisado não é salvo nem compartilhado

## 📝 Estrutura de Arquivos

```
extension/
├── manifest.json          # Configuração da extensão
├── popup/
│   ├── popup.html        # Interface do usuário
│   ├── popup.js          # Lógica da aplicação
│   └── popup.css         # Estilos
└── icons/
    ├── icon16.png        # Ícone 16x16
    ├── icon48.png        # Ícone 48x48
    └── icon128.png       # Ícone 128x128
```

## 🛠️ Desenvolvimento

### Recarregar Alterações

1. Faça suas alterações nos arquivos
2. Volte à página `chrome://extensions/`
3. Clique no botão de **Recarregar** (ícone de atualização) na extensão
4. Teste as mudanças

### Debug

- Clique com botão direito no ícone da extensão
- Selecione **"Inspecionar popup"**
- Use o console para ver logs e erros

## 📄 Licença

Este projeto é parte do trabalho acadêmico da disciplina de Informática e Sociedade - UNIFEI.

## 👥 Suporte

Em caso de problemas ou dúvidas:

1. Verifique a seção de **Solução de Problemas**
2. Consulte os logs da API no terminal
3. Verifique o console do navegador (F12)

---


