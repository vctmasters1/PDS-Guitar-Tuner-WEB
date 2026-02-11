/**
 * Guitar Tuner - Configuration
 * All constants and configuration values
 */

// Reference frequency (A4) - can be changed by user
let REFERENCE_FREQ = 440;

// dB threshold for pitch detection
let DB_THRESHOLD = -40;

// Guitar strings configuration
// Each string has: name, display name, semitones from A4, and color
const GUITAR_STRINGS = [
    { name: 'E2', displayName: 'E (6)', semitones: -29, color: '#8B7355' },
    { name: 'A2', displayName: 'A (5)', semitones: -24, color: '#9D8164' },
    { name: 'D3', displayName: 'D (4)', semitones: -19, color: '#AF8F73' },
    { name: 'G3', displayName: 'G (3)', semitones: -14, color: '#C19D82' },
    { name: 'B3', displayName: 'B (2)', semitones: -10, color: '#D3AB91' },
    { name: 'E4', displayName: 'E (1)', semitones: -5, color: '#E5B9A0' }
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
 * Calculate all frequencies based on current reference frequency
 * Uses Equal Temperament (12-TET): freq = ref * 2^(semitones/12)
 */
function calculateFrequencies() {
    // Calculate guitar string frequencies
    GUITAR_STRINGS.forEach(s => {
        s.freq = REFERENCE_FREQ * Math.pow(2, s.semitones / 12);
    });
    
    // Generate piano notes (D2 to A4)
    PIANO_NOTES = [];
    for (let octave = 2; octave <= 4; octave++) {
        for (let i = 0; i < 12; i++) {
            const note = NOTE_NAMES[i];
            const noteName = note + octave;
            const semitonesFromA4 = (octave - 4) * 12 + (i - 9);
            const freq = REFERENCE_FREQ * Math.pow(2, semitonesFromA4 / 12);
            
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
 * Update dB threshold from slider
 */
function updateThreshold() {
    DB_THRESHOLD = parseInt(document.getElementById('dbThreshold').value);
    document.getElementById('dbThresholdVal').textContent = DB_THRESHOLD + ' dB';
}
