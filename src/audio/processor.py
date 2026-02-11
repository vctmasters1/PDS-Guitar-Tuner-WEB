"""Audio processor for WebRTC stream handling"""

import numpy as np
from src.core.config import GUITAR_STRINGS
from src.audio.capture import AudioCapture
from src.state.session import update_detected_frequency, get_tuner


class AudioProcessor:
    """Processes audio from WebRTC stream and detects guitar frequencies."""
    
    def __init__(self):
        """Initialize the audio processor with an AudioCapture instance."""
        self.audio_capture = AudioCapture()
    
    def recv(self, frame):
        """
        Process incoming audio frame from WebRTC stream.
        
        Args:
            frame: Audio frame from WebRTC stream
            
        Returns:
            frame: The audio frame (unchanged)
        """
        try:
            import streamlit as st
            
            # Convert frame to numpy array
            audio = frame.to_ndarray()
            
            # Detect frequency
            frequency = self.audio_capture.detect_frequency(audio)
            
            # Calculate audio level
            level_db = self.audio_capture.calculate_level_db(audio)
            
            # Update session state with level
            if level_db is not None:
                st.session_state.audio_level_db = level_db
            
            if frequency and frequency > 60:
                tuner = get_tuner()
                
                # Find closest guitar string
                min_distance = float('inf')
                closest_string_idx = None
                
                for idx, (_, note_name, octave_offset) in enumerate(GUITAR_STRINGS):
                    target_freq = tuner.calculate_frequency(
                        note_name, octave_offset
                    )
                    distance = abs(frequency - target_freq)
                    
                    if distance < min_distance:
                        min_distance = distance
                        closest_string_idx = idx
                
                if closest_string_idx is not None and min_distance < 50:
                    # Calculate cents deviation
                    target = tuner.calculate_frequency(
                        GUITAR_STRINGS[closest_string_idx][1],
                        GUITAR_STRINGS[closest_string_idx][2]
                    )
                    cents = 1200 * np.log2(frequency / target)
                    
                    # Update session state
                    update_detected_frequency(frequency, closest_string_idx, cents)
        except Exception as e:
            # Silently handle errors in audio processing
            import streamlit as st
            # Only log if explicitly debugging
            pass
        
        return frame
