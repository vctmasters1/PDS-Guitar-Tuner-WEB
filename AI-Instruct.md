# Guitar Tuner Web - Comprehensive AI Instructions

## Project Scope
**Pure static web-based** real-time guitar tuner using HTML, CSS, and JavaScript. Uses the Web Audio API for microphone access and autocorrelation-based pitch detection. Provides visual feedback for pitch accuracy across 6 guitar strings. **No server required** - runs entirely in the browser.

---

## Architecture: Modular Static Web App

### Why Static?
- All audio processing happens in JavaScript via Web Audio API
- No backend requirements - browser handles everything
- **Deploy to GitHub Pages** - just serve static files
- Zero dependencies (no npm, no Python, no builds)

### Key Technologies
- **Web Audio API** - Microphone access via `getUserMedia()`
- **Autocorrelation Algorithm** - Pitch detection in JavaScript
- **CSS Flexbox** - Responsive layout
- **Vanilla JavaScript** - No frameworks needed

---

## Project Structure

```
Guitar-Tuner-WEB/
├── index.html              # HTML structure only
├── css/
│   └── styles.css          # All CSS styles
├── js/
│   ├── config.js           # Configuration & constants
│   ├── audio.js            # Web Audio API & pitch detection
│   ├── ui.js               # UI rendering functions
│   └── app.js              # Main initialization
├── README.md               # User-facing documentation
├── LICENSE                 # MIT License
├── AI-Instruct.md          # This file
└── .github/
    └── copilot-instructions.md
```

---

## File Responsibilities

### index.html
- DOCTYPE and meta tags
- Semantic HTML structure
- Links to external CSS (`css/styles.css`)
- Links to external JS (in order: config → audio → ui → app)
- NO inline styles or scripts

### css/styles.css
- All visual styling
- Reset and base styles
- Component styles (header, settings, buttons, gauges, piano)
- Responsive media queries
- CSS custom properties (if needed)

### js/config.js
- Configuration variables (`REFERENCE_FREQ`, `DB_THRESHOLD`)
- `GUITAR_STRINGS` array with semitone offsets
- `PIANO_NOTES` array (generated)
- `calculateFrequencies()` - recalculate based on reference
- `updateReferenceFreq()` - handle dropdown change
- `updateThreshold()` - handle slider change

### js/audio.js
- Web Audio API setup (`audioContext`, `analyser`)
- `startAudio()` - initialize microphone input
- `stopAudio()` - cleanup audio resources
- `detectPitch()` - main detection loop (called every 100ms)
- `autoCorrelate()` - pitch detection algorithm
- `playNote()` - play reference tone via oscillator
- Harmonic filtering logic

### js/ui.js
- `initUI()` - initialize all UI components
- `renderStringRows()` - generate string row HTML
- `renderPianoKeyboard()` - generate piano key HTML
- DOM manipulation functions

### js/app.js
- `initApp()` - application entry point
- DOMContentLoaded event listener
- Calls `calculateFrequencies()` and `initUI()`

---

## Deployment: GitHub Pages

### Setup (One-Time)
1. Push all files to repository
2. Go to repository **Settings** → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **master** (or main), folder: **/ (root)**
5. Save

### URL
After enabling, app is live at:
```
https://<username>.github.io/<repo-name>/
```

### No Build Step Required
- GitHub serves static files directly
- Updates deploy automatically on push
- HTTPS enabled by default

---

## CRITICAL - Frequency Calculation Requirements

### Rule 1: NO HARDCODED FREQUENCIES
**ALL target frequencies must be mathematically calculated.**

```javascript
// ✅ CORRECT - Calculate dynamically (in js/config.js)
const freq = REFERENCE_FREQ * Math.pow(2, semitones / 12);

// ❌ WRONG - Hardcoded value
const freq = 82.41;
```

### Rule 2: Recalculate on Settings Change
When reference frequency changes, recalculate all frequencies:
```javascript
function updateReferenceFreq() {
    REFERENCE_FREQ = parseFloat(document.getElementById('refFreq').value);
    calculateFrequencies();  // Recalculates all string/piano frequencies
    initUI();                // Rebuilds UI with new values
}
```

### Rule 3: Frequency Formula (Equal Temperament 12-TET)
```
frequency = reference_freq × 2^(semitones_from_A4 / 12)
```

Example: A4 = 440 Hz, E2 = 440 × 2^(-29/12) ≈ 82.41 Hz

---

## UI Layout

