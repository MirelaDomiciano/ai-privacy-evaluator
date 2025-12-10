import streamlit as st
import requests

API_URL = "http://backend:8000/api/v1/evaluate"

st.set_page_config(
    page_title="AI Privacy Policy Evaluator", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para reduzir tamanho da fonte das métricas
st.markdown("""
<style>
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔒 AI Privacy Policy Evaluator")
st.markdown("""
Avalie automaticamente políticas de privacidade usando Inteligência Artificial. 
Nossa ferramenta analisa documentos sob a ótica da **LGPD** e identifica riscos para sua privacidade.
""")
st.divider()

# Inicializar estado da sessão
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'result' not in st.session_state:
    st.session_state.result = None

# Input - expandido ou colapsado baseado no estado
input_expanded = not st.session_state.analysis_done

with st.expander("📄 Cole a política de privacidade para análise", expanded=input_expanded):
    policy_text = st.text_area(
        "Texto da política:",
        height=300,
        placeholder="Cole aqui o texto completo da política de privacidade que deseja avaliar...",
        help="Insira o texto integral da política que deseja analisar.",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Analisar Política"):
        if not policy_text.strip():
            st.warning("⚠️ Por favor, cole uma política para analisar.")
        else:
            with st.spinner("Analisando com IA... Isso pode levar alguns segundos."):
                try:
                    resp = requests.post(
                        API_URL,
                        json={"text": policy_text},
                        timeout=120
                    )
                    if resp.status_code == 200:
                        st.session_state.result = resp.json()
                        st.session_state.analysis_done = True
                        st.rerun()
                    else:
                        st.error(f"❌ Erro na API: {resp.status_code}\n{resp.json().get('detail')}")
                except Exception as e:
                    st.error(f"❌ Erro de conexão com o backend: {e}")

# Mostrar resultados se a análise foi feita
if st.session_state.analysis_done and st.session_state.result:
    result = st.session_state.result
    
    # Success message
    st.success("✅ Análise concluída com sucesso!")
    st.divider()
    
    # Barra superior com métricas de risco
    score = result['risk_score']
    if score >= 7:
        score_text = "Alto Risco"
    elif score >= 4:
        score_text = "Risco Moderado"
    else:
        score_text = "Baixo Risco"
    
    # Contadores por severidade
    high_count = sum(1 for rp in result["risk_points"] if rp["severity"] == "high")
    medium_count = sum(1 for rp in result["risk_points"] if rp["severity"] == "medium")
    low_count = sum(1 for rp in result["risk_points"] if rp["severity"] == "low")
    
    # Métricas em linha
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric(
            label="Pontuação de Risco",
            value=f"{score} / 10",
            delta=score_text,
            delta_color="inverse"
        )
    with metric_col2:
        st.metric("🔴 Alto", high_count)
    with metric_col3:
        st.metric("🟠 Médio", medium_count)
    with metric_col4:
        st.metric("🟢 Baixo", low_count)
    
    # Layout em duas colunas para conteúdo
    col1, col2 = st.columns([1, 1])
    
    # Coluna 1: Resumo
    with col1:
        st.markdown("### 📋 Resumo da Política")
        # Substituir \n literais por quebras de linha reais
        summary_text = result["summary"].replace("\\n", "\n")
        st.markdown(summary_text)
    
    # Coluna 2: Detalhamento dos Riscos
    with col2:
        st.markdown("### 📊 Detalhamento dos Riscos")
        
        # Lista de riscos
        for i, rp in enumerate(result["risk_points"], 1):
            emoji = "🔴" if rp["severity"] == "high" else ("🟠" if rp["severity"] == "medium" else "🟢")
            severity_label = {
                "high": "Alto",
                "medium": "Médio",
                "low": "Baixo"
            }[rp["severity"]]
            
            with st.expander(f"{emoji} **{rp['category']}**", expanded=(i <= 2)):
                st.markdown(f"**Severidade:** {severity_label}")
                st.markdown(rp['description'])

# Footer
st.divider()
st.caption("🎓 Projeto acadêmico — Powered by FastAPI + Gemini + Streamlit")
