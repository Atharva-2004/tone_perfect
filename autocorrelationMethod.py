import numpy as np
from scipy.io.wavfile import read
import math

def freq_to_note(freq):
    if freq <= 0:
        return "Unknown"
    midi_num = round(12 * math.log2(freq / 440.0) + 69)
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note = note_names[midi_num % 12]
    octave = midi_num // 12 - 1
    return f"{note}{octave}"

def detect_pitch_autocorr(filename):
    sr, data = read(filename)
    if data.ndim > 1:
        data = data[:, 0]  # mono
    
    # Normalize
    data = data.astype(np.float32)
    data = data / np.max(np.abs(data))

    # Autocorrelation
    corr = np.correlate(data, data, mode="full")
    corr = corr[len(corr)//2:]

    # Find first minimum, then maximum after it
    d = np.diff(corr)
    start = np.where(d > 0)[0][0]   # first positive slope
    peak = np.argmax(corr[start:]) + start

    # Fundamental frequency
    period = peak
    freq = sr / period

    return freq, freq_to_note(freq)

# Test with real instrument WAV
filename = "single_notes/R_c2s.wav"   # replace with C3/C#3/D3 file
freq, note = detect_pitch_autocorr(filename)
print(f"🎵 {filename} → {freq:.2f} Hz → {note}")



# issues- c1, c2, c1s