import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import log2

# --- PHYSICS + SIGNAL LAYER ---

def emit_photons(n):
    """Simulate photon pulses randomly going to either S or P detector."""
    return [random.choice(['S', 'P']) for _ in range(n)]

def generate_photodiode_signals(photon_paths):
    """Simulate analog signals based on photon detection."""
    analog_data = []
    for path in photon_paths:
        if path == 'S':
            dS = np.random.uniform(0.8, 1.0)
            dP = np.random.uniform(0.0, 0.2)
        else:
            dS = np.random.uniform(0.0, 0.2)
            dP = np.random.uniform(0.8, 1.0)
        analog_data.append((dS, dP))
    return analog_data

def arduino_logic(analog_data):
    """Simulate Arduino signal comparison logic."""
    bits = []
    for dS, dP in analog_data:
        if abs(dS - dP) < 0.05:
            continue  # Discard coincidence
        bits.append('0' if dS > dP else '1')
    return bits

def von_neumann(bits):
    """Von Neumann extractor to remove bias."""
    result = []
    for i in range(0, len(bits) - 1, 2):
        a, b = bits[i], bits[i+1]
        if a != b:
            result.append('0' if a == '0' else '1')
    return result

def calculate_entropy(bits, window=100):
    entropies = []
    for i in range(0, len(bits) - window + 1, window):
        segment = bits[i:i + window]
        p0 = segment.count('0') / window
        p1 = segment.count('1') / window
        if p0 > 0 and p1 > 0:
            entropy = -(p0 * log2(p0) + p1 * log2(p1))
        else:
            entropy = 0
        entropies.append(entropy)
    return entropies

# --- GUI SIMULATOR ---

class QRNGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QRNG Visualization Simulator")
        self.root.geometry("1000x700")

        self.photons = 500
        self.raw_bits = []
        self.processed_bits = []
        self.paths = []

        # Photon emission
        tk.Label(root, text="Number of Photons:").pack()
        self.entry = tk.Entry(root)
        self.entry.insert(0, "500")
        self.entry.pack()

        tk.Button(root, text="Run Simulation", command=self.run_simulation).pack(pady=5)

        # Photon flow output
        self.canvas = tk.Canvas(root, width=900, height=250, bg='white')
        self.canvas.pack(pady=10)

        # Bitstream output
        self.bit_label = tk.Label(root, text="Raw Bits:")
        self.bit_label.pack()
        self.bit_box = tk.Text(root, height=5, width=120)
        self.bit_box.pack()

        # Entropy plot
        self.fig, self.ax = plt.subplots(figsize=(7, 3))
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.plot_canvas.get_tk_widget().pack()

    def draw_photon_paths(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(60, 110, 90, 140, fill="red")  # Laser
        self.canvas.create_text(75, 100, text="Laser", font=("Arial", 8))

        self.canvas.create_line(90, 125, 160, 125, fill="red", width=2)  # Beam
        self.canvas.create_rectangle(160, 105, 190, 145, fill="lightgray")  # Polarizer
        self.canvas.create_text(175, 95, text="45° Polarizer", font=("Arial", 8))

        self.canvas.create_line(190, 125, 250, 125, fill="red", width=2)  # Beam to PBS
        self.canvas.create_rectangle(250, 105, 280, 145, fill="cyan")  # PBS
        self.canvas.create_text(265, 95, text="PBS", font=("Arial", 8))

        for i, path in enumerate(self.paths[:30]):  # Show only first 30 photons
            x = 250
            y = 125
            if path == 'P':
                end_x = 350
                end_y = 125
                color = "green"
            else:
                end_x = 265
                end_y = 50
                color = "orange"
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=color)
            self.canvas.create_line(x, y, end_x, end_y, fill=color, width=1)

        self.canvas.create_oval(345, 120, 355, 130, fill="green")  # P-detector
        self.canvas.create_text(355, 140, text="P", font=("Arial", 8))

        self.canvas.create_oval(260, 45, 270, 55, fill="orange")  # S-detector
        self.canvas.create_text(275, 45, text="S", font=("Arial", 8))

    def run_simulation(self):
        try:
            self.photons = int(self.entry.get())
        except:
            self.photons = 500

        self.paths = emit_photons(self.photons)
        signals = generate_photodiode_signals(self.paths)
        self.raw_bits = arduino_logic(signals)
        self.processed_bits = von_neumann(self.raw_bits)

        # Update bit display
        self.bit_box.delete("1.0", tk.END)
        self.bit_box.insert(tk.END, f"Raw Bits:   {''.join(self.raw_bits[:100])}...\n")
        self.bit_box.insert(tk.END, f"Post Bits:  {''.join(self.processed_bits[:100])}...\n")
        self.bit_box.insert(tk.END, f"Raw Count: {len(self.raw_bits)} | Post-Processed Count: {len(self.processed_bits)}")

        # Redraw photon paths
        self.draw_photon_paths()

        # Plot entropy
        raw_entropy = calculate_entropy(self.raw_bits)
        post_entropy = calculate_entropy(self.processed_bits)
        self.ax.clear()
        self.ax.plot(raw_entropy, label="Raw Entropy", color='blue')
        self.ax.plot(post_entropy, label="Post-Processed Entropy", color='green')
        self.ax.set_ylim(0, 1.05)
        self.ax.set_title("Entropy Graph")
        self.ax.set_ylabel("Entropy")
        self.ax.set_xlabel("Window Index")
        self.ax.legend()
        self.plot_canvas.draw()


# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QRNGApp(root)
    root.mainloop()
