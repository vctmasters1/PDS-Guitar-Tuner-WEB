"""Core tuner logic for frequency analysis and calculations"""

import numpy as np
from core.config import (
    IN_TUNE_THRESHOLD,
    CLOSE_THRESHOLD,
    TEMPERAMENT_EQUAL,
    TEMPERAMENT_JUST,
)


class GuitarTuner:
    """Handles guitar tuning calculations and analysis."""

    # Just Intonation ratios from C
    JUST_RATIOS_FROM_C = {
        "C": 1 / 1,
        "C#": 16 / 15,
        "D": 9 / 8,
        "D#": 6 / 5,
        "E": 5 / 4,
        "F": 4 / 3,
        "F#": 45 / 32,
        "G": 3 / 2,
        "G#": 8 / 5,
        "A": 5 / 3,
        "A#": 9 / 5,
        "B": 15 / 8,
    }

    def __init__(self, reference_freq=440.0, temperament=TEMPERAMENT_EQUAL):
        self.reference_freq = reference_freq
        self.temperament = temperament

    def set_reference_frequency(self, freq):
        """Set the reference tuning frequency (A4)."""
        self.reference_freq = freq

    def set_temperament(self, temperament):
        """Set the temperament system."""
        self.temperament = temperament

    def calculate_frequency(self, note_name, octave_offset=0):
        """
        Calculate frequency for a note based on temperament system.

        Args:
            note_name: Note name (e.g., 'E', 'A', 'D')
            octave_offset: Octave offset from A4

        Returns:
            float: Frequency in Hz
        """
        if self.temperament == TEMPERAMENT_EQUAL:
            return self._calculate_equal_temperament(note_name, octave_offset)
        else:
            return self._calculate_just_intonation(note_name, octave_offset)

    def _calculate_equal_temperament(self, note_name, octave_offset=0):
        """Calculate frequency using equal temperament (12-TET)."""
        note_semitones = {
            "C": -9,
            "C#": -8,
            "D": -7,
            "D#": -6,
            "E": -5,
            "F": -4,
            "F#": -3,
            "G": -2,
            "G#": -1,
            "A": 0,
            "A#": 1,
            "B": 2,
        }

        semitone_offset = note_semitones.get(note_name, 0)
        semitone_offset += octave_offset * 12

        return self.reference_freq * (2 ** (semitone_offset / 12))

    def _calculate_just_intonation(self, note_name, octave_offset=0):
        """Calculate frequency using just intonation."""
        # Base frequency of C in same octave as reference
        c_freq = self.reference_freq / (5 / 3)  # A4 / (5/3) = C4

        ratio = self.JUST_RATIOS_FROM_C.get(note_name, 1.0)
        base_freq = c_freq * ratio

        # Apply octave offset
        return base_freq * (2 ** octave_offset)

    def calculate_cents(self, detected_freq, target_freq):
        """
        Calculate cents deviation from target frequency.

        Args:
            detected_freq: The detected frequency
            target_freq: The target frequency

        Returns:
            float: Cents deviation (positive = sharp, negative = flat)
        """
        if target_freq == 0 or detected_freq == 0:
            return 0
        return 1200 * np.log2(detected_freq / target_freq)

    def get_tuning_status(self, cents):
        """
        Determine tuning status based on cents deviation.

        Args:
            cents: Cents deviation from target

        Returns:
            tuple: (status_text, color_status)
        """
        abs_cents = abs(cents)

        if abs_cents < IN_TUNE_THRESHOLD:
            return "✓ In Tune!", "green"
        elif abs_cents < CLOSE_THRESHOLD:
            direction = "↑ Sharp" if cents > 0 else "↓ Flat"
            return f"{direction} {abs_cents:.1f}¢", "orange"
        else:
            direction = "↑ Sharp" if cents > 0 else "↓ Flat"
            return f"{direction} {abs_cents:.1f}¢", "red"

    def find_closest_string(self, detected_freq, guitar_strings):
        """
        Find the closest guitar string to detected frequency.

        Args:
            detected_freq: The detected frequency
            guitar_strings: List of (name, base_freq, note) tuples

        Returns:
            tuple: (string_index, display_name, note_name, octave_offset, target_freq)
                   or None if not found
        """
        if not detected_freq:
            return None

        # Define frequency ranges for each string
        bands = []
        for i, (display_name, base_freq, note_name) in enumerate(guitar_strings):
            target_freq = self.calculate_frequency(note_name, octave_offset=-1)
            # Band is roughly ±50 cents around target
            low = target_freq * (2 ** (-50 / 1200))
            high = target_freq * (2 ** (50 / 1200))
            bands.append((i, display_name, note_name, -1, target_freq, low, high))

        # Find band match
        for i, display_name, note_name, octave_offset, target_freq, low, high in bands:
            if low <= detected_freq <= high:
                return (i, display_name, note_name, octave_offset, target_freq)

        # Fallback to closest target
        closest = min(
            bands, key=lambda x: abs(detected_freq - x[4])
        )
        
        cents_diff = abs(self.calculate_cents(detected_freq, closest[4]))
        if cents_diff > 50:  # More than 50 cents off
            return None

        return (closest[0], closest[1], closest[2], closest[3], closest[4])
