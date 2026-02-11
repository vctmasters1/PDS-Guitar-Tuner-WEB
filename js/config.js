/**
 * Guitar Tuner - Configuration
 * All constants and configuration values
 */

// Reference frequency (A4) - can be changed by user
let REFERENCE_FREQ = 440;

// dB threshold for pitch detection
let DB_THRESHOLD = -40;

// Temperament system ('equal' or 'just')
let TEMPERAMENT = 'equal';

// Just Intonation ratios (relative to the root note)
// These are the pure harmonic ratios for each interval
const JUST_RATIOS = {
    'C': 1,           // Unison
    'C#': 16/15,      // Minor second
    'D': 9/8,         // Major second
    'D#': 6/5,        // Minor third
    'E': 5/4,         // Major third
    'F': 4/3,         // Perfect fourth
    'F#': 45/32,      // Tritone
    'G': 3/2,         // Perfect fifth
    'G#': 8/5,        // Minor sixth
    'A': 5/3,         // Major sixth
    'A#': 9/5,        // Minor seventh
    'B': 15/8         // Major seventh
};

// Guitar strings configuration
// Each string has: name, display name, semitones from A4, and color
const GUITAR_STRINGS = [
    { name: 'E2', displayName: 'E (6)', semitones: -29, note: 'E', octave: 2, color: '#8B7355' },
    { name: 'A2', displayName: 'A (5)', semitones: -24, note: 'A', octave: 2, color: '#9D8164' },
    { name: 'D3', displayName: 'D (4)', semitones: -19, note: 'D', octave: 3, color: '#AF8F73' },
    { name: 'G3', displayName: 'G (3)', semitones: -14, note: 'G', octave: 3, color: '#C19D82' },
    { name: 'B3', displayName: 'B (2)', semitones: -10, note: 'B', octave: 3, color: '#D3AB91' },
    { name: 'E4', displayName: 'E (1)', semitones: -5, note: 'E', octave: 4, color: '#E5B9A0' }
];

// Piano notes array (populated by calculateFrequencies)
let PIANO_NOTES = [];

// Note names for generating piano keys
const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

// Tuning thresholds (in cents)
const THRESHOLD_IN_TUNE = 5;   // ±5 cents = in tune
const THRESHOLD_CLOSE = 15;    // ±15 cents = close
const THRESHOLD_DETECT = 30;   // ±30 Hz = activate string row

/**
 * Calculate frequency for a given note using current temperament
 * @param {string} note - Note name (e.g., 'E', 'A', 'G#')
 * @param {number} octave - Octave number
 * @returns {number} Frequency in Hz
 */
function calculateNoteFrequency(note, octave) {
    if (TEMPERAMENT === 'equal') {
        // Equal Temperament: freq = ref * 2^(semitones/12)
        const noteIndex = NOTE_NAMES.indexOf(note);
        const semitonesFromA4 = (octave - 4) * 12 + (noteIndex - 9);
        return REFERENCE_FREQ * Math.pow(2, semitonesFromA4 / 12);
    } else {
        // Just Intonation: use pure harmonic ratios
        // Calculate C4 as the base (A4 / ratio of A)
        const C4 = REFERENCE_FREQ / JUST_RATIOS['A'];
        const ratio = JUST_RATIOS[note] || 1;
        const octaveMultiplier = Math.pow(2, octave - 4);
        return C4 * ratio * octaveMultiplier;
    }
}

/**
 * Calculate all frequencies based on current reference frequency and temperament
 */
function calculateFrequencies() {
    // Calculate guitar string frequencies
    GUITAR_STRINGS.forEach(s => {
        s.freq = calculateNoteFrequency(s.note, s.octave);
    });
    
    // Generate piano notes (D2 to A4)
    PIANO_NOTES = [];
    for (let octave = 2; octave <= 4; octave++) {
        for (let i = 0; i < 12; i++) {
            const note = NOTE_NAMES[i];
            const noteName = note + octave;
            const freq = calculateNoteFrequency(note, octave);
            
            // Filter to D2 through A4
            if ((octave === 2 && i >= 2) || (octave === 3) || (octave === 4 && i <= 9)) {
                PIANO_NOTES.push({
                    name: noteName,
                    note: note,
                    octave: octave,
                    freq: freq,
                    isBlack: note.includes('#')
                });
            }
        }
    }
}

/**
 * Update reference frequency from dropdown
 */
function updateReferenceFreq() {
    REFERENCE_FREQ = parseFloat(document.getElementById('refFreq').value);
    calculateFrequencies();
    initUI();
}

/**
 * Update temperament from dropdown
 */
function updateTemperament() {
    TEMPERAMENT = document.getElementById('temperament').value;
    calculateFrequencies();
    initUI();
}

/**
 * Update dB threshold from slider
 */
function updateThreshold() {
    DB_THRESHOLD = parseInt(document.getElementById('dbThreshold').value);
    document.getElementById('dbThresholdVal').textContent = DB_THRESHOLD + ' dB';
}

/**
 * Show the info modal
 */
function showInfoModal() {
    const modal = document.getElementById('infoModal');
    modal.style.display = 'flex';
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

/**
 * Hide the info modal
 */
function hideInfoModal(event) {
    // If called from overlay click, only close if clicked on overlay itself
    if (event && event.target !== event.currentTarget) return;
    const modal = document.getElementById('infoModal');
    modal.style.display = 'none';
    modal.classList.remove('active');
    document.body.style.overflow = '';
}
