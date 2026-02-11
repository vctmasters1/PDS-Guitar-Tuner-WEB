"""
🎸 Guitar Tuner - Web Application

A real-time guitar tuner using frequency detection and visual feedback.
JavaScript-based audio processing with Streamlit wrapper.
"""

import sys
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui import render_page_config, render_header, render_sidebar
from src.state import initialize_session_state
from src.core.config import DEFAULT_REFERENCE_FREQ, DEFAULT_TEMPERAMENT


def get_full_tuner_html(reference_freq=440.0):
    """Return complete HTML/JS for the guitar tuner with string gauges and piano."""
    return f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1e1e1e; color: #fff; }}

.tuner-container {{ display: flex; gap: 20px; padding: 10px; }}
.left-panel {{ flex: 2; }}
.right-panel {{ flex: 1; }}

/* Control buttons */
.controls {{ display: flex; gap: 10px; align-items: center; margin-bottom: 15px; flex-wrap: wrap; }}
.btn {{ padding: 12px 24px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer; }}
.btn-start {{ background: #4CAF50; color: white; }}
.btn-stop {{ background: #f44336; color: white; }}
.btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
.status {{ color: #888; margin-left: 10px; }}

/* Main frequency display */
.main-display {{ 
    background: #2d2d2d; 
    padding: 20px; 
    border-radius: 8px; 
    text-align: center; 
    margin-bottom: 20px;
}}
.freq-line {{ 
    font-size: 36px; 
    font-weight: bold; 
    color: #32a852; 
    font-family: 'Courier New', monospace; 
}}
.freq-val, .db-val {{ display: inline-block; text-align: right; }}
.freq-val {{ width: 140px; }}
.db-val {{ width: 70px; }}

/* String rows */
.string-row {{ 
    display: flex; 
    align-items: center; 
    gap: 10px; 
    padding: 10px; 
    background: #2d2d2d; 
    border-radius: 8px; 
    margin-bottom: 8px;
    opacity: 0.4;
    transition: opacity 0.2s;
}}
.string-row.active {{ opacity: 1; }}
.string-name {{ 
    width: 60px; 
    height: 60px; 
    border-radius: 5px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    font-weight: bold; 
    font-size: 18px; 
    color: white;
}}
.string-info {{ flex: 1; min-width: 100px; }}
.string-target {{ color: #888; font-size: 12px; }}
.string-freq {{ font-size: 16px; font-weight: bold; }}

/* Gauge */
.gauge-container {{ flex: 2; min-width: 200px; }}
.gauge-labels {{ display: flex; justify-content: space-between; color: #666; font-size: 10px; margin-bottom: 3px; }}
.gauge-bar {{ 
    position: relative; 
    height: 24px; 
    background: linear-gradient(to right, #f44336 0%, #f44336 35%, #4CAF50 45%, #4CAF50 55%, #ff9800 65%, #ff9800 100%); 
    border-radius: 4px;
}}
.gauge-center {{ position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: white; transform: translateX(-50%); }}
.gauge-needle {{ 
    position: absolute; 
    left: 50%; 
    top: -3px; 
    bottom: -3px; 
    width: 4px; 
    background: #888; 
    border-radius: 2px; 
    transform: translateX(-50%); 
    transition: left 0.1s ease-out;
    box-shadow: 0 0 4px rgba(0,0,0,0.5);
}}
.cents-display {{ text-align: center; font-size: 14px; color: #888; margin-top: 3px; font-family: 'Courier New', monospace; }}

.string-status {{ 
    width: 80px; 
    text-align: center; 
    font-size: 12px; 
    font-weight: bold; 
    padding: 8px; 
    border-radius: 4px;
}}
.status-idle {{ background: #33333355; color: #666; }}
.status-intune {{ background: #4CAF5033; color: #4CAF50; }}
.status-close {{ background: #ff980033; color: #ff9800; }}
.status-off {{ background: #f4433633; color: #f44336; }}

/* Piano */
.piano-title {{ font-size: 16px; margin-bottom: 10px; color: #888; }}
.piano-container {{ 
    max-height: 500px; 
    overflow-y: auto; 
    background: #2d2d2d; 
    border-radius: 8px; 
    padding: 5px;
}}
.piano-key {{ 
    display: flex; 
    align-items: center; 
    justify-content: space-between;
    padding: 8px 12px; 
    margin: 2px 0; 
    border-radius: 4px; 
    cursor: pointer; 
    transition: opacity 0.1s;
    font-size: 12px;
}}
.piano-key:hover {{ opacity: 0.8; }}
.piano-key.white {{ background: #f5f5f5; color: #000; }}
.piano-key.black {{ background: #1a1a1a; color: #fff; margin-left: 40px; width: calc(100% - 40px); }}
.piano-key.guitar-string {{ border-left: 4px solid; }}
.piano-key.detected {{ box-shadow: 0 0 0 2px #4CAF50; }}
.key-note {{ font-weight: bold; }}
.key-freq {{ opacity: 0.7; }}
</style>
</head>
<body>

<div class="tuner-container">
    <div class="left-panel">
        <!-- Controls -->
        <div class="controls">
            <button id="startBtn" class="btn btn-start" onclick="startAudio()">🎤 Start Microphone</button>
            <button id="stopBtn" class="btn btn-stop" onclick="stopAudio()" disabled>⏹ Stop</button>
            <span id="status" class="status">Click Start to begin</span>
        </div>
        
        <!-- Main Display -->
        <div class="main-display">
            <div class="freq-line">
                <span id="hz-val" class="freq-val">----.--</span> Hz | 
                <span id="db-val" class="db-val">---.-</span> dB
            </div>
        </div>
        
        <!-- String Rows -->
        <div id="string-rows"></div>
    </div>
    
    <div class="right-panel">
        <div class="piano-title">⌨️ Piano Keyboard</div>
        <div id="piano-container" class="piano-container"></div>
    </div>
</div>

<script>
// Configuration
const REFERENCE_FREQ = {reference_freq};
const DB_THRESHOLD = -40;

// Guitar strings with calculated frequencies
const GUITAR_STRINGS = [
    {{ name: 'E2', displayName: 'E (6)', semitones: -29, color: '#8B7355' }},
    {{ name: 'A2', displayName: 'A (5)', semitones: -24, color: '#9D8164' }},
    {{ name: 'D3', displayName: 'D (4)', semitones: -19, color: '#AF8F73' }},
    {{ name: 'G3', displayName: 'G (3)', semitones: -14, color: '#C19D82' }},
    {{ name: 'B3', displayName: 'B (2)', semitones: -10, color: '#D3AB91' }},
    {{ name: 'E4', displayName: 'E (1)', semitones: -5, color: '#E5B9A0' }}
];

// Calculate frequencies
GUITAR_STRINGS.forEach(s => {{
    s.freq = REFERENCE_FREQ * Math.pow(2, s.semitones / 12);
}});

// Piano notes D2 to A4
const PIANO_NOTES = [];
const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
for (let octave = 2; octave <= 4; octave++) {{
    for (let i = 0; i < 12; i++) {{
        const note = noteNames[i];
        const noteName = note + octave;
        // Calculate semitones from A4
        const semitonesFromA4 = (octave - 4) * 12 + (i - 9);
        const freq = REFERENCE_FREQ * Math.pow(2, semitonesFromA4 / 12);
        // Filter D2 to A4
        if ((octave === 2 && i >= 2) || (octave === 3) || (octave === 4 && i <= 9)) {{
            PIANO_NOTES.push({{
                name: noteName,
                note: note,
                octave: octave,
                freq: freq,
                isBlack: note.includes('#')
            }});
        }}
    }}
}}

// Audio variables
let audioContext = null;
let analyser = null;
let microphone = null;
let mediaStream = null;
let intervalId = null;
let lastValidFreq = null;
let playbackContext = null;

// Initialize UI
function initUI() {{
    // Create string rows
    const container = document.getElementById('string-rows');
    GUITAR_STRINGS.forEach((s, idx) => {{
        container.innerHTML += `
            <div id="string-${{idx}}" class="string-row">
                <div class="string-name" style="background: ${{s.color}};">${{s.displayName}}</div>
                <div class="string-info">
                    <div class="string-target">Target: ${{s.freq.toFixed(2)}} Hz</div>
                    <div class="string-freq" id="string-freq-${{idx}}">-- Hz</div>
                </div>
                <div class="gauge-container">
                    <div class="gauge-labels"><span>♭ FLAT</span><span>✓</span><span>♯ SHARP</span></div>
                    <div class="gauge-bar">
                        <div class="gauge-center"></div>
                        <div id="needle-${{idx}}" class="gauge-needle"></div>
                    </div>
                    <div id="cents-${{idx}}" class="cents-display">-- cents</div>
                </div>
                <div id="status-${{idx}}" class="string-status status-idle">IDLE</div>
            </div>
        `;
    }});
    
    // Create piano
    const pianoContainer = document.getElementById('piano-container');
    PIANO_NOTES.forEach((p, idx) => {{
        const isGuitarString = GUITAR_STRINGS.find(s => Math.abs(s.freq - p.freq) < 1);
        const guitarColor = isGuitarString ? isGuitarString.color : null;
        const keyClass = p.isBlack ? 'black' : 'white';
        const guitarClass = isGuitarString ? 'guitar-string' : '';
        const style = isGuitarString ? `border-left-color: ${{guitarColor}}; background: ${{guitarColor}};` : '';
        
        pianoContainer.innerHTML += `
            <div id="piano-${{idx}}" class="piano-key ${{keyClass}} ${{guitarClass}}" style="${{style}}" onclick="playNote(${{p.freq}})">
                <span class="key-note">${{p.name}}</span>
                <span class="key-freq">${{p.freq.toFixed(1)}} Hz</span>
            </div>
        `;
    }});
}}

// Audio functions
function startAudio() {{
    navigator.mediaDevices.getUserMedia({{ audio: true, video: false }})
        .then(function(stream) {{
            mediaStream = stream;
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 4096;
            analyser.smoothingTimeConstant = 0.85;
            
            microphone = audioContext.createMediaStreamSource(stream);
            microphone.connect(analyser);
            
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            document.getElementById('status').innerText = '🎤 Listening...';
            document.getElementById('status').style.color = '#32a852';
            
            intervalId = setInterval(detectPitch, 100);
        }})
        .catch(function(err) {{
            document.getElementById('status').innerText = 'Error: ' + err.message;
            document.getElementById('status').style.color = '#f44336';
        }});
}}

function stopAudio() {{
    if (intervalId) {{ clearInterval(intervalId); intervalId = null; }}
    if (mediaStream) {{ mediaStream.getTracks().forEach(track => track.stop()); mediaStream = null; }}
    if (audioContext) {{ audioContext.close(); audioContext = null; }}
    lastValidFreq = null;
    
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('status').innerText = 'Stopped';
    document.getElementById('status').style.color = '#888';
    document.getElementById('hz-val').innerText = '----.--';
    document.getElementById('db-val').innerText = '---.-';
    
    // Reset all strings
    GUITAR_STRINGS.forEach((s, idx) => {{
        document.getElementById('string-' + idx).classList.remove('active');
        document.getElementById('string-freq-' + idx).innerText = '-- Hz';
        document.getElementById('needle-' + idx).style.left = '50%';
        document.getElementById('needle-' + idx).style.background = '#888';
        document.getElementById('cents-' + idx).innerText = '-- cents';
        document.getElementById('status-' + idx).className = 'string-status status-idle';
        document.getElementById('status-' + idx).innerText = 'IDLE';
    }});
    
    // Reset piano highlighting
    PIANO_NOTES.forEach((p, idx) => {{
        document.getElementById('piano-' + idx).classList.remove('detected');
    }});
}}

function formatHz(freq) {{
    if (freq <= 0) return '----.--';
    return freq.toFixed(2).padStart(7, ' ');
}}

function formatDb(db) {{
    if (db <= -100) return '---.-';
    return db.toFixed(1).padStart(5, ' ');
}}

function detectPitch() {{
    if (!analyser) return;
    
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Float32Array(bufferLength);
    analyser.getFloatTimeDomainData(dataArray);
    
    // Calculate RMS for dB
    let sum = 0;
    for (let i = 0; i < dataArray.length; i++) {{
        sum += dataArray[i] * dataArray[i];
    }}
    const rms = Math.sqrt(sum / dataArray.length);
    const db = rms > 0 ? 20 * Math.log10(rms) : -100;
    
    document.getElementById('db-val').innerText = formatDb(db);
    
    // Reset all strings first
    GUITAR_STRINGS.forEach((s, idx) => {{
        document.getElementById('string-' + idx).classList.remove('active');
    }});
    PIANO_NOTES.forEach((p, idx) => {{
        document.getElementById('piano-' + idx).classList.remove('detected');
    }});
    
    if (db < DB_THRESHOLD) {{
        document.getElementById('hz-val').innerText = '----.--';
        lastValidFreq = null;
        return;
    }}
    
    const sampleRate = audioContext.sampleRate;
    let frequency = autoCorrelate(dataArray, sampleRate);
    let freqRounded = frequency > 0 ? Math.round(frequency * 100) / 100 : -1;
    
    // Harmonic filtering
    if (freqRounded > 0 && lastValidFreq !== null) {{
        const ratio = freqRounded / lastValidFreq;
        if (ratio > 1.9 && ratio < 2.1) {{
            freqRounded = lastValidFreq;
        }} else if (ratio > 0.48 && ratio < 0.52 && db < -20) {{
            freqRounded = lastValidFreq;
        }}
    }}
    
    if (freqRounded > 0) lastValidFreq = freqRounded;
    
    document.getElementById('hz-val').innerText = formatHz(freqRounded);
    
    if (freqRounded <= 0) return;
    
    // Find closest guitar string
    let closestIdx = -1;
    let minDist = Infinity;
    GUITAR_STRINGS.forEach((s, idx) => {{
        const dist = Math.abs(freqRounded - s.freq);
        if (dist < minDist) {{
            minDist = dist;
            closestIdx = idx;
        }}
    }});
    
    // Only activate if within 30Hz of a string
    if (closestIdx >= 0 && minDist < 30) {{
        const s = GUITAR_STRINGS[closestIdx];
        const cents = 1200 * Math.log2(freqRounded / s.freq);
        const centsRounded = Math.round(cents * 10) / 10;
        
        // Activate this string row
        document.getElementById('string-' + closestIdx).classList.add('active');
        document.getElementById('string-freq-' + closestIdx).innerText = freqRounded.toFixed(2) + ' Hz';
        
        // Update needle
        const clampedCents = Math.max(-50, Math.min(50, centsRounded));
        const needlePos = 50 + clampedCents;
        const needle = document.getElementById('needle-' + closestIdx);
        needle.style.left = needlePos + '%';
        
        // Cents display
        const centsText = (centsRounded >= 0 ? '+' : '') + centsRounded.toFixed(1);
        document.getElementById('cents-' + closestIdx).innerText = centsText + ' cents';
        
        // Status and needle color
        const statusEl = document.getElementById('status-' + closestIdx);
        if (Math.abs(centsRounded) <= 5) {{
            needle.style.background = '#4CAF50';
            statusEl.className = 'string-status status-intune';
            statusEl.innerText = '✓ IN TUNE';
        }} else if (Math.abs(centsRounded) <= 15) {{
            needle.style.background = '#ff9800';
            statusEl.className = 'string-status status-close';
            statusEl.innerText = '~ CLOSE';
        }} else {{
            needle.style.background = '#f44336';
            statusEl.className = 'string-status status-off';
            statusEl.innerText = centsRounded < 0 ? '♭ FLAT' : '♯ SHARP';
        }}
    }}
    
    // Highlight closest piano key
    let closestPianoIdx = -1;
    let minPianoDist = Infinity;
    PIANO_NOTES.forEach((p, idx) => {{
        const dist = Math.abs(freqRounded - p.freq);
        if (dist < minPianoDist) {{
            minPianoDist = dist;
            closestPianoIdx = idx;
        }}
    }});
    if (closestPianoIdx >= 0 && minPianoDist < 20) {{
        document.getElementById('piano-' + closestPianoIdx).classList.add('detected');
    }}
}}

function playNote(frequency) {{
    if (!playbackContext) {{
        playbackContext = new (window.AudioContext || window.webkitAudioContext)();
    }}
    
    const now = playbackContext.currentTime;
    const oscillator = playbackContext.createOscillator();
    const gainNode = playbackContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(playbackContext.destination);
    
    oscillator.frequency.value = frequency;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, now);
    gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
    
    oscillator.start(now);
    oscillator.stop(now + 0.5);
}}

function autoCorrelate(buffer, sampleRate) {{
    const SIZE = buffer.length;
    let rms = 0;
    
    for (let i = 0; i < SIZE; i++) {{
        rms += buffer[i] * buffer[i];
    }}
    rms = Math.sqrt(rms / SIZE);
    
    if (rms < 0.01) return -1;
    
    let r1 = 0, r2 = SIZE - 1;
    const threshold = 0.2;
    
    for (let i = 0; i < SIZE / 2; i++) {{
        if (Math.abs(buffer[i]) < threshold) {{ r1 = i; break; }}
    }}
    for (let i = 1; i < SIZE / 2; i++) {{
        if (Math.abs(buffer[SIZE - i]) < threshold) {{ r2 = SIZE - i; break; }}
    }}
    
    const buf2 = buffer.slice(r1, r2);
    const newSize = buf2.length;
    
    if (newSize < 2) return -1;
    
    const c = new Array(newSize).fill(0);
    for (let i = 0; i < newSize; i++) {{
        for (let j = 0; j < newSize - i; j++) {{
            c[i] += buf2[j] * buf2[j + i];
        }}
    }}
    
    let d = 0;
    while (d < newSize - 1 && c[d] > c[d + 1]) d++;
    
    let maxval = -1, maxpos = -1;
    for (let i = d; i < newSize; i++) {{
        if (c[i] > maxval) {{
            maxval = c[i];
            maxpos = i;
        }}
    }}
    
    if (maxpos < 1) return -1;
    
    let T0 = maxpos;
    
    if (T0 > 0 && T0 < newSize - 1) {{
        const x1 = c[T0 - 1], x2 = c[T0], x3 = c[T0 + 1];
        const a = (x1 + x3 - 2 * x2) / 2;
        const b = (x3 - x1) / 2;
        if (a) T0 = T0 - b / (2 * a);
    }}
    
    const freq = sampleRate / T0;
    
    if (freq > 60 && freq < 1000) {{
        return freq;
    }}
    return -1;
}}

// Initialize on load
initUI();
</script>

</body>
</html>
    """


def main():
    """Main Streamlit application orchestrator."""
    
    # Configure page
    render_page_config()
    
    # Initialize state
    initialize_session_state()
    
    # Render minimal header
    render_header()
    
    # Render sidebar settings
    render_sidebar(DEFAULT_REFERENCE_FREQ, DEFAULT_TEMPERAMENT)
    
    # Get current reference frequency from session state
    ref_freq = st.session_state.get('reference_freq', DEFAULT_REFERENCE_FREQ)
    
    # Full JavaScript-based tuner with string rows and piano
    components.html(get_full_tuner_html(ref_freq), height=700, scrolling=True)


def run_with_error_handling():
    """Run the app with proper error handling and user feedback."""
    try:
        main()
    except Exception as e:
        print("\n" + "=" * 70)
        print("🎸 GUITAR TUNER - ERROR")
        print("=" * 70)
        print(f"\nError Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print("\nFull Traceback:")
        print("-" * 70)
        
        import traceback
        traceback.print_exc()
        
        print("-" * 70)
        print("\nPlease check:")
        print("1. Python version is 3.9 or higher")
        print("2. All dependencies are installed: pip install -r requirements.txt")
        print("3. Virtual environment is activated")
        print("4. All source files are present (check src/ directory)")
        print("\nFor more help, see SETUP_GUIDE.md or README.md")
        print("=" * 70)
        
        sys.exit(1)


if __name__ == "__main__":
    run_with_error_handling()
