// Configuração da API
const API_URL = 'http://localhost:8000/api/v1/evaluate';

// Elementos do DOM
const policyTextArea = document.getElementById('policyText');
const evaluateBtn = document.getElementById('evaluateBtn');
const getSelectedTextBtn = document.getElementById('getSelectedText');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const resultsDiv = document.getElementById('results');
const apiStatusDot = document.getElementById('apiStatus');
const apiStatusText = document.getElementById('apiStatusText');

// Verifica status da API ao carregar
checkApiStatus();

// Event Listeners
evaluateBtn.addEventListener('click', evaluatePolicy);
getSelectedTextBtn.addEventListener('click', getSelectedText);

// Função para obter texto selecionado da página
async function getSelectedText() {
    try {
        // Desabilita o botão temporariamente
        getSelectedTextBtn.disabled = true;
        getSelectedTextBtn.textContent = '⏳ Copiando...';
        
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        // Verifica se é uma página permitida
        if (tab.url.startsWith('chrome://') || tab.url.startsWith('edge://') || tab.url.startsWith('about:')) {
            throw new Error('Não é possível acessar páginas internas do navegador');
        }
        
        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => window.getSelection().toString()
        });
        
        const selectedText = results[0].result;
        
        if (selectedText && selectedText.trim()) {
            policyTextArea.value = selectedText;
            showMessage('✅ Texto copiado com sucesso! (' + selectedText.length + ' caracteres)', 'success');
        } else {
            showMessage('⚠️ Nenhum texto selecionado na página. Selecione o texto e tente novamente.', 'warning');
        }
    } catch (error) {
        console.error('Erro ao obter texto selecionado:', error);
        let errorMsg = 'Erro ao obter texto selecionado.';
        
        if (error.message.includes('Cannot access')) {
            errorMsg = 'Não é possível acessar esta página. Tente em uma página web normal.';
        } else if (error.message.includes('páginas internas')) {
            errorMsg = error.message;
        }
        
        showMessage('❌ ' + errorMsg, 'error');
    } finally {
        // Reabilita o botão
        getSelectedTextBtn.disabled = false;
        getSelectedTextBtn.textContent = '📄 Usar Texto Selecionado';
    }
}

// Função para avaliar a política
async function evaluatePolicy() {
    const text = policyTextArea.value.trim();
    
    if (!text) {
        showError('Por favor, insira o texto da política de privacidade.');
        return;
    }
    
    if (text.length < 100) {
        showError('O texto parece muito curto. Insira uma política de privacidade completa.');
        return;
    }
    
    // Mostra loading
    hideAll();
    loadingDiv.classList.remove('hidden');
    evaluateBtn.disabled = true;
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('API Response:', data); // Debug: ver formato da resposta
        displayResults(data);
        
    } catch (error) {
        console.error('Erro na avaliação:', error);
        showError(`Erro ao avaliar política: ${error.message}. Verifique se a API está rodando em ${API_URL}`);
    } finally {
        loadingDiv.classList.add('hidden');
        evaluateBtn.disabled = false;
    }
}

