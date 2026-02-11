/**
 * Guitar Tuner - Audio Processing
 * Web Audio API and pitch detection algorithms
 */

// Audio context and nodes
let audioContext = null;
let analyser = null;
let microphone = null;
let mediaStream = null;
let intervalId = null;
let lastValidFreq = null;
let playbackContext = null;

/**
 * Start audio capture from microphone
 */
function startAudio() {
    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(function(stream) {
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
            
            // Start pitch detection loop (10Hz update rate)
            intervalId = setInterval(detectPitch, 100);
        })
        .catch(function(err) {
            document.getElementById('status').innerText = 'Error: ' + err.message;
            document.getElementById('status').style.color = '#f44336';
        });
}

/**
 * Stop audio capture and cleanup
 */
function stopAudio() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
    lastValidFreq = null;
    
    // Update UI
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('status').innerText = 'Stopped';
    document.getElementById('status').style.color = '#888';
    document.getElementById('hz-val').innerText = '----.--';
    document.getElementById('db-val').innerText = '---.-';
    
    // Reset all string rows
    GUITAR_STRINGS.forEach((s, idx) => {
        document.getElementById('string-' + idx).classList.remove('active');
        document.getElementById('string-freq-' + idx).innerText = '-- Hz';
        document.getElementById('needle-' + idx).style.left = '50%';
        document.getElementById('needle-' + idx).style.background = '#888';
        document.getElementById('cents-' + idx).innerText = '-- cents';
        document.getElementById('status-' + idx).className = 'string-status status-idle';
        document.getElementById('status-' + idx).innerText = 'IDLE';
    });
    
    // Reset piano highlights
    PIANO_NOTES.forEach((p, idx) => {
        document.getElementById('piano-' + idx).classList.remove('detected');
    });
}

/**
 * Format frequency for display
 */
function formatHz(freq) {
    if (freq <= 0) return '----.--';
    return freq.toFixed(2).padStart(7, ' ');
}

/**
 * Format dB level for display
 */
function formatDb(db) {
    if (db <= -100) return '---.-';
    return db.toFixed(1).padStart(5, ' ');
}

/**
 * Main pitch detection loop
 * Called every 100ms when audio is active
 */
function detectPitch() {
    if (!analyser) return;
    
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Float32Array(bufferLength);
    analyser.getFloatTimeDomainData(dataArray);
    
    // Calculate RMS for dB level
    let sum = 0;
    for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i] * dataArray[i];
    }
    const rms = Math.sqrt(sum / dataArray.length);
    const db = rms > 0 ? 20 * Math.log10(rms) : -100;
    
    document.getElementById('db-val').innerText = formatDb(db);
    
    // Reset all visual states
    GUITAR_STRINGS.forEach((s, idx) => {
        document.getElementById('string-' + idx).classList.remove('active');
    });
    PIANO_NOTES.forEach((p, idx) => {
        document.getElementById('piano-' + idx).classList.remove('detected');
    });
    
    // Check if signal is above threshold
    if (db < DB_THRESHOLD) {
        document.getElementById('hz-val').innerText = '----.--';
        lastValidFreq = null;
        return;
    }
    
    // Detect pitch using autocorrelation
    const sampleRate = audioContext.sampleRate;
    let frequency = autoCorrelate(dataArray, sampleRate);
    let freqRounded = frequency > 0 ? Math.round(frequency * 100) / 100 : -1;
    
    // Harmonic filtering to prevent octave jumps
    if (freqRounded > 0 && lastValidFreq !== null) {
        const ratio = freqRounded / lastValidFreq;
        // Detected frequency jumped to octave - keep previous
        if (ratio > 1.9 && ratio < 2.1) {
            freqRounded = lastValidFreq;
        }
        // Detected frequency dropped to sub-octave - keep previous
        else if (ratio > 0.48 && ratio < 0.52 && db < -20) {
            freqRounded = lastValidFreq;
        }
    }
    
    if (freqRounded > 0) lastValidFreq = freqRounded;
    
    document.getElementById('hz-val').innerText = formatHz(freqRounded);
    
    if (freqRounded <= 0) return;
    
    // Find closest guitar string
    let closestIdx = -1;
    let minDist = Infinity;
    GUITAR_STRINGS.forEach((s, idx) => {
        const dist = Math.abs(freqRounded - s.freq);
        if (dist < minDist) {
            minDist = dist;
            closestIdx = idx;
        }
    });
    
    // Activate string row if within detection threshold
    if (closestIdx >= 0 && minDist < THRESHOLD_DETECT) {
        const s = GUITAR_STRINGS[closestIdx];
        const cents = 1200 * Math.log2(freqRounded / s.freq);
        const centsRounded = Math.round(cents * 10) / 10;
        
        // Activate this string row
        document.getElementById('string-' + closestIdx).classList.add('active');
        document.getElementById('string-freq-' + closestIdx).innerText = freqRounded.toFixed(2) + ' Hz';
        
        // Update needle position
        const clampedCents = Math.max(-50, Math.min(50, centsRounded));
        const needlePos = 50 + clampedCents;
        const needle = document.getElementById('needle-' + closestIdx);
        needle.style.left = needlePos + '%';
        
        // Update cents display
        const centsText = (centsRounded >= 0 ? '+' : '') + centsRounded.toFixed(1);
        document.getElementById('cents-' + closestIdx).innerText = centsText + ' cents';
        
        // Update status and needle color
        const statusEl = document.getElementById('status-' + closestIdx);
        if (Math.abs(centsRounded) <= THRESHOLD_IN_TUNE) {
            needle.style.background = '#4CAF50';
            statusEl.className = 'string-status status-intune';
            statusEl.innerText = '✓ IN TUNE';
        } else if (Math.abs(centsRounded) <= THRESHOLD_CLOSE) {
            needle.style.background = '#ff9800';
            statusEl.className = 'string-status status-close';
            statusEl.innerText = '~ CLOSE';
        } else {
            needle.style.background = '#f44336';
            statusEl.className = 'string-status status-off';
            statusEl.innerText = centsRounded < 0 ? '♭ FLAT' : '♯ SHARP';
        }
    }
    
    // Highlight closest piano key
    let closestPianoIdx = -1;
    let minPianoDist = Infinity;
    PIANO_NOTES.forEach((p, idx) => {
        const dist = Math.abs(freqRounded - p.freq);
        if (dist < minPianoDist) {
            minPianoDist = dist;
            closestPianoIdx = idx;
        }
    });
    if (closestPianoIdx >= 0 && minPianoDist < 20) {
        document.getElementById('piano-' + closestPianoIdx).classList.add('detected');
    }
}

