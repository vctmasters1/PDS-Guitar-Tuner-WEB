# Guitar Tuner Web - Copilot Instructions

## Priority Directives

**ALWAYS read and follow AI-Instruct.md before responding to ANY request in this project.**

The root-level [AI-Instruct.md](../AI-Instruct.md) contains:
- ✅ Complete project scope and structure
- ✅ CRITICAL frequency calculation rules (NO hardcoding)
- ✅ UI layout requirements (two-column, VERTICAL piano ONLY)
- ✅ Configuration patterns
- ✅ Code quality standards
- ✅ Piano keyboard specifications
- ✅ DO's and DON'Ts list

**Reference AI-Instruct.md for every code change.**

---

## Project Structure

```
Guitar-Tuner-WEB/
├── app.py                          # Main entry point (ONLY app file)
├── requirements.txt
├── AI-Instruct.md                 # ROOT INSTRUCTIONS (read first!)
├── .github/copilot-instructions.md # This file
├── .dev.md/                        # Development notes
├── src/
│   ├── core/
│   │   ├── config.py              # Constants only
│   │   ├── tuner.py               # Frequency formulas
│   │   └── __init__.py
│   ├── audio/
│   │   ├── capture.py             # FFT & audio detection
│   │   └── __init__.py
│   └── __init__.py
└── .venv/                          # Virtual environment
```

---

## Critical Piano Layout Rules - NON-NEGOTIABLE

### ❌ WRONG (Don't do these)
- Horizontal piano keyboard (side-by-side keys)
- Keys as plain text divs
- Scrollable horizontally instead of vertically
- SVG with complex positioning logic

