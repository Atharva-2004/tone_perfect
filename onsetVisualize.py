import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load audio
y, sr = librosa.load("multiple_notes/R_fast_c4-c4-d4-c4-f4-e4-c4-c4-d4-c4-g4-f4.wav")

# Detect onsets
onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
onset_times = np.append(onset_times, librosa.get_duration(y=y, sr=sr))


# --- Filter onsets ---
filtered_onset_times = []
for i in range(len(onset_times) - 1):
    start = int(onset_times[i] * sr)
    end = int(onset_times[i+1] * sr)
    chunk = y[start:end]

    if len(chunk) < int(0.02 * sr):  # too short
        continue
    if np.sqrt(np.mean(chunk**2)) < 0.01:  # too quiet
        continue

    filtered_onset_times.append(onset_times[i])

onset_times = filtered_onset_times

# Plot waveform with onset markers
plt.figure(figsize=(14, 6))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
for onset in onset_times:
    plt.axvline(x=onset, color="r", linestyle="--", alpha=0.8)
plt.title("Waveform with Filtered Onset Detection")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()

# Plot spectrogram with onsets
D = np.abs(librosa.stft(y))
DB = librosa.amplitude_to_db(D, ref=np.max)

plt.figure(figsize=(14, 6))
librosa.display.specshow(DB, sr=sr, x_axis="time", y_axis="log")
plt.colorbar(format="%+2.0f dB")
for onset in onset_times:
    plt.axvline(x=onset, color="r", linestyle="--", alpha=0.8)
plt.title("Spectrogram with Filtered Onset Detection")
plt.show()