### Structure
```
┌─────────────────────────────────────────────────┐
│  HEADER - Title & Description                   │
├─────────────────────────────────────────────────┤
│  SETTINGS BAR - Reference freq, Sensitivity     │
├─────────────────────────────────────────────────┤
│                MAIN CONTAINER                   │
│  ┌──────────────────────┬───────────────────┐   │
│  │  LEFT PANEL (2/3)    │  RIGHT PANEL      │   │
│  │                      │                   │   │
│  │  [Start/Stop]        │  Piano Keyboard   │   │
│  │  [Hz/dB Display]     │  (vertical keys)  │   │
│  │                      │                   │   │
│  │  String Row: E2      │  D2 ──────────    │   │
│  │  String Row: A2      │  D#2 ────────     │   │
│  │  String Row: D3      │  E2 ──────────    │   │
│  │  String Row: G3      │  ...              │   │
│  │  String Row: B3      │  (scrollable)     │   │
│  │  String Row: E4      │                   │   │
│  └──────────────────────┴───────────────────┘   │
└─────────────────────────────────────────────────┘
```

### String Rows (rendered by js/ui.js)
Each row contains:
- **String name badge** (colored with tan gradient)
- **Target frequency** (calculated, not hardcoded)
- **Detected frequency** (live from microphone)
- **Gauge** (visual cents deviation indicator with needle)
- **Status** (IN TUNE / CLOSE / FLAT / SHARP)

### Piano Keyboard (rendered by js/ui.js)
- **VERTICAL layout ONLY** (keys stacked top-to-bottom)
- Range: D2 through A4 (~30 notes)
- White keys: light background
- Black keys: dark background, indented
- Guitar string notes: highlighted with color
- Detected note: green border highlight
- Click to play tone (Web Audio oscillator)

---

## Audio Processing (js/audio.js)

### Web Audio API Setup
```javascript
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        audioContext = new AudioContext();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 4096;
        
        microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);
        
        setInterval(detectPitch, 100);  // 10Hz update rate
    });
```

### Pitch Detection: Autocorrelation
```javascript
function autoCorrelate(buffer, sampleRate) {
    // 1. Calculate RMS to check signal level
    // 2. Trim silent ends of buffer
    // 3. Compute autocorrelation coefficients
    // 4. Find peak (fundamental period)
    // 5. Parabolic interpolation for accuracy
    // 6. Return frequency = sampleRate / period
}
```

### Harmonic Filtering
Prevent octave jumps by comparing to previous frequency:
```javascript
if (freqRounded / lastValidFreq > 1.9 && freqRounded / lastValidFreq < 2.1) {
    freqRounded = lastValidFreq;  // Ignore octave jump
}
```

---

## Configuration (js/config.js)

### Guitar Strings
```javascript
const GUITAR_STRINGS = [
    { name: 'E2', displayName: 'E (6)', semitones: -29, color: '#8B7355' },
    { name: 'A2', displayName: 'A (5)', semitones: -24, color: '#9D8164' },
    { name: 'D3', displayName: 'D (4)', semitones: -19, color: '#AF8F73' },
    { name: 'G3', displayName: 'G (3)', semitones: -14, color: '#C19D82' },
    { name: 'B3', displayName: 'B (2)', semitones: -10, color: '#D3AB91' },
    { name: 'E4', displayName: 'E (1)', semitones: -5,  color: '#E5B9A0' }
];
```

### Tuning Reference Options
- 432 Hz
- 440 Hz (Standard - default)
- 442 Hz
- 444 Hz

### Thresholds
- **In-tune**: ±5 cents (green)
- **Close**: ±15 cents (orange)
- **Off**: >15 cents (red)
- **dB threshold**: -40 dB (adjustable via slider)

---

## DO's and DON'Ts

### ✅ DO
- Keep HTML, CSS, JS in separate files
- Calculate frequencies dynamically
- Use Web Audio API for all audio
- Make UI responsive (mobile-friendly)
- Use vanilla JavaScript (no frameworks)
- Test microphone permissions
- Maintain clear file separation

### ❌ DON'T
- Hardcode frequency values
- Add npm/build dependencies
- Require a server to run
- Put inline styles in HTML
- Put inline scripts in HTML
- Change piano to horizontal layout
- Mix concerns between files

---

## Testing Checklist

- [ ] Open `index.html` directly in browser
- [ ] CSS loads correctly (styled UI appears)
- [ ] JS loads without console errors
- [ ] Click "Start Microphone" - permissions work
- [ ] Play a note - frequency detected and displayed
- [ ] Correct string row activates and shows gauge
- [ ] Piano key highlights for detected note
- [ ] Change reference frequency - all values update
- [ ] Adjust sensitivity slider - affects detection
- [ ] Click piano keys - plays tones
- [ ] Works on mobile browsers
- [ ] Works when served via GitHub Pages (HTTPS)

---

## Browser Requirements

- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Full support (iOS 14.5+)
- **HTTPS required** for microphone access (GitHub Pages provides this)
