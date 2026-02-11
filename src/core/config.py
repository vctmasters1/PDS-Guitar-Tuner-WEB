"""Configuration for Guitar Tuner"""

# Tuning constants
TEMPERAMENT_EQUAL = "equal"
TEMPERAMENT_JUST = "just"
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

# Guitar strings - Format: (display_name, note_name, octave_offset)
# Octave offset: -2 = two octaves below A4, -1 = one octave below, 0 = same octave as A4
GUITAR_STRINGS = [
    ('E (6)', 'E', -2),   # E2 - Low E
    ('A (5)', 'A', -2),   # A2
    ('D (4)', 'D', -1),   # D3
    ('G (3)', 'G', -1),   # G3
    ('B (2)', 'B', -1),   # B3
    ('E (1)', 'E', 0)     # E4 - High E
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
    'bg_light': '#444444',
    'text_primary': '#ffffff',
    'text_secondary': '#888888',
    'accent_gold': '#FFD700',
    'accent_cyan': '#00BFFF',
    'status_in_tune': '#00FF00',
    'status_close': '#FFD700',
    'status_off': '#FF4444',
    'status_inactive': '#555555',
    'button_primary': '#4CAF50',
    'button_secondary': '#2196F3',
    'button_stop': '#f44336',
    'button_temperament': '#9C27B0'
}

# String colors (tan gradient from dark to light)
STRING_COLORS = [
    '#8B7355',  # Low E - Dark tan
    '#9D8164',  # A - Medium-dark tan
    '#AF8F73',  # D - Medium tan
    '#C19D82',  # G - Medium-light tan
    '#D3AB91',  # B - Light tan
    '#E5B9A0'   # High E - Very light tan
]

DEFAULT_TOLERANCE_HZ = 0.2  # Default tolerance in Hz
