# Guitar Tuner Web - Comprehensive AI Instructions

## Project Scope
Web-based real-time guitar tuner using Streamlit, FFT audio analysis, and mathematical frequency calculations. Provides visual feedback for pitch accuracy across 6 guitar strings with support for multiple tuning references and temperament systems.

---

## Project Structure

### Root Directory Files (Documentation & Config)
- `app.py` - Main Streamlit application entry point (ONLY app file in root)
- `requirements.txt` - Python dependencies
- `README.md` - User-facing overview
- `QUICKSTART.md` - Quick setup guide
- `CONTRIBUTING.md` - Contribution guidelines
- `Procfile` - Deployment configuration
- `LICENSE` - MIT License
- Documentation files (.md only, no backups)

### Source Code Organization (`src/`)
```
src/
├── core/
│   ├── config.py      # Constants, colors, tuning data
│   ├── tuner.py       # Musical frequency calculations
│   └── __init__.py
├── audio/
│   ├── capture.py     # Audio input & FFT analysis
│   └── __init__.py
└── __init__.py
```

### Development & Reference
- `UPSTREAM-RESEARCH/` - Reference PC implementation (tkinter version)
- `.dev.md/` - Development notes directory
- `.github/` - CI/CD and issue templates
- `.streamlit/` - Streamlit configuration
- `.venv/` - Python virtual environment

---

## CRITICAL - Frequency Calculation Requirements

### Rule 1: NO HARDCODED FREQUENCIES
**ALL target frequencies must be mathematically calculated, NEVER hardcoded.**

When render_string_rows() executes:
```python
target_freq = st.session_state.tuner.calculate_frequency(note_name, octave_offset)
```

This MUST call the tuner's formula-based calculation, not a lookup table.

### Rule 2: Tuner Object Lifecycle
The tuner object MUST be recreated when settings change:
```python
# When reference_freq or temperament changes:
st.session_state.tuner = GuitarTuner(
    st.session_state.reference_freq, 
    st.session_state.temperament
)
```

### Rule 3: Frequency Calculation Formulas
**Equal Temperament (12-TET):**
```
frequency = reference_freq * 2^(semitones_from_A4 / 12)
```

**Just Intonation:**
```
frequency = (reference_freq / 5/3) * harmonic_ratio * 2^(octave_offset)
```

Example: A4 = 440 Hz, E4 = 440 * 2^(-5/12) ≈ 329.63 Hz

---

## UI Layout - NON-NEGOTIABLE

### Two-Column Layout (REQUIRED)
```
┌─────────────────────────────────────────────────┐
│  ⚙️ SIDEBAR                                     │
│  - Tuning Reference (dropdown)                  │
│  - Temperament (radio)                          │
│  - Tolerance (slider)                           │
└─────────────────────────────────────────────────┘
┌────────────────────────────┬────────────────────┐
│  LEFT COLUMN (2/3)         │  RIGHT (1/3)       │
│  🎸 String Rows            │  ⌨️ Piano          │
│                            │                     │
│  [E (6) Tan Row]           │  D2 ┌──────┐       │
│  Target: 82.41 Hz          │      │      │       │
│  Detected: 82.45 Hz        │  D#2 │      │       │
│  Deviation: +0.5¢ ✓        │      │      │       │
│                            │  E2 ┌┴──────┴┐      │
│  [A (5) Tan Row]           │      │ 82.41  │      │
│  Target: 110.00 Hz         │      │ Hz     │      │
│  Detected: -- Hz           │      └────────┘      │
│  Status: IDLE              │                     │
│                            │  (scrollable)       │
│  ... (4 more strings)      │                     │
└────────────────────────────┴────────────────────┘
```

### Left Column: String Rows
- **6 rows** (one per string)
- **Layout per row**: String Name | Target Freq | Detected Freq | Status
- **Colors**: Tan gradient (STRING_COLORS)
- **Target Freq**: Recalculated on every render (NOT cached)
- **Status**: Color-coded based on cents deviation

