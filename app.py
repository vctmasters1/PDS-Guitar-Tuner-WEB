"""
🎸 Guitar Tuner - Web App
A real-time guitar tuner using frequency detection and visual feedback.
Streamlit-based web application.
"""

import sys
from pathlib import Path
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.tuner import GuitarTuner
from core.config import (
    GUITAR_STRINGS,
    TUNING_PRESETS,
    DEFAULT_REFERENCE_FREQ,
    DEFAULT_TEMPERAMENT,
    TEMPERAMENT_EQUAL,
    TEMPERAMENT_JUST,
    COLORS,
    STRING_COLORS,
    DEFAULT_TOLERANCE_HZ,
)
from audio.capture import AudioCapture


# Page configuration
st.set_page_config(
    page_title="🎸 Guitar Tuner",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stApp {
        background-color: #1e1e1e;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .metric-card {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #0066cc;
    }
    .in-tune {
        color: #00cc00;
        font-weight: bold;
    }
    .close {
        color: #ffff00;
        font-weight: bold;
    }
    .off-tune {
        color: #cc0000;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables"""
    if "reference_freq" not in st.session_state:
        st.session_state.reference_freq = DEFAULT_REFERENCE_FREQ
    if "temperament" not in st.session_state:
        st.session_state.temperament = DEFAULT_TEMPERAMENT
    if "tolerance_hz" not in st.session_state:
        st.session_state.tolerance_hz = DEFAULT_TOLERANCE_HZ
    if "detected_frequency" not in st.session_state:
        st.session_state.detected_frequency = None
    if "current_string" not in st.session_state:
        st.session_state.current_string = None
    if "cents_deviation" not in st.session_state:
        st.session_state.cents_deviation = 0


def create_frequency_chart(frequency, target_freq=None):
    """Create an interactive frequency chart"""
    fig = go.Figure()

    # Simulated FFT data centered around detected frequency
    if frequency:
        x_range = np.linspace(frequency - 100, frequency + 100, 100)
        # Create a Gaussian-like peak at detected frequency
        y_data = np.exp(-((x_range - frequency) ** 2) / (2 * 50 ** 2)) * 1000
    else:
        x_range = np.linspace(50, 300, 100)
        y_data = np.zeros_like(x_range)

    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=y_data,
            mode="lines",
            name="Detected",
            line=dict(color="#0066cc", width=2),
            fill="tozeroy",
        )
    )

    # Add target frequency line
    if target_freq:
        fig.add_vline(
            x=target_freq,
            line_dash="dash",
            line_color="green",
            annotation_text="Target",
            annotation_position="top left",
        )

    if frequency:
        fig.add_vline(
            x=frequency,
            line_dash="solid",
            line_color="orange",
            annotation_text="Detected",
            annotation_position="top right",
        )

    fig.update_layout(
        title="Frequency Spectrum",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude",
        template="plotly_dark",
        height=400,
        showlegend=True,
        hovermode="x unified",
    )

    return fig


def create_tuner_gauge(cents_deviation, tolerance_hz):
    """Create a gauge chart for tuning accuracy"""
    # Color based on deviation
    if abs(cents_deviation) < 5:
        color = "green"
        status = "IN TUNE"
    elif abs(cents_deviation) < 50:
        color = "yellow"
        status = "CLOSE"
    else:
        color = "red"
        status = "OFF"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=abs(cents_deviation),
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Tuning Accuracy (Cents)"},
            delta={"reference": 0, "suffix": " ¢"},
            gauge={
                "axis": {"range": [None, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 5], "color": "rgba(0, 204, 0, 0.2)"},
                    {"range": [5, 50], "color": "rgba(255, 255, 0, 0.2)"},
                    {"range": [50, 100], "color": "rgba(204, 0, 0, 0.2)"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 5,
                },
            },
            number={"suffix": " ¢", "font": {"size": 28, "color": color}},
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        margin=dict(l=20, r=20, t=70, b=20),
    )

    return fig


