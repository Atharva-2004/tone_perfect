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
    if len(y) < 2:
        return None

    # Autocorrelation via FFT (much faster than np.correlate)
    corr = np.fft.irfft(np.fft.rfft(y) * np.conj(np.fft.rfft(y)))

    # Only keep positive lags
    corr = corr[:len(corr)//2]

    # Define min/max lag from frequency bounds
    min_lag = int(sr / fmax)
    max_lag = int(sr / fmin)
    if max_lag >= len(corr):
        max_lag = len(corr) - 1

    # Find peak within lag range
    peak = np.argmax(corr[min_lag:max_lag]) + min_lag
    if peak <= 0:
        return None
    freq = sr / peak
    return freq

# ---------- Main Function (with onset detection) ----------
def detect_notes_in_file(filename):
    y, sr = librosa.load(filename, sr=None)

    # Normalize once
    y = y.astype(np.float32)
    y = y / np.max(np.abs(y))

    # Onset detection (find where notes begin)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Add the end of the file as the last boundary
    onset_times = np.append(onset_times, librosa.get_duration(y=y, sr=sr))

    notes = []
    for i in range(len(onset_times) - 1):
        start = int(onset_times[i] * sr)
        end = int(onset_times[i+1] * sr)
        chunk = y[start:end]

    # Skip tiny or silent chunks
        if len(chunk) < int(0.05 * sr):  # shorter than 50 ms
            continue
        if np.sqrt(np.mean(chunk**2)) < 0.015:  # too quiet
            continue

        freq = detect_pitch_autocorr(chunk, sr)
        note = freq_to_note(freq)
        notes.append(note)

        if freq:
            print(f"Note {i+1}: {note} (freq ~ {freq:.2f} Hz)")
        else:
            print(f"Note {i+1}: Unknown")

    return notes

# ---------- Example ----------
filename = "multiple_notes/R_c3-d3-e3-f3.wav"  # replace with your file
notes = detect_notes_in_file(filename)
print("Detected sequence:", notes)
