import numpy as np
from scipy.io import wavfile
import math

# Function to convert frequency to musical note
def freq_to_note(freq):
    if freq <= 0:
        return "Unknown"
    
    # A4 = 440 Hz, MIDI 69
    midi_num = round(12 * math.log2(freq / 440.0) + 69)
    
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note = note_names[midi_num % 12]
    octave = midi_num // 12 - 1  # MIDI octave formula
    
    return f"{note}{octave}"

# Step 1: Read audio file (mono)
sr, data = wavfile.read("R_c2.wav")  # replace with your .wav file
if data.ndim > 1:  # If stereo, take one channel
    data = data[:, 0]

# Step 2: Apply FFT
fft_result = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(fft_result), 1/sr)

# Step 3: Take positive freqs only
positive_freqs = frequencies[:len(frequencies)//2]
magnitude = np.abs(fft_result[:len(frequencies)//2])

# Step 4: Find dominant frequency
dominant_freq = positive_freqs[np.argmax(magnitude)]
print("Dominant frequency:", dominant_freq, "Hz")

# Step 5: Map to musical note
note = freq_to_note(dominant_freq)
print("Detected Note:", note)
