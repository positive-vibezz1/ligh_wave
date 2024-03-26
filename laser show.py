import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import threading
import matplotlib.colors as mcolors

def capture_and_visualize_sound():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000

    audio = pyaudio.PyAudio()

    fig, ax = plt.subplots(figsize=(19.2, 10.8))  # Adjust the figure size to match your screen size
    x = np.arange(0, CHUNK)
    line, = ax.plot(x, np.random.rand(CHUNK))

    ax.set_ylim(0, 500)
    ax.set_xlim(0, CHUNK)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)  # Fill the entire tkinter window

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        data_int = np.frombuffer(data, dtype=np.int16)

        # Dynamically adjust the size of x
        x = np.arange(0, len(data_int))

        line.set_ydata(data_int)
        ax.set_xlim(0, len(data_int))  # Update x-axis limit

        # Normalize amplitude separately
        normalized_amplitude = np.abs(data_int) / (2 ** 15)  # Normalize amplitude to [0, 1]
        # Ensure normalized_amplitude has the correct shape for color mapping
        normalized_amplitude = np.repeat(normalized_amplitude[:, np.newaxis], 4, axis=1)  # Repeat values for RGBA
        colors = plt.cm.viridis(normalized_amplitude) #Uses viridis scale
        #hex_colors = mcolors.to_hex(colors, keep_alpha=False) #convertes rgb to hexa
        hex_colors = ['#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255)) for r, g, b, _ in colors[0]]
        # Set the color of each point in the line plot individually
        line_data = line.get_data()
        for i, hex_color in enumerate(hex_colors):
            rgba_color = mcolors.hex2color(hex_color)  # Convert hex to RGBA
            rgba_color = list(rgba_color)  # Convert tuple to list for modification
            rgba_color.append(1.0)  # Add alpha value (opacity)
            line_data[1][4 * i:4 * (i + 1)] = rgba_color  # Set RGBA color for each point


        fig.canvas.draw()
        fig.canvas.flush_events()

    stream.stop_stream()
    stream.close()
    audio.terminate()

def create_gui():

    global root
    root = tk.Tk()
    root.title("Music Visualizer")
    root.geometry("1920x1080")  # Open tkinter window in fullscreen mode

if __name__ == "__main__":
    create_gui()

    # Start capturing sound and visualizing it in a separate thread
    capture_thread = threading.Thread(target=capture_and_visualize_sound)
    capture_thread.daemon = True
    capture_thread.start()   
    root.mainloop()
