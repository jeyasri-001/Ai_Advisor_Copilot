import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from rag.hybrid_search import search

st.set_page_config(
    page_title="AI Advisor Copilot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f1419 0%, #1a1a2e 50%, #16213e 100%) !important;
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
        max-width: 800px !important;
        padding: 20px !important;
    }
    
    .main {
        background: transparent !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Header */
    .app-header {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
    }
    
    .app-title {
        color: #6366f1;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .app-subtitle {
        color: #ffffff;
        font-size: 24px;
        font-weight: 500;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: rgba(22, 33, 62, 0.8) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin: 12px 0 !important;
        max-width: 100% !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Chat input container */
    [data-testid="stChatInputContainer"] {
        background: transparent !important;
        padding: 0 !important;
        margin: 20px 0 !important;
    }
    
    [data-testid="stChatInputContainer"] input {
        background-color: rgba(22, 33, 62, 0.8) !important;
        border: 1px solid #5a7fa6 !important;
        color: #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 16px !important;
    }
    
    [data-testid="stChatInputContainer"] input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    [data-testid="stChatInputContainer"] input::placeholder {
        color: #7a8fa6 !important;
    }
    
    /* Buttons container */
    .button-row {
        margin-top: 15px;
    }
    
    /* Buttons */
    .stButton button {
        background-color: rgba(90, 127, 166, 0.2) !important;
        border: 1px solid #5a7fa6 !important;
        color: #a0aec0 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        background-color: rgba(99, 102, 241, 0.2) !important;
        border-color: #6366f1 !important;
        color: #6366f1 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #6366f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #818cf8;
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Header - Always visible
st.markdown("""
<div class="app-header">
    <div class="app-title">💼 AI Advisor Copilot</div>
    <div class="app-subtitle">What's on your mind?</div>
</div>
""", unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg['content'])
    else:
        with st.chat_message("assistant"):
            st.write(msg['content'])

# Chat input
query = st.chat_input("Message AI chat...")

# Action buttons - BELOW input
st.markdown('<div class="button-row">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📊 Fund Analysis"):
        query = "Analyze the top performing mutual funds for me"
        st.session_state.trigger_query = query
        st.rerun()

with col2:
    if st.button("💰 Investment Tips"):
        query = "Give me investment tips for beginners"
        st.session_state.trigger_query = query
        st.rerun()

with col3:
    if st.button("🎯 Risk Profile"):
        query = "What's my ideal risk profile for investing"
        st.session_state.trigger_query = query
        st.rerun()

with col4:
    if st.button("📈 Market Trends"):
        query = "What are the current market trends"
        st.session_state.trigger_query = query
        st.rerun()

with col5:
    if st.button("💡 Portfolio Tips"):
        query = "How should I build my investment portfolio"
        st.session_state.trigger_query = query
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Handle triggered query from buttons
if "trigger_query" in st.session_state:
    query = st.session_state.trigger_query
    del st.session_state.trigger_query

# Process query
if query:
    # Add user message
    st.session_state.history.append({"role": "user", "content": query})
    
    # Display user message
    with st.chat_message("user"):
        st.write(query)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Analyzing your query..."):
            try:
                import io
                buffer = io.StringIO()
                sys.stdout = buffer

                response = search(query, st.session_state.history)

                sys.stdout = sys.__stdout__
                
                if response:
                    st.write(response)
                    st.session_state.history.append({"role": "assistant", "content": response})
                else:
                    st.error("Could not generate response. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                sys.stdout = sys.__stdout__
    
    st.rerun()
