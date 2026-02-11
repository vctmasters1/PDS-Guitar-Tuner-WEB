"""Header component for Guitar Tuner UI"""

import streamlit as st
from src.ui.styles import get_base_styles


def render_header():
    """Render the main header section."""
    st.markdown(get_base_styles(), unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="header-section">
        <h1>🎸 Guitar Tuner</h1>
        <p>Real-time guitar tuning with frequency detection and visual feedback</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="🎸 Guitar Tuner",
        page_icon="🎸",
        layout="wide",
        initial_sidebar_state="expanded",
    )