### Right Column: Piano Keyboard
- **VERTICAL layout ONLY** (keys stacked top-to-bottom, NOT horizontal)
- **Visual styling** (NOT plain text) - Each key is a styled div element
- **Range**: D2 (27.5 Hz) through A4 (440 Hz) = 30+ notes
- **Each key displays**: Note name + octave, Frequency (Hz)
- **Container**: Scrollable with max-height 600px (overflow-y auto)
- **White keys**: Light background (#f5f5f5), dark text, 60px height
- **Black keys**: Dark background (#1a1a1a), white text, 50px height
- **Highlighting**:
  - Guitar string notes: Colored with STRING_COLORS (tan gradient)
  - Detected note: 4px left border in accent color
- **DO NOT** change to horizontal layout under any circumstances

---

## Configuration Management

### config.py Format
```python
# Temperament constants - SHORT NAMES ONLY
TEMPERAMENT_EQUAL = "equal"
TEMPERAMENT_JUST = "just"

# Guitar strings - (display_name, note_name, octave_offset)
GUITAR_STRINGS = [
    ('E (6)', 'E', -2),   # E2
    ('A (5)', 'A', -2),   # A2
    ('D (4)', 'D', -1),   # D3
    ('G (3)', 'G', -1),   # G3
    ('B (2)', 'B', -1),   # B3
    ('E (1)', 'E', 0),    # E4
]

# Tuning frequencies (Hz)
TUNING_PRESETS = [
    ("432 Hz", 432.0),
    ("440 Hz (A4)", 440.0),
    ("442 Hz", 442.0),
    ("444 Hz", 444.0),
]

# Colors - ALWAYS TAN GRADIENT
STRING_COLORS = [
    '#8B7355',  # Dark tan
    '#9D8164',  # Medium-dark tan
    '#AF8F73',  # Medium tan
    '#C19D82',  # Medium-light tan
    '#D3AB91',  # Light tan
    '#E5B9A0',  # Very light tan
]

# Thresholds
IN_TUNE_THRESHOLD = 5.0      # ±5 cents
CLOSE_THRESHOLD = 50.0       # ±50 cents
```

---

## Streamlit State Management

### Session State Initialization
```python
def initialize_session_state():
    STATE_VARS = {
        "reference_freq": DEFAULT_REFERENCE_FREQ,
        "temperament": DEFAULT_TEMPERAMENT,
        "tolerance_hz": DEFAULT_TOLERANCE_HZ,
        "detected_frequency": None,
        "current_string_idx": None,
        "cents_deviation": 0,
        "tuner": GuitarTuner(DEFAULT_REFERENCE_FREQ, DEFAULT_TEMPERAMENT),
        "audio_capture": AudioCapture(),
    }
    for key, value in STATE_VARS.items():
        if key not in st.session_state:
            st.session_state[key] = value
```

### Settings Updates
```python
# In sidebar:
st.session_state.reference_freq = preset_freq
st.session_state.temperament = temperament

# Then recreate tuner for new state:
st.session_state.tuner = GuitarTuner(
    st.session_state.reference_freq,
    st.session_state.temperament
)
```

---

## Root Directory Cleanup Rules

### KEEP in Root
- `app.py` - Single entry point
- `requirements.txt` - Dependencies
- `README.md`, `QUICKSTART.md`, `CONTRIBUTING.md` - Documentation
- `Procfile`, `LICENSE` - Deployment & legal
- `Guitar-Tuner-WEB.code-workspace` - VS Code workspace
- Hidden directories: `.github/`, `.streamlit/`, `.venv/`, `.git/`

### REMOVE from Root
- `app_old.py`, `app_backup.py` etc. - Use git for version control
- `*.bat`, `*.ps1` scripts - Move to `.dev.md/` if needed
- Old notebooks or test files
- Non-essential README files

---

## Code Style & Quality

### Python Standards
- **PEP 8**: 79 char lines, proper spacing
- **Docstrings**: All functions and classes required
- **Type hints**: Where practical for clarity
- **No magic numbers**: Use config.py constants

### Function Pattern
```python
def meaningful_function_name(required_param):
    """
    One-line description.
    
    Args:
        required_param: Description
        
    Returns:
        Description of return value
    """
    # Implementation
    return result
```

---

## Testing Before Commit

### Functional Testing
- [ ] Change tuning preset → target frequencies update
- [ ] Change temperament → target frequencies update (different values)
- [ ] Play a note → appears on piano keyboard
- [ ] Mic detection works → updates detected frequency
- [ ] Cents deviation correct → ±5 = green, ±50 = yellow, >50 = red

### Visual Testing
- [ ] Two-column layout displays correctly
- [ ] Piano keyboard is NOT just text (has styling/colors)
- [ ] String rows use tan gradient colors
- [ ] Guitar string notes highlighted on piano
- [ ] Responsive on mobile (tablet-like dimensions)

### Run Locally
```bash
streamlit run app.py
```

---

## When Modifying Code

### Adding Features
1. Update `src/core/config.py` if new constants
2. Implement logic in appropriate `src/*/` module
3. Call from `app.py` (orchestrator only)
4. Update this AI-Instruct.md if pattern changes

### Fixing Frequency Issues
1. Verify `calculate_frequency()` formula in tuner.py
2. Check tuner is recreated after state changes
3. Ensure `render_string_rows()` calls `st.session_state.tuner` (current instance)
4. Use `st.write(f"Debug: {calculated_value}")` for testing

### UI Improvements
1. Keep two-column layout
2. Update CSS in markdown style blocks
3. Maintain tan STRING_COLORS consistency
4. Test on various screen sizes
