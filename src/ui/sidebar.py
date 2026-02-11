"""Sidebar settings component for Guitar Tuner UI"""

import streamlit as st
from src.core.config import (
    TUNING_PRESETS,
    TEMPERAMENT_EQUAL,
    TEMPERAMENT_JUST,
    DEFAULT_TOLERANCE_HZ,
)
from src.core.tuner import GuitarTuner


@st.dialog("Temperament Systems", width="large")
def show_temperament_info():
    """Display temperament system information in a fullscreen modal dialog."""
    st.markdown(
        """
        ## Equal Temperament (12-TET)
        
        The Western music standard where the octave is divided into 12 equal semitones.
        Each semitone has a frequency ratio of 2^(1/12) ≈ 1.0595.
        
        **Advantages:**
        - Universal standard for modern instruments
        - Same intervals between all semitones
        - Works in any key
        - Practical for retuning
        
        **Disadvantages:**
        - No perfectly pure intervals (except octaves)
        - Some chord combinations sound slightly impure
        
        **Best for:** Guitar, keyboard, most modern music
        
        [Learn more on Wikipedia](https://en.wikipedia.org/wiki/Equal_temperament)
        
        ---
        
        ## Just Intonation
        
        A tuning system based on pure harmonic ratios derived from the harmonic series.
        Each note frequency is a simple ratio of the base frequency.
        
        **Common ratios (from C):**
        - 1/1 (Unison)
        - 9/8 (Major Second)
        - 5/4 (Major Third)
        - 4/3 (Perfect Fourth)
        - 3/2 (Perfect Fifth)
        - 5/3 (Major Sixth)
        - 15/8 (Major Seventh)
        - 2/1 (Octave)
        
        **Advantages:**
        - Mathematically pure intervals
        - Natural consonance in harmonic relationships
        - No beating when properly tuned
        
        **Disadvantages:**
        - Different ratios needed for each key
        - Requires frequent retuning when changing keys
        - Not standard for fretted instruments
        
        **Best for:** A cappella singing, certain acoustic instruments, experimental music
        
        [Learn more on Wikipedia](https://en.wikipedia.org/wiki/Just_intonation)
        """
    )


def render_sidebar(default_reference_freq: float, default_temperament: str):
    """
    Render the settings sidebar.
    
    Args:
        default_reference_freq: Default reference frequency in Hz
        default_temperament: Default temperament system
    """
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Reference frequency selection
        st.subheader("Tuning Reference")
        preset_labels = [f"{name} ({freq} Hz)" for name, freq in TUNING_PRESETS]
        
        # Initialize custom_freq_input in session state if not present
        if "custom_freq_input" not in st.session_state:
            st.session_state.custom_freq_input = default_reference_freq
        
        def on_preset_change():
            """Callback when tuning preset selection changes"""
            selected_idx = preset_labels.index(st.session_state.tuning_select)
            preset_freq = TUNING_PRESETS[selected_idx][1]
            st.session_state.custom_freq_input = preset_freq
        
        selected_preset = st.selectbox(
            "Select tuning reference:",
            preset_labels,
            index=1,  # Default to 440 Hz
            key="tuning_select",
            on_change=on_preset_change,
        )
        
        # Custom frequency input
        st.markdown("**Or enter custom frequency:**")
        custom_freq = st.number_input(
            "Custom frequency (Hz)",
            min_value=400.0,
            max_value=460.0,
            step=0.1,
            key="custom_freq_input",
        )
        
        # Use custom if different from preset
        actual_freq = custom_freq
        st.session_state.reference_freq = actual_freq
        
        # Temperament selection with info
        st.subheader("Temperament System")
        
        temperament_options = [
            (TEMPERAMENT_EQUAL, "Equal Temperament (12-TET)"),
            (TEMPERAMENT_JUST, "Just Intonation")
        ]
        
        col_radio, col_info = st.columns([3, 1])
        
        with col_radio:
            selected_temp_idx = 0 if st.session_state.temperament == TEMPERAMENT_EQUAL else 1
            temp_choice = st.radio(
                "Select temperament:",
                [opt[1] for opt in temperament_options],
                index=selected_temp_idx,
                key="temperament_radio",
            )
            st.session_state.temperament = temperament_options[
                [opt[1] for opt in temperament_options].index(temp_choice)
            ][0]
        
        with col_info:
            if st.button("ℹ️", key="temp_info_btn", help="Learn about temperament systems"):
                show_temperament_info()
        
        # CRITICAL: Recreate tuner AFTER all settings are determined
        st.session_state.tuner = GuitarTuner(
            st.session_state.reference_freq,
            st.session_state.temperament
        )
        
        # Tolerance setting
        st.subheader("Tuning Tolerance")
        tolerance = st.slider(
            "Tolerance (Hz):",
            min_value=0.1,
            max_value=5.0,
            value=st.session_state.tolerance_hz,
            step=0.1,
            key="tolerance_slider",
        )
        st.session_state.tolerance_hz = tolerance
        
        st.divider()
        st.info(
            "📱 Grant microphone access to use the tuner. Allow the browser to access your microphone."
        )
        
        st.divider()
        if st.checkbox("Show Information", value=False):
            st.markdown(
                """
                ### How to Use
                1. **Grant Microphone Access**: Click "Allow" when the browser asks
                2. **Select Tuning**: Choose your reference frequency
                3. **Play a String**: Pluck a guitar string near your microphone
                4. **Read Feedback**:
                   - ✓ IN TUNE = String is tuned correctly
                   - ~ CLOSE = String is close
                   - ✗ OFF = String needs adjustment
                5. **Tune**: Adjust the string until it shows green
                
                ### Tips
                - Keep environment quiet
                - Play one string at a time
                - Keep microphone 6-12 inches away
                """
            )
