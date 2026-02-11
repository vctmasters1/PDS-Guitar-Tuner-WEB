# Guitar Tuner Web - Copilot Instructions

## Priority Directives

**ALWAYS read and follow AI-Instruct.md before responding to ANY request in this project.**

This is a **pure static web app** - HTML, CSS, and JavaScript only. No server, no Python, no build tools.

---

## Architecture: Modular Static Web App

### Project Structure
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
├── README.md
├── LICENSE
├── AI-Instruct.md
└── .github/copilot-instructions.md
```

### No Server Required
- Open `index.html` directly in browser
- Deploy to GitHub Pages (just enable in repo settings)
- No npm, no Python, no build step

### Technologies Used
- **HTML5** - Structure (index.html)
- **CSS3** - Styling (css/styles.css)
- **JavaScript** - Logic (js/*.js)
- **Web Audio API** - Microphone & audio processing

---

## Critical Rules

### Rule 1: NO Hardcoded Frequencies
Every frequency MUST be calculated in `js/config.js`:
```javascript
// ✅ CORRECT
const freq = REFERENCE_FREQ * Math.pow(2, semitones / 12);

// ❌ WRONG
const freq = 82.41;
```

### Rule 2: Recalculate on Settings Change
When reference frequency changes (in `js/config.js`):
```javascript
function updateReferenceFreq() {
    REFERENCE_FREQ = parseFloat(document.getElementById('refFreq').value);
    calculateFrequencies();
    initUI();
}
```

### Rule 3: Piano Layout - VERTICAL Only
Piano keyboard must ALWAYS be:
- Vertical arrangement (keys stacked top-to-bottom)
- Styled divs with flexbox
- Scrollable in Y direction
- Range: D2 through A4

**DO NOT change to horizontal layout.**

### Rule 4: File Organization
Keep concerns separated:
- `index.html` - HTML structure only (no inline styles/scripts)
- `css/styles.css` - All styling
- `js/config.js` - Configuration and constants
- `js/audio.js` - Audio processing and pitch detection
- `js/ui.js` - DOM manipulation and rendering
- `js/app.js` - Initialization and entry point

---

## JavaScript Module Responsibilities

### js/config.js
- `REFERENCE_FREQ` - Current reference frequency
- `DB_THRESHOLD` - Sensitivity threshold
- `GUITAR_STRINGS` - String configuration array
- `PIANO_NOTES` - Piano key data
- `calculateFrequencies()` - Recalculate all frequencies
- `updateReferenceFreq()` - Handle reference change
- `updateThreshold()` - Handle sensitivity change

### js/audio.js
- `startAudio()` - Initialize microphone
- `stopAudio()` - Cleanup audio resources
- `detectPitch()` - Main detection loop
- `autoCorrelate()` - Pitch detection algorithm
- `playNote()` - Play reference tone

### js/ui.js
- `initUI()` - Initialize all UI components
- `renderStringRows()` - Build string row HTML
- `renderPianoKeyboard()` - Build piano keyboard HTML

### js/app.js
- `initApp()` - Application entry point
- DOMContentLoaded listener

---

## Frequency Formula (Equal Temperament)

```
frequency = reference_freq × 2^(semitones_from_A4 / 12)
```

Guitar string semitones from A4:
- E2: -29 semitones
- A2: -24 semitones
- D3: -19 semitones
- G3: -14 semitones
- B3: -10 semitones
- E4: -5 semitones

---

## Deployment: GitHub Pages

1. Push all files to repository
2. Go to Settings → Pages
3. Source: Deploy from branch
4. Branch: master, folder: / (root)
5. App is live at `https://<user>.github.io/<repo>/`

No build step. No configuration files. Just static files.

---

## When Fixing Bugs

### Audio not working
1. Check browser console for errors
2. Verify HTTPS (required for microphone)
3. Check `getUserMedia` permissions in `js/audio.js`
4. Verify analyser is connected

### Frequencies wrong after settings change
1. Check `calculateFrequencies()` in `js/config.js`
2. Verify `initUI()` is called in `js/ui.js`
3. Confirm REFERENCE_FREQ variable is updated

### Gauges not moving
1. Check `detectPitch()` in `js/audio.js`
2. Verify closest string detection logic
3. Check cents calculation formula

---

## Testing Checklist

- [ ] `index.html` opens directly in browser
- [ ] All CSS loads from `css/styles.css`
- [ ] All JS files load in correct order
- [ ] Microphone permission prompt appears
- [ ] Frequency detection works (Hz updates)
- [ ] dB level displays
- [ ] String gauges activate when playing notes
- [ ] Piano keys highlight for detected notes
- [ ] Piano keys play tones when clicked
- [ ] Reference frequency change updates all values
- [ ] Works on GitHub Pages (HTTPS)

---

## DO's and DON'Ts

### ✅ DO
- Keep HTML, CSS, and JS in separate files
- Use vanilla JavaScript
- Calculate frequencies dynamically
- Test microphone in browser
- Use Web Audio API patterns
- Maintain modular file structure

### ❌ DON'T
- Hardcode frequency values
- Add npm/yarn dependencies
- Require a build step
- Put inline styles in HTML
- Put inline scripts in HTML
- Change piano to horizontal layout
