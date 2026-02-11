/**
 * Guitar Tuner - UI Rendering
 * Functions to build and update the user interface
 */

/**
 * Initialize the UI - render string rows and piano keyboard
 * Called on page load and when reference frequency changes
 */
function initUI() {
    renderStringRows();
    renderPianoKeyboard();
}

/**
 * Render the 6 guitar string rows with gauges
 */
function renderStringRows() {
    const container = document.getElementById('string-rows');
    container.innerHTML = '';
    
    GUITAR_STRINGS.forEach((s, idx) => {
        container.innerHTML += `
            <div id="string-${idx}" class="string-row">
                <div class="string-name" style="background: ${s.color};">${s.displayName}</div>
                <div class="string-info">
                    <div class="string-target">${s.freq.toFixed(2)} Hz</div>
                </div>
                <div class="gauge-container">
                    <div class="gauge-labels"><span>♭ FLAT</span><span>✓</span><span>♯ SHARP</span></div>
                    <div class="gauge-bar">
                        <div class="gauge-center"></div>
                        <div id="needle-${idx}" class="gauge-needle"></div>
                    </div>
                    <div id="cents-${idx}" class="cents-display">-- cents</div>
                </div>
                <div id="status-${idx}" class="string-status status-idle">IDLE</div>
            </div>
        `;
    });
}

/**
 * Render the vertical piano keyboard
 */
function renderPianoKeyboard() {
    const pianoContainer = document.getElementById('piano-container');
    pianoContainer.innerHTML = '';
    
    PIANO_NOTES.forEach((p, idx) => {
        // Check if this note matches a guitar string
        const isGuitarString = GUITAR_STRINGS.find(s => Math.abs(s.freq - p.freq) < 1);
        const guitarColor = isGuitarString ? isGuitarString.color : null;
        const keyClass = p.isBlack ? 'black' : 'white';
        const guitarClass = isGuitarString ? 'guitar-string' : '';
        const style = isGuitarString ? `border-left-color: ${guitarColor}; background: ${guitarColor};` : '';
        
        pianoContainer.innerHTML += `
            <div id="piano-${idx}" class="piano-key ${keyClass} ${guitarClass}" style="${style}" onclick="playNote(${p.freq})">
                <span class="key-note">${p.name}</span>
                <span class="key-freq">${p.freq.toFixed(1)} Hz</span>
            </div>
        `;
    });
}
