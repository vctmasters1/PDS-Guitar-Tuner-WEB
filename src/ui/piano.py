"""Vertical piano keyboard component for Guitar Tuner UI"""

import streamlit as st
import streamlit.components.v1 as components
from src.core.config import (
    GUITAR_STRINGS,
    COLORS,
    STRING_COLORS,
)


def render_vertical_piano():
    """
    Render a vertical interactive piano keyboard using SVG graphics.
    
    Features:
    - Vertical stacking of all 30+ piano keys (D2 to A4) as SVG
    - Black keys overlaid on top of white keys in correct piano orientation
    - Guitar string notes highlighted with STRING_COLORS
    - Detected note highlighted with accent
    - Click any key to play that frequency via Web Audio API
    - Each key shows note name/octave and frequency (2 decimals)
    """
    st.markdown("### ⌨️ Piano Keyboard")
    
    # Piano configuration: D2 to A4
    piano_notes = [
        'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#',
        'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#',
        'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A'
    ]
    
    piano_octaves = [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1, -1,
                     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0]
    
    white_notes = {'D', 'E', 'F', 'G', 'A', 'B', 'C'}
    
    # SVG dimensions - compact keys that fit in one column
    key_width = 140
    key_height = 35
    white_key_x = 2
    white_key_width = key_width - 4
    black_key_x = 60
    black_key_width = 65
    total_height = len(piano_notes) * key_height
    
    # Start SVG with proper structure
    svg = f'<svg width="100%" height="{total_height}" viewBox="0 0 {key_width} {total_height}" xmlns="http://www.w3.org/2000/svg" style="border: 2px solid {COLORS["text_secondary"]}; border-radius: 8px; background: {COLORS["bg_medium"]}; cursor: pointer;">'
    
    # Draw all keys
    for i, (note, octave_offset) in enumerate(zip(piano_notes, piano_octaves)):
        freq = st.session_state.tuner.calculate_frequency(note, octave_offset)
        octave = 4 + octave_offset
        note_name = f"{note}{octave}"
        y_pos = i * key_height
        
        # Check if guitar string
        is_guitar_string = False
        guitar_string_color = None
        for str_idx, (display_name, str_note, str_octave) in enumerate(GUITAR_STRINGS):
            if str_note == note and str_octave == octave_offset:
                is_guitar_string = True
                guitar_string_color = STRING_COLORS[str_idx]
                break
        
        # Check if detected
        is_detected = False
        if st.session_state.detected_frequency and st.session_state.current_string_idx is not None:
            min_diff = float('inf')
            detected_note_idx = None
            for j, (n, o) in enumerate(zip(piano_notes, piano_octaves)):
                f = st.session_state.tuner.calculate_frequency(n, o)
                diff = abs(f - st.session_state.detected_frequency)
                if diff < min_diff and diff < 50:
                    min_diff = diff
                    detected_note_idx = j
            is_detected = (detected_note_idx == i)
        
        is_white = note in white_notes
        
        if is_white:
            # White key
            fill = guitar_string_color if is_guitar_string else '#f5f5f5'
            stroke = COLORS['status_in_tune'] if is_detected else '#333'
            stroke_width = "3" if is_detected else "2"
            
            svg += f'<rect class="piano-key" data-freq="{freq:.2f}" x="{white_key_x}" y="{y_pos + 1}" width="{white_key_width}" height="{key_height - 2}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" rx="3"/>'
            svg += f'<text x="8" y="{y_pos + 22}" font-size="11" font-weight="bold" fill="#000" font-family="Arial, sans-serif" pointer-events="none">{note_name}  {freq:.1f}Hz</text>'
        else:
            # Black key (narrower, overlaid to the right)
            fill = guitar_string_color if is_guitar_string else '#1a1a1a'
            stroke = COLORS['status_in_tune'] if is_detected else '#111'
            stroke_width = "3" if is_detected else "2"
            
            svg += f'<rect class="piano-key" data-freq="{freq:.2f}" x="{black_key_x}" y="{y_pos + 1}" width="{black_key_width}" height="{key_height - 2}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" rx="2"/>'
            text_color = '#fff' if not is_guitar_string else ('#000' if guitar_string_color in ['#E5B9A0', '#D3AB91'] else '#fff')
            svg += f'<text x="{black_key_x + 8}" y="{y_pos + 22}" font-size="10" font-weight="bold" fill="{text_color}" font-family="Arial, sans-serif" pointer-events="none">{note_name}  {freq:.1f}Hz</text>'
    
    svg += '</svg>'
    
    # HTML wrapper with Web Audio API for clicking and playing
    html_content = f'''
    <div>
        {svg}
    </div>
    <script>
    // Web Audio API setup
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    // Find all piano keys and add click listeners
    document.querySelectorAll('.piano-key').forEach(key => {{
        key.addEventListener('click', function(e) {{
            e.stopPropagation();
            const frequency = parseFloat(this.getAttribute('data-freq'));
            playTone(frequency, 0.5); // Play for 0.5 seconds
        }});
        key.addEventListener('mouseenter', function() {{
            this.style.opacity = '0.8';
        }});
        key.addEventListener('mouseleave', function() {{
            this.style.opacity = '1';
        }});
    }});
    
    function playTone(frequency, duration) {{
        const now = audioContext.currentTime;
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration);
        
        oscillator.start(now);
        oscillator.stop(now + duration);
    }}
    </script>
    '''
    
    components.html(html_content, height=total_height + 50)
