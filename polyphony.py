import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Function to convert frequency → musical note
def freq_to_note(freq):
    if freq == 0: return "Rest"
    # MIDI formula
    midi = int(round(69 + 12 * np.log2(freq / 440.0)))
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note = note_names[midi % 12] + str(midi // 12 - 1)
    return note

# Load audio
y, sr = librosa.load("simultaneous_notes/river_flows_in_you_part1.wav")

# Onset detection
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# Short-time Fourier transform
S = np.abs(librosa.stft(y))

# Top-N peak note detection
N_TOP =1  # how many simultaneous notes to detect
detected_notes = []

for onset in onset_frames:
    spectrum = S[:, onset]
    peaks, _ = find_peaks(spectrum, height=np.max(spectrum)*0.3)
    top_peaks = sorted(peaks, key=lambda p: spectrum[p], reverse=True)[:N_TOP]
    freqs = librosa.fft_frequencies(sr=sr)
    notes = [freq_to_note(freqs[p]) for p in top_peaks]
    detected_notes.append((librosa.frames_to_time(onset, sr=sr), notes))

# --- Plot ---
plt.figure(figsize=(14, 6))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
plt.vlines(onset_times, -1, 1, color='r', linestyle='--', alpha=0.8)

for t, notes in detected_notes:
    plt.text(t, 0.8, ", ".join(notes), rotation=45, fontsize=9, color="blue")

plt.title("Detected Notes (Top-1 Peaks)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()
