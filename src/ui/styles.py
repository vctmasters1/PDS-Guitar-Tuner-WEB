"""UI Styling and CSS constants for Guitar Tuner"""

from src.core.config import COLORS


def get_base_styles() -> str:
    """Get base CSS styling for the application."""
    return f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: {COLORS['bg_dark']};
    }}
    .stApp {{
        background-color: {COLORS['bg_dark']};
    }}
    h1, h2, h3 {{
        color: {COLORS['text_primary']};
    }}
    
    .header-section {{
        background-color: {COLORS['bg_medium']};
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }}
    </style>
    """


def get_string_row_styles(string_color: str, bg_color: str, text_primary: str, 
                          text_secondary: str) -> str:
    """Get CSS for a guitar string row."""
    return f"""
    <div style="
        background-color: {string_color};
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 20px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    "></div>
    """


def get_frequency_display_styles(bg_color: str, text_primary: str, 
                                 text_secondary: str, label: str, 
                                 frequency: float, note: str, 
                                 secondary_text: str = "") -> str:
    """Get CSS for frequency display."""
    secondary_line = f"""<div style="color: {text_secondary}; font-size: 11px; margin-top: 5px;">{secondary_text}</div>""" if secondary_text else ""
    return f"""
    <div style="
        background-color: {bg_color};
        padding: 15px;
        border-radius: 5px;
        height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
    <div style="color: {text_secondary}; font-size: 12px;">{label}</div>
    <div style="color: {text_primary}; font-size: 16px; font-weight: bold;">{frequency:.2f} Hz</div>
    {secondary_line}
    </div>
    """


def get_status_indicator_styles(status_color: str, text_color: str, 
                                status_text: str) -> str:
    """Get CSS for status indicator."""
    return f"""
    <div style="
        background-color: {status_color}22;
        border-left: 4px solid {status_color};
        padding: 15px;
        border-radius: 5px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
    <div style="color: {status_color}; font-size: 14px; font-weight: bold; text-align: center;">{status_text}</div>
    </div>
    """