// Função para exibir os resultados
function displayResults(data) {
    console.log('displayResults called with:', data); // Debug
    hideAll();
    resultsDiv.classList.remove('hidden');
    
    // Risk score agora é de 0-5 (onde 5 é muito seguro e 0 é muito arriscado)
    const riskScore = data.risk_score !== undefined ? data.risk_score : 2.5;
    
    // Arredonda para 1 casa decimal se necessário
    const displayScore = Math.round(riskScore * 10) / 10;
    
    console.log('Risk Score:', riskScore, 'Display Score:', displayScore); // Debug
    
    // 1. PONTUAÇÃO (compacta e discreta)
    const overallScore = document.getElementById('overallScore');
    if (overallScore) {
        overallScore.textContent = `${displayScore}/5`;
        // Calcula a classe baseado na escala 0-5
        const scorePercentage = (riskScore / 5) * 100;
        overallScore.className = `score-badge ${getScoreClass(scorePercentage)}`;
        console.log('Score element updated:', overallScore.textContent); // Debug
    } else {
        console.error('overallScore element not found!'); // Debug
    }
    
    // 2. RESUMO
    const summaryText = document.getElementById('summaryText');
    if (summaryText) {
        summaryText.innerHTML = data.summary || 'Análise concluída com sucesso.';
    }
    
    // 3. PROBLEMAS POR CATEGORIA (com toggles)
    const issuesList = document.getElementById('issuesList');
    issuesList.innerHTML = '';
    
    if (data.risk_points && data.risk_points.length > 0) {
        // Agrupa risk_points por categoria
        const groupedByCategory = {};
        
        data.risk_points.forEach(point => {
            const category = point.category || 'Outros';
            if (!groupedByCategory[category]) {
                groupedByCategory[category] = [];
            }
            groupedByCategory[category].push(point);
        });
        
        // Cria toggles para cada categoria
        Object.entries(groupedByCategory).forEach(([category, points]) => {
            // Determina a severidade mais alta da categoria
            const severities = points.map(p => p.severity);
            let maxSeverity = 'low';
            if (severities.includes('high')) maxSeverity = 'high';
            else if (severities.includes('medium')) maxSeverity = 'medium';
            
            const toggleItem = document.createElement('div');
            toggleItem.className = 'issue-toggle-item';
            toggleItem.dataset.category = category;
            
            // Header (clicável)
            const header = document.createElement('div');
            header.className = 'issue-toggle-header';
            header.innerHTML = `
                <div class="issue-toggle-left">
                    <span class="issue-toggle-icon">▶</span>
                    <span class="issue-category-name">${category}</span>
                </div>
                <span class="issue-severity-badge ${maxSeverity}">${getSeverityLabel(maxSeverity)}</span>
            `;
            
            // Body (expansível)
            const body = document.createElement('div');
            body.className = 'issue-toggle-body';
            
            const content = document.createElement('div');
            content.className = 'issue-toggle-content';
            
            // Adiciona todas as descrições da categoria
            points.forEach((point, index) => {
                const desc = document.createElement('p');
                desc.className = 'issue-description';
                desc.innerHTML = `${points.length > 1 ? `<strong>${index + 1}.</strong> ` : ''}${point.description}`;
                content.appendChild(desc);
                
                // Adiciona espaçamento entre múltiplas descrições
                if (index < points.length - 1) {
                    content.appendChild(document.createElement('br'));
                }
            });
            
            body.appendChild(content);
            
            // Toggle ao clicar
            header.addEventListener('click', () => {
                toggleItem.classList.toggle('expanded');
            });
            
            toggleItem.appendChild(header);
            toggleItem.appendChild(body);
            issuesList.appendChild(toggleItem);
        });
    } else {
        issuesList.innerHTML = '<p class="no-data">✅ Nenhum problema crítico identificado!</p>';
    }
}

// Função auxiliar para obter label de severidade
function getSeverityLabel(severity) {
    const labels = {
        'high': 'Alto',
        'medium': 'Médio',
        'low': 'Baixo'
    };
    return labels[severity] || 'Médio';
}

// Funções auxiliares
function hideAll() {
    errorDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    loadingDiv.classList.add('hidden');
}

function showError(message) {
    hideAll();
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
}

function showMessage(message, type = 'info') {
    // Remove mensagens anteriores
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Cria nova mensagem
    const tempDiv = document.createElement('div');
    tempDiv.className = `message ${type}`;
    tempDiv.textContent = message;
    tempDiv.style.cssText = 'padding:10px;margin:10px 0;border-radius:6px;font-size:13px;animation:fadeIn 0.3s;border:1px solid;';
    
    if (type === 'success') {
        tempDiv.style.background = '#d4edda';
        tempDiv.style.color = '#155724';
        tempDiv.style.borderColor = '#c3e6cb';
    }
    if (type === 'warning') {
        tempDiv.style.background = '#fff3cd';
        tempDiv.style.color = '#856404';
        tempDiv.style.borderColor = '#ffeaa7';
    }
    if (type === 'error') {
        tempDiv.style.background = '#f8d7da';
        tempDiv.style.color = '#721c24';
        tempDiv.style.borderColor = '#f5c6cb';
    }
    
    const inputSection = document.querySelector('.input-section');
    if (inputSection) {
        inputSection.appendChild(tempDiv);
        setTimeout(() => tempDiv.remove(), 4000);
    }
}

function getScoreClass(score) {
    if (score >= 80) return 'score-good';
    if (score >= 60) return 'score-medium';
    return 'score-bad';
}

function getSeverityIcon(severity) {
    const icons = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🟢'
    };
    return icons[severity] || '🟡';
}

async function checkApiStatus() {
    try {
        const response = await fetch('http://localhost:8000/api/v1/evaluate', {
            method: 'OPTIONS'
        });
        
        apiStatusDot.style.color = '#4caf50';
        apiStatusText.textContent = 'Conectado';
    } catch (error) {
        apiStatusDot.style.color = '#f44336';
        apiStatusText.textContent = 'Desconectado';
    }
}

