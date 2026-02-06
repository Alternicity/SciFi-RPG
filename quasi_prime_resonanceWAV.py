import math
import numpy as np
import wave
import struct

# Constants for sound generation
SAMPLE_RATE = 44100  # Hz
DURATION = 0.5       # seconds per tone
BASE_FREQUENCY = 220  # A3 in Hz

# Helper: Check if a number is quasi-prime (not prime, but close)
def is_quasi_prime(n):
    if n < 4:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return True
    return False

# Generate the frequency series
def generate_quasi_prime_frequencies(base_freq, count=12):
    frequencies = []
    for phase in range(count):
        modulated = int((phase * math.sqrt(10)) % 12)
        if is_quasi_prime(modulated + 7):  # offset to avoid trivial values
            freq = base_freq * (1 + (modulated / 12))
            frequencies.append(freq)
    return frequencies

# Generate tone wave
def generate_tone(freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = 0.5 * np.sin(2 * np.pi * freq * t)
    return (wave_data * 32767).astype(np.int16)

# Create a wave file from tones
def save_wave(filename, frequencies):
    wave_data = np.concatenate([generate_tone(f, DURATION, SAMPLE_RATE) for f in frequencies])
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(wave_data.tobytes())
    return filename

# Generate and save the wave file
frequencies = generate_quasi_prime_frequencies(BASE_FREQUENCY)
output_file = "/mnt/data/quasi_prime_resonance.wav"
save_wave(output_file, frequencies)

output_file
