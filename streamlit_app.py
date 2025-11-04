"""
LangChain v1.0 Middleware - Streamlit Interface

Interactive web interface for demonstrating middleware patterns in AI agent context control.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Import pages
from streamlit_pages import (
    home_page,
    logging_demo_page,
    token_budget_page,
    security_filter_page,
    context_summarization_page,
    expertise_based_page,
    middleware_stack_page,
    comparison_page,
    playground_page,
)

# Page configuration
st.set_page_config(
    page_title="LangChain v1.0 Middleware Demo",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Demo:",
    [
        "Home",
        "Logging Middleware",
        "Token Budget",
        "Security Filter",
        "Context Summarization",
        "Expertise-Based",
        "Middleware Stack",
        "Architecture Comparison",
        "Playground",
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This demo showcases LangChain v1.0's middleware architecture for systematic AI agent context control.

Built for AI developers and engineers.
""")

# Route to pages
if page == "Home":
    home_page()
elif page == "Logging Middleware":
    logging_demo_page()
elif page == "Token Budget":
    token_budget_page()
elif page == "Security Filter":
    security_filter_page()
elif page == "Context Summarization":
    context_summarization_page()
elif page == "Expertise-Based":
    expertise_based_page()
elif page == "Middleware Stack":
    middleware_stack_page()
elif page == "Architecture Comparison":
    comparison_page()
elif page == "Playground":
    playground_page()