### ✅ CORRECT (Do this)
- **Vertical stacking ONLY**: Keys arranged top to bottom
- **Visual styling**: Each key is a styled HTML div
- **Scrollable vertically**: max-height 600px, overflow-y auto
- **Simple flex layout**: Each key is flexbox (Note Name | Frequency)
- **30+ keys**: D2 through A4
- **White keys** (#f5f5f5, 60px height), **Black keys** (#1a1a1a, 50px height)

---

## Critical Rules - DO NOT VIOLATE

### Rule 1: NO Hardcoded Frequencies
Every target frequency MUST be calculated:
```python
# ✅ CORRECT
target_freq = st.session_state.tuner.calculate_frequency(note_name, octave_offset)

# ❌ WRONG
target_freq = 82.41  # Hardcoded value
```

### Rule 2: Tuner Recreation on Settings Change
When user changes reference frequency or temperament:
```python
st.session_state.tuner = GuitarTuner(
    st.session_state.reference_freq,
    st.session_state.temperament
)
```

### Rule 3: Piano Layout - VERTICAL Only, NEVER Change
Piano keyboard must ALWAYS be:
- Vertical arrangement (keys stacked vertically)
- Styled divs (not plain text)
- Scrollable in Y direction (not X)
- Displaying all 30+ notes from D2 to A4

**This has been changed before. Do NOT change it again.**

### Rule 4: Use Callbacks for Reactivity
Add `on_change` callbacks to settings widgets:
```python
st.selectbox(..., on_change=callback_function)
st.radio(..., on_change=callback_function)
st.slider(..., on_change=callback_function)
```

### Rule 5: Two-Column Layout (Non-negotiable)
- Left column (2/3): String rows with target/detected frequencies
- Right column (1/3): Piano keyboard
- Use `st.columns([2, 1])` for layout

---

## Frequency Calculation Formulas

### Equal Temperament (12-TET)
```
frequency = reference_freq × 2^(semitones_from_A4 / 12)
```

### Just Intonation
```
frequency = (reference_freq / 5/3) × harmonic_ratio × 2^(octave_offset)
```

**Both formulas implemented in `src/core/tuner.py`**

---

## Session State Pattern

```python
def initialize_session_state():
    if "tuner" not in st.session_state:
        st.session_state.tuner = GuitarTuner(
            DEFAULT_REFERENCE_FREQ, 
            DEFAULT_TEMPERAMENT
        )
    if "reference_freq" not in st.session_state:
        st.session_state.reference_freq = DEFAULT_REFERENCE_FREQ
    if "temperament" not in st.session_state:
        st.session_state.temperament = DEFAULT_TEMPERAMENT
    # ... other state vars

initialize_session_state()
```

---

## Config File Rules

**src/core/config.py must contain ONLY:**
- Constants (no functions)
- Tuning data (presets, guitar strings)
- Color definitions (tan gradient STRING_COLORS)
- Thresholds and magic numbers
- Temperament names (short strings: "equal", "just")

**Example:**
```python
TEMPERAMENT_EQUAL = "equal"
GUITAR_STRINGS = [
    ('E (6)', 'E', -2),
    ('A (5)', 'A', -2),
    # ...
]
```

---

## When Fixing Bugs

### Target frequencies not updating
1. ✅ Check tuner is recreated after settings change
2. ✅ Add `on_change` callbacks to sidebar widgets
3. ✅ Verify `render_string_rows()` uses `st.session_state.tuner`
4. ✅ Use `st.rerun()` if needed for force recalculation

### Piano keyboard issues
1. ✅ MUST be VERTICAL (stacked vertically, NOT horizontal)
2. ✅ Each key must be a styled HTML div (NOT text)
3. ✅ Use simple flexbox layout for each key
4. ✅ Max-height: 600px, overflow-y: auto for scrolling
5. ✅ Display note name, octave, and frequency on each key
6. ✅ White keys: light bg, Black keys: dark bg

### Audio detection not working
1. ✅ Check `AudioCapture` in `src/audio/capture.py`
2. ✅ Verify FFT parameters (sample rate, chunk size)
3. ✅ Ensure `st.session_state.detected_frequency` is updated
4. ✅ Test mic permissions in browser

---

## Testing Checklist

- [ ] Change tuning preset → target frequencies update instantly
- [ ] Change temperament → different frequency values appear
- [ ] Piano keyboard is VERTICAL (NOT horizontal)
- [ ] Each piano key is a styled element (NOT text)
- [ ] Guitar string notes are colored with tan gradient
- [ ] Detected note highlighted with accent border
- [ ] Info button opens fullscreen modal
- [ ] Microphone captures audio and updates detected frequency
- [ ] Two-column layout displays correctly
- [ ] Piano scrolls vertically (max 600px height)

---

## Development Workflow

1. **Read AI-Instruct.md** - Always start here
2. **Check .dev.md/** - Review architecture decisions
3. **Run app**: `streamlit run app.py`
4. **Test items** - Verify against checklist above
5. **Update AI-Instruct.md** - If adding new patterns
6. **Commit** - Keep history clean

---

## Key Files and Their Purpose

| File | Purpose | Modify When |
|------|---------|-------------|
| `app.py` | Main orchestration | UI changes, rendering |
| `src/core/config.py` | Constants only | Adding presets, colors, strings |
| `src/core/tuner.py` | Frequency formulas | Bug in calculations, new temperament |
| `src/audio/capture.py` | FFT analysis | Audio detection issues |
| `AI-Instruct.md` | Master guidelines | Any pattern change |
| `.dev.md/` | Architecture notes | Major decisions |

---

## Common Mistakes to Avoid

❌ Hardcoding frequencies (82.41 Hz, etc.)
❌ Using `st.info()` instead of `@st.dialog()` for modals
❌ **Changing piano to horizontal layout** ← MOST COMMON MISTAKE
❌ Rendering piano as plain text
❌ Removing or consolidating instruction files
❌ Not recreating tuner after settings change
❌ Forgetting `on_change` callbacks on widgets
❌ Caching frequencies instead of recalculating
❌ Using state callbacks instead of widget on_change
❌ **Modifying files in .old/ directory** ← DO NOT EDIT, ARCHIVE ONLY

---

## Questions? Review AI-Instruct.md First

Almost all guidance is in [AI-Instruct.md](../AI-Instruct.md). Check there first before making changes.

Always check this directory for:
- Architecture decisions
- Development notes
- Feature planning
- Technical debt tracking
