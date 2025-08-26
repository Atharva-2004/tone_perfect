import numpy as np
from scipy.io.wavfile import write

def generate_note(filename, freq, duration=2.0, sr=44100):
    """
    Generate a sine wave note and save as .wav file
    filename: output wav file
    freq: frequency in Hz
    duration: seconds
    sr: sample rate
    """
    t = np.linspace(0, duration, int(sr*duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * freq * t)  # 0.5 volume
    write(filename, sr, (waveform * 32767).astype(np.int16))
    print(f"Saved {filename} with freq {freq} Hz")

# Example: Generate C3, C#3, D3
note_freqs = {
    "C3_sine": 130.81,
    "C#3_sine": 138.59,
    "D3_sine": 146.83,
    "D#3_sine": 155.56,
    "E3_sine": 164.81
}

for name, freq in note_freqs.items():
    generate_note(f"{name}.wav", freq)
