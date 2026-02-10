"""Audio capture module for web-based guitar tuner"""

import numpy as np
from scipy.fft import fft
from scipy.signal import find_peaks
import streamlit as st
from core.config import CHUNK_SIZE, SAMPLE_RATE


class AudioCapture:
    """Handles audio input and frequency detection via FFT."""

    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.chunk_size = CHUNK_SIZE

    def detect_frequency(self, audio_data):
        """
        Detect fundamental frequency using FFT.

        Args:
            audio_data: Audio waveform array

        Returns:
            float: Detected frequency in Hz, or None if detection fails
        """
        if audio_data is None or len(audio_data) == 0:
            return None

        # Convert to numpy array if needed
        if not isinstance(audio_data, np.ndarray):
            audio_data = np.array(audio_data, dtype=np.float32)

        # Apply Hanning window
        windowed = audio_data * np.hanning(len(audio_data))

        # Compute FFT
        fft_data = np.abs(fft(windowed))
        fft_data = fft_data[: len(fft_data) // 2]

        # Find peaks
        threshold = np.max(fft_data) * 0.3
        if threshold < 0.01:
            return None

        peaks, properties = find_peaks(fft_data, height=threshold)

        if len(peaks) == 0:
            return None

        # Get the strongest peak
        peak_idx = peaks[np.argmax(properties["peak_heights"])]

        # Convert to frequency
        freq = peak_idx * self.sample_rate / len(audio_data)

        # Filter for guitar range (60 Hz to 1000 Hz)
        if 60 < freq < 1000:
            return freq

        return None

    def calculate_level_db(self, audio_data):
        """
        Calculate RMS level in dBFS.

        Args:
            audio_data: Audio waveform array

        Returns:
            float: Level in dBFS
        """
        if audio_data is None or len(audio_data) == 0:
            return None

        if not isinstance(audio_data, np.ndarray):
            audio_data = np.array(audio_data, dtype=np.float32)

        rms = np.sqrt(np.mean(audio_data ** 2))
        if rms > 0:
            return 20 * np.log10(rms)
        return -100  # Very quiet
