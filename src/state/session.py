"""Session state management for Guitar Tuner application"""

from src.core.tuner import GuitarTuner
from src.audio.capture import AudioCapture
from src.core.config import (
    DEFAULT_REFERENCE_FREQ,
    DEFAULT_TEMPERAMENT,
    DEFAULT_TOLERANCE_HZ,
)


def initialize_session_state():
    """
    Initialize session state variables with proper tuner and audio instances.
    
    Session state variables:
    - reference_freq: Current tuning reference frequency (Hz)
    - temperament: Current temperament system ("equal" or "just")
    - tolerance_hz: Tuning tolerance threshold (Hz)
    - detected_frequency: Currently detected frequency (Hz or None)
    - current_string_idx: Index of the currently detected string (0-5 or None)
    - cents_deviation: Cents offset from target frequency
    - tuner: GuitarTuner instance for frequency calculations
    - audio_capture: AudioCapture instance for FFT analysis
    """
    import streamlit as st
    
    # Tuning settings
    if "reference_freq" not in st.session_state:
        st.session_state.reference_freq = DEFAULT_REFERENCE_FREQ
    
    if "temperament" not in st.session_state:
        st.session_state.temperament = DEFAULT_TEMPERAMENT
    
    if "tolerance_hz" not in st.session_state:
        st.session_state.tolerance_hz = DEFAULT_TOLERANCE_HZ
    
    # Detection state
    if "detected_frequency" not in st.session_state:
        st.session_state.detected_frequency = None
    
    if "current_string_idx" not in st.session_state:
        st.session_state.current_string_idx = None
    
    if "cents_deviation" not in st.session_state:
        st.session_state.cents_deviation = 0
    
    if "audio_level_db" not in st.session_state:
        st.session_state.audio_level_db = None
    
    # Core instances
    if "tuner" not in st.session_state:
        st.session_state.tuner = GuitarTuner(
            st.session_state.reference_freq,
            st.session_state.temperament
        )
    
    if "audio_capture" not in st.session_state:
        st.session_state.audio_capture = AudioCapture()


def get_tuner() -> GuitarTuner:
    """Get the active GuitarTuner instance."""
    import streamlit as st
    
    if "tuner" not in st.session_state:
        initialize_session_state()
    return st.session_state.tuner


def get_audio_capture() -> AudioCapture:
    """Get the active AudioCapture instance."""
    import streamlit as st
    
    if "audio_capture" not in st.session_state:
        initialize_session_state()
    return st.session_state.audio_capture


def update_detected_frequency(frequency: float, string_idx: int, cents: float):
    """
    Update the currently detected frequency and associated data.
    
    Args:
        frequency: Detected frequency in Hz
        string_idx: Index of the detected guitar string
        cents: Cents deviation from target
    """
    import streamlit as st
    
    st.session_state.detected_frequency = frequency
    st.session_state.current_string_idx = string_idx
    st.session_state.cents_deviation = cents


def clear_detected_frequency():
    """Clear the currently detected frequency."""
    import streamlit as st
    
    st.session_state.detected_frequency = None
    st.session_state.current_string_idx = None
    st.session_state.cents_deviation = 0
