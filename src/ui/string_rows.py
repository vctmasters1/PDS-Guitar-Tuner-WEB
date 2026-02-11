"""Guitar string rows component for Guitar Tuner UI"""

import streamlit as st
from src.core.config import (
    GUITAR_STRINGS,
    COLORS,
    STRING_COLORS,
    IN_TUNE_THRESHOLD,
    CLOSE_THRESHOLD,
)


def get_tuning_status(cents):
    """Get tuning status based on cents deviation."""
    if cents is None:
        return "IDLE", COLORS['status_inactive']
    
    cents_abs = abs(cents)
    if cents_abs <= IN_TUNE_THRESHOLD:
        return "✓ IN TUNE", COLORS['status_in_tune']
    elif cents_abs <= CLOSE_THRESHOLD:
        return "~ CLOSE", COLORS['status_close']
    else:
        return "✗ OFF", COLORS['status_off']


def render_string_rows():
    """
    Render the 6 guitar string rows on the left side.
    
    Each row displays:
    - String name with color
    - Target frequency (calculated mathematically)
    - Detected frequency and cents deviation
    - Tuning status indicator
    """
    st.markdown("### 🎸 String Tuning")
    
    for idx, (display_name, note_name, octave_offset) in enumerate(GUITAR_STRINGS):
        string_color = STRING_COLORS[idx]
        bg_color = COLORS['bg_medium']
        
        # CRITICAL: Calculate target frequency using current tuner
        target_freq = st.session_state.tuner.calculate_frequency(note_name, octave_offset)
        
        # Determine if this is the current string being detected
        is_current_string = idx == st.session_state.current_string_idx
        detected_freq = st.session_state.detected_frequency if is_current_string else None
        cents = st.session_state.cents_deviation if is_current_string else 0
        status_text, status_color = get_tuning_status(cents if is_current_string else None)
        
        # Create row container
        col1, col2, col3, col4 = st.columns([0.8, 2, 2, 1.5])
        
        with col1:
            st.markdown(
                f"""
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
                ">
                {display_name}
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    padding: 15px;
                    border-radius: 5px;
                    height: 80px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                <div style="color: {COLORS['text_secondary']}; font-size: 12px;">Target Frequency</div>
                <div style="color: {COLORS['text_primary']}; font-size: 16px; font-weight: bold;">{target_freq:.2f} Hz</div>
                <div style="color: {COLORS['text_secondary']}; font-size: 11px; margin-top: 5px;">{note_name}{4 + octave_offset}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col3:
            detected_text = f"{detected_freq:.2f} Hz" if detected_freq else "-- Hz"
            cents_text = f"{cents:+.1f}¢" if is_current_string else "-- ¢"
            
            st.markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    padding: 15px;
                    border-radius: 5px;
                    height: 80px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                <div style="color: {COLORS['text_secondary']}; font-size: 12px;">Detected Frequency</div>
                <div style="color: {COLORS['text_primary']}; font-size: 16px; font-weight: bold;">{detected_text}</div>
                <div style="color: {COLORS['text_secondary']}; font-size: 11px; margin-top: 5px;">Deviation: {cents_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col4:
            st.markdown(
                f"""
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
                """,
                unsafe_allow_html=True,
            )
        
        st.divider()
