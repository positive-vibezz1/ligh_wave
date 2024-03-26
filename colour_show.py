import tkinter as tk
import pyaudio
import numpy as np
import threading
import librosa
from queue import Queue

#Set up the GUI
root = tk.Tk()
root.title("Music Visualization App")
canvas = tk.Canvas(root, width=1920, height=1080, bg='black')
canvas.pack()

#Input
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)

#Audio Processing
def process_audio(q):
    while True:
        data = stream.read(CHUNK)
        q.put(data)

def analyze_audio(q):
    while True:
        data = q.get()
        audio_array = np.frombuffer(data, dtype=np.int16)
        level = np.abs(audio_array).mean()
    
        #Visualization
        canvas.delete("all")

        scale_factor = 0.05

        # Perform FFT to analyze frequency content of the audio signal
        fft_data = np.fft.fft(audio_array)
        freqs = np.fft.fftfreq(len(audio_array), 1/RATE)
        magnitude = np.abs(fft_data)

        # Define frequency ranges of interest
        freq_ranges = [(50, 200), (200, 400), (400, 600), (600, 800), (800, 1000), (1000, 1200),(1200,1400)]

        # Initialize colors for visualization
        colors = ['blue', 'pink', 'red', 'green', 'orange', 'purple', 'yellow']  # Example colors
        vertical_spacing = 50
        y_offset = 50
    
        # Create rectangles based on frequency ranges and their magnitudes
        for i, (low, high) in enumerate(freq_ranges):
            mask = (freqs >= low) & (freqs < high)
            magnitude_in_range = np.mean(magnitude[mask])
            width = 50 + magnitude_in_range * scale_factor  # Adjust width based on magnitude
            height = 50
            canvas.create_rectangle(50, y_offset, 50 + width, y_offset + height, fill=colors[i])
            y_offset += 50
        
        root.update()

#Start threads for audio processing and visualization
q = Queue()
audio_thread = threading.Thread(target=process_audio, args=(q,), daemon=True)
audio_thread.start()

analyze_thread = threading.Thread(target=analyze_audio, args=(q,), daemon=True)
analyze_thread.start()

root.mainloop()