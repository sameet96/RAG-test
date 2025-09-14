#!/usr/bin/env python3
"""
Preview script to show the new portfolio-style UI
Run this to see how the updated interface looks
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI PDF Chat Preview | Sameet Sonawane",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.main {
    padding: 2rem 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

.portfolio-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.portfolio-header h1 {
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #ffffff, #f0f0f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.portfolio-header p {
    font-family: 'Inter', sans-serif;
    font-size: 1.2rem;
    opacity: 0.9;
    font-weight: 300;
    margin-bottom: 0;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 2rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.feature-card h3 {
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    margin-bottom: 1rem;
}

.feature-card p {
    color: rgba(255, 255, 255, 0.8);
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1.5rem;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Portfolio-style header
st.markdown("""
<div class="portfolio-header">
    <h1>🤖 AI PDF Chat</h1>
    <p>Intelligent Document Analysis & Q&A System</p>
</div>
""", unsafe_allow_html=True)

# Feature showcase
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <h3>Smart PDF Processing</h3>
        <p>Extract text, images, and tables from PDF documents with advanced OCR capabilities</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <h3>RAG Technology</h3>
        <p>Retrieval-Augmented Generation system that understands document context</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>Natural Conversations</h3>
        <p>Ask questions in natural language and get intelligent responses</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Demo content
st.markdown("## 🎨 New Portfolio-Style Design")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✨ Design Features")
    st.markdown("""
    - **Modern Gradient Headers**: Eye-catching purple-blue gradients
    - **Glass Morphism Cards**: Translucent cards with backdrop blur
    - **Inter Font Family**: Clean, professional typography
    - **Smooth Animations**: Hover effects and transitions
    - **Responsive Grid**: Adapts to different screen sizes
    - **Custom Scrollbars**: Branded scrollbar styling
    """)

with col2:
    st.markdown("### 🚀 Portfolio Integration")
    st.markdown("""
    - **Branded Header**: Matches your portfolio aesthetic
    - **Professional Footer**: Links to your portfolio and GitHub
    - **Consistent Colors**: Purple-blue gradient theme
    - **Clean Layout**: Minimal, focused design
    - **Interactive Elements**: Engaging hover effects
    - **Mobile Responsive**: Works on all devices
    """)

# Interactive demo
st.markdown("### 🎯 Interactive Demo")

if st.button("🚀 Launch Full Application", type="primary"):
    st.success("Ready to launch! Run `python run.py` to start the full application.")

if st.button("📱 View Portfolio Integration"):
    st.info("Check the portfolio integration files in the project directory!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.7);">
    <p style="font-family: 'Inter', sans-serif; font-size: 0.9rem; margin: 0;">
        Built with ❤️ by <strong>Sameet Sonawane</strong> | 
        <a href="https://www.sameetsonawane.com" style="color: #667eea; text-decoration: none;">Portfolio</a> | 
        <a href="https://github.com/sameetsonawane" style="color: #667eea; text-decoration: none;">GitHub</a>
    </p>
    <p style="font-family: 'Inter', sans-serif; font-size: 0.8rem; margin: 0.5rem 0 0 0; opacity: 0.6;">
        Powered by OpenAI GPT, ChromaDB, and Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
