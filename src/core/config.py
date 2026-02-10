"""Configuration for Guitar Tuner"""

# Tuning constants
TEMPERAMENT_EQUAL = "Equal Temperament"
TEMPERAMENT_JUST = "Just Intonation"
DEFAULT_TEMPERAMENT = TEMPERAMENT_EQUAL

# Reference frequency
DEFAULT_REFERENCE_FREQ = 440.0

# Tuning presets (name, frequency)
TUNING_PRESETS = [
    ("432 Hz", 432.0),
    ("440 Hz (A4)", 440.0),
    ("442 Hz", 442.0),
    ("444 Hz", 444.0),
]

# Frequency update range
FREQ_UPDATE_RANGE = (400, 460)

# In-tune thresholds (cents)
IN_TUNE_THRESHOLD = 5.0      # Within 5 cents = in tune
CLOSE_THRESHOLD = 50.0       # Within 50 cents = close

# Guitar strings (name, base_freq, note)
GUITAR_STRINGS = [
    ("E (6)", 82.41, "E2"),
    ("A (5)", 110.00, "A2"),
    ("D (4)", 146.83, "D3"),
    ("G (3)", 196.00, "G3"),
    ("B (2)", 246.94, "B3"),
    ("E (1)", 329.63, "E4"),
]

# Audio settings
CHUNK_SIZE = 4096
SAMPLE_RATE = 44100
CHANNELS = 1
DURATION_SECONDS = 0.5  # Duration of each audio chunk in seconds

# Color scheme
COLORS = {
    'bg_dark': '#1e1e1e',
    'bg_medium': '#2d2d2d',
    'bg_light': '#3d3d3d',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'button_primary': '#0066cc',
    'button_secondary': '#004499',
    'status_in_tune': '#00cc00',
    'status_close': '#ffff00',
    'status_off': '#cc0000',
}

# String colors
STRING_COLORS = [
    '#ff6b6b',  # Red
    '#ff8c42',  # Orange
    '#ffd93d',  # Yellow
    '#6bcf7f',  # Green
    '#4d96ff',  # Blue
    '#c77dff',  # Purple
]

DEFAULT_TOLERANCE_HZ = 1.0  # Default tolerance in Hz