/**
 * Play a reference tone at the specified frequency
 */
function playNote(frequency) {
    if (!playbackContext) {
        playbackContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    
    const now = playbackContext.currentTime;
    const oscillator = playbackContext.createOscillator();
    const gainNode = playbackContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(playbackContext.destination);
    
    oscillator.frequency.value = frequency;
    oscillator.type = 'sine';
    
    // Envelope: quick attack, gradual release
    gainNode.gain.setValueAtTime(0.3, now);
    gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
    
    oscillator.start(now);
    oscillator.stop(now + 0.5);
}

/**
 * Autocorrelation-based pitch detection
 * Returns detected frequency in Hz, or -1 if no valid pitch
 */
function autoCorrelate(buffer, sampleRate) {
    const SIZE = buffer.length;
    let rms = 0;
    
    // Calculate RMS
    for (let i = 0; i < SIZE; i++) {
        rms += buffer[i] * buffer[i];
    }
    rms = Math.sqrt(rms / SIZE);
    
    // Too quiet - no valid pitch
    if (rms < 0.01) return -1;
    
    // Trim silent ends of buffer
    let r1 = 0, r2 = SIZE - 1;
    const threshold = 0.2;
    
    for (let i = 0; i < SIZE / 2; i++) {
        if (Math.abs(buffer[i]) < threshold) {
            r1 = i;
            break;
        }
    }
    for (let i = 1; i < SIZE / 2; i++) {
        if (Math.abs(buffer[SIZE - i]) < threshold) {
            r2 = SIZE - i;
            break;
        }
    }
    
    const buf2 = buffer.slice(r1, r2);
    const newSize = buf2.length;
    
    if (newSize < 2) return -1;
    
    // Compute autocorrelation
    const c = new Array(newSize).fill(0);
    for (let i = 0; i < newSize; i++) {
        for (let j = 0; j < newSize - i; j++) {
            c[i] += buf2[j] * buf2[j + i];
        }
    }
    
    // Find first dip (start of first period)
    let d = 0;
    while (d < newSize - 1 && c[d] > c[d + 1]) d++;
    
    // Find maximum correlation after dip
    let maxval = -1, maxpos = -1;
    for (let i = d; i < newSize; i++) {
        if (c[i] > maxval) {
            maxval = c[i];
            maxpos = i;
        }
    }
    
    if (maxpos < 1) return -1;
    
    let T0 = maxpos;
    
    // Parabolic interpolation for sub-sample accuracy
    if (T0 > 0 && T0 < newSize - 1) {
        const x1 = c[T0 - 1], x2 = c[T0], x3 = c[T0 + 1];
        const a = (x1 + x3 - 2 * x2) / 2;
        const b = (x3 - x1) / 2;
        if (a) T0 = T0 - b / (2 * a);
    }
    
    const freq = sampleRate / T0;
    
    // Valid guitar frequency range
    if (freq > 60 && freq < 1000) {
        return freq;
    }
    return -1;
}