def create_string_indicator(strings_data):
    """Create string tuning indicators"""
    cols = st.columns(len(GUITAR_STRINGS))

    for idx, (col, string_info) in enumerate(zip(cols, strings_data)):
        with col:
            name, status, color = string_info
            st.markdown(
                f"""
                <div style="text-align: center; padding: 20px; background-color: #2d2d2d; border-radius: 10px; border: 3px solid {color};">
                    <h3 style="margin: 0; color: #ffffff;">{name}</h3>
                    <p style="color: {color}; font-size: 18px; font-weight: bold; margin: 10px 0;">{status}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def main():
    """Main Streamlit application"""
    initialize_session_state()

    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🎸 Guitar Tuner")
        st.markdown(
            "Real-time guitar tuning with frequency detection and visual feedback"
        )

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        # Reference frequency selection
        st.subheader("Tuning Reference")
        selected_preset = st.selectbox(
            "Select tuning reference:",
            [f"{name} ({freq} Hz)" for name, freq in TUNING_PRESETS],
            index=1,  # Default to 440 Hz
        )

        # Extract frequency from selection
        preset_freq = TUNING_PRESETS[
            [f"{name} ({freq} Hz)" for name, freq in TUNING_PRESETS].index(
                selected_preset
            )
        ][1]
        st.session_state.reference_freq = preset_freq

        # Custom frequency input
        st.markdown("**Or enter custom frequency:**")
        custom_freq = st.number_input(
            "Custom frequency (Hz)",
            min_value=400.0,
            max_value=460.0,
            value=float(st.session_state.reference_freq),
            step=0.1,
        )
        if custom_freq != st.session_state.reference_freq:
            st.session_state.reference_freq = custom_freq

        # Temperament selection
        st.subheader("Temperament System")
        temperament = st.radio(
            "Select temperament:",
            [TEMPERAMENT_EQUAL, TEMPERAMENT_JUST],
            index=0 if st.session_state.temperament == TEMPERAMENT_EQUAL else 1,
        )
        st.session_state.temperament = temperament

        # Tolerance setting
        st.subheader("Tuning Tolerance")
        tolerance = st.slider(
            "Tolerance (Hz):",
            min_value=0.1,
            max_value=5.0,
            value=st.session_state.tolerance_hz,
            step=0.1,
        )
        st.session_state.tolerance_hz = tolerance

        st.markdown("---")
        st.info(
            "📱 Grant microphone access to use the tuner. Allow the browser to access your microphone."
        )

    # Main content
    st.markdown("### 🎤 Audio Input")

    # WebRTC configuration
    rtc_configuration = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    class AudioProcessor:
        def __init__(self):
            self.audio_capture = AudioCapture()
            self.tuner = GuitarTuner(
                st.session_state.reference_freq,
                st.session_state.temperament,
            )

        def recv(self, frame):
            audio = frame.to_ndarray()

            # Detect frequency
            frequency = self.audio_capture.detect_frequency(audio)

            if frequency:
                # Find closest string
                result = self.tuner.find_closest_string(frequency, GUITAR_STRINGS)

                if result:
                    (
                        string_idx,
                        display_name,
                        note_name,
                        octave_offset,
                        target_freq,
                    ) = result
                    cents = self.tuner.calculate_cents(frequency, target_freq)

                    st.session_state.detected_frequency = frequency
                    st.session_state.current_string = (
                        string_idx,
                        display_name,
                        note_name,
                        target_freq,
                    )
                    st.session_state.cents_deviation = cents

            return frame

    # WebRTC streamer
    webrtc_ctx = webrtc_streamer(
        key="guitar-tuner",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    if webrtc_ctx.state.playing:
        st.success("🎤 Microphone connected!")

    # Display metrics
    if st.session_state.detected_frequency:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Detected Frequency",
                f"{st.session_state.detected_frequency:.2f} Hz",
                delta=f"{st.session_state.cents_deviation:.1f}¢",
            )

        if st.session_state.current_string:
            string_idx, display_name, note_name, target_freq = (
                st.session_state.current_string
            )

            with col2:
                st.metric("Current String", display_name)

            with col3:
                st.metric("Target Frequency", f"{target_freq:.2f} Hz")

            with col4:
                status, _ = st.session_state.tuner.get_tuning_status(
                    st.session_state.cents_deviation
                ) if hasattr(st.session_state, 'tuner') else ("--", "gray")
                st.metric("Status", status)

    # Charts section
    st.markdown("### 📊 Visual Feedback")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Frequency chart
        if st.session_state.detected_frequency:
            target = (
                st.session_state.current_string[3]
                if st.session_state.current_string
                else None
            )
            fig = create_frequency_chart(st.session_state.detected_frequency, target)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🎵 Play a note to see frequency analysis")

    with chart_col2:
        # Tuner gauge
        if st.session_state.detected_frequency:
            fig = create_tuner_gauge(
                st.session_state.cents_deviation, st.session_state.tolerance_hz
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🎵 Play a note to see tuning accuracy")

    # String status
    st.markdown("### 🎸 String Status")
    if st.session_state.current_string:
        string_idx = st.session_state.current_string[0]
        strings_status = []

        for i, (name, _, note) in enumerate(GUITAR_STRINGS):
            if i == string_idx:
                cents = st.session_state.cents_deviation
                if abs(cents) < 5:
                    status = "✓ IN TUNE"
                    color = "#00cc00"
                elif abs(cents) < 50:
                    status = "~ CLOSE"
                    color = "#ffff00"
                else:
                    status = "✗ OFF"
                    color = "#cc0000"
            else:
                status = "-- MUTED"
                color = "#666666"

            strings_status.append((name, status, color))

        create_string_indicator(strings_status)
    else:
        st.info("🎵 Play a guitar string to see status indicators")

    # Information section
    st.markdown("---")
    with st.expander("ℹ️ How to use"):
        st.markdown(
            """
        1. **Grant Microphone Access**: Click "Allow" when the browser asks for microphone permission
        2. **Select Tuning**: Choose your reference frequency (or enter custom value)
        3. **Play a String**: Pluck a guitar string near your microphone
        4. **Read the Feedback**: 
           - Green ✓ = String is in tune
           - Yellow ~ = String is close to in tune
           - Red ✗ = String needs adjustment
        5. **Tune**: Adjust the string until it shows green

        **Tips:**
        - Ensure a quiet environment for better detection
        - Play one string at a time
        - Keep the microphone at a reasonable distance (6-12 inches)
        """
        )

    with st.expander("🔧 Technical Info"):
        st.markdown(
            f"""
        **Current Settings:**
        - Reference Frequency: {st.session_state.reference_freq} Hz
        - Temperament: {st.session_state.temperament}
        - Tolerance: {st.session_state.tolerance_hz} Hz

        **How It Works:**
        - Uses Fast Fourier Transform (FFT) to analyze audio
        - Detects the fundamental frequency of the note
        - Compares to expected guitar string frequencies
        - Shows deviation in cents (100 cents = 1 semitone)
        """
        )


if __name__ == "__main__":
    main()
