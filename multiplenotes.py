# works fine for slow paced notes (with a little silence between them)


import numpy as np
import librosa

# ---------- Frequency to Note Mapping ----------
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F",
              "F#", "G", "G#", "A", "A#", "B"]

def freq_to_note(freq):
    if freq is None or freq <= 0:
        return "Unknown"
    A4 = 440.0
    semitones = 12 * np.log2(freq / A4)
    midi = int(round(semitones)) + 69
    note = NOTE_NAMES[midi % 12] + str(midi // 12 - 1)
    return note

# ---------- Autocorrelation Pitch Detection ----------
def detect_pitch_autocorr(y, sr, fmin=50, fmax=2000):
    # Autocorrelation via FFT (much faster than np.correlate)
    corr = np.fft.irfft(np.fft.rfft(y) * np.conj(np.fft.rfft(y)))

    # Only keep positive lags
    corr = corr[:len(corr)//2]

    # Define min/max lag from frequency bounds
    min_lag = int(sr / fmax)
    max_lag = int(sr / fmin)

    # Find peak within lag range
    peak = np.argmax(corr[min_lag:max_lag]) + min_lag
    if peak == 0:
        return None
    freq = sr / peak
    return freq

# ---------- Main Function ----------
def detect_notes_in_file(filename, top_db=10):
    y, sr = librosa.load(filename, sr=None)

    # Normalize entire audio once
    y = y.astype(np.float32)
    y = y / np.max(np.abs(y))

    # Split into non-silent chunks
    chunks = librosa.effects.split(y, top_db=top_db)

    notes = []
    for i, (start, end) in enumerate(chunks):
        chunk = y[start:end]

        freq = detect_pitch_autocorr(chunk, sr)
        note = freq_to_note(freq)
        notes.append(note)

        if freq:
            print(f"Note {i+1}: {note} (freq ~ {freq:.2f} Hz)")
        else:
            print(f"Note {i+1}: Unknown")

    return notes

# ---------- Example ----------
filename = "single_notes/R_d4.wav"  # replace with your file
notes = detect_notes_in_file(filename)
print("Detected sequence:", notes)
