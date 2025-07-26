import tkinter as tk
import random
import numpy as np
import time
import threading
import platform
from math import log2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Windows beep support
if platform.system() == "Windows":
    import winsound
else:
    import os


ENABLE_ARDUINO = False
ARDUINO_PORT = 'COM3' 
BAUD_RATE = 9600

try:
    if ENABLE_ARDUINO:
        import serial
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print("Arduino not connected:", e)
    ENABLE_ARDUINO = False

class Photon:
    def __init__(self, canvas, path):
        self.canvas = canvas
        self.path = path
        self.x, self.y = 60, 125
        self.id = canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3, fill="red")

    def move_step(self):
        if self.x < 190:
            dx, dy = 6, 0
        elif self.x < 250:
            dx, dy = 6, 0
        elif self.path == 'P':
            dx, dy = 6, 0
        else:
            dx, dy = 0, -6
        self.canvas.move(self.id, dx, dy)
        self.x += dx
        self.y += dy

class QRNGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Random Number Generator - Enhanced")

        self.bitstream = []
        self.post_bits = []

        self.canvas = tk.Canvas(root, width=850, height=300, bg="white")
        self.canvas.pack()

        self.setup_circuit()

        # Controls
        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Label(control_frame, text="Photon Count:").pack(side=tk.LEFT)
        self.count_entry = tk.Entry(control_frame, width=6)
        self.count_entry.insert(0, "50")
        self.count_entry.pack(side=tk.LEFT)

        tk.Button(control_frame, text="Start Simulation", command=self.start_simulation).pack(side=tk.LEFT)

        # Photon processed counter
        self.counter_var = tk.StringVar(value="Photons Processed: 0")
        self.counter_label = tk.Label(control_frame, textvariable=self.counter_var)
        self.counter_label.pack(side=tk.LEFT, padx=10)

        self.bit_box = tk.Text(root, height=3, width=100)
        self.bit_box.pack()

        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status).pack()

        # Plotting area
        self.fig, self.ax = plt.subplots(figsize=(6, 2.5))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_plot.get_tk_widget().pack()
        self.bit_box = tk.Text(root, height=3, width=100)
        self.bit_box.pack()

        self.status = tk.StringVar()
        tk.Label(root, textvariable=self.status).pack()

        # Plotting area
        self.fig, self.ax = plt.subplots(figsize=(6, 2.5))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_plot.get_tk_widget().pack()

    def setup_circuit(self):
        c = self.canvas
        c.create_rectangle(30, 110, 60, 140, fill="red")
        c.create_text(45, 100, text="Laser")
        c.create_rectangle(160, 105, 190, 145, fill="gray")
        c.create_text(175, 95, text="Polarizer")
        c.create_rectangle(250, 105, 280, 145, fill="cyan")
        c.create_text(265, 95, text="PBS")
        c.create_oval(345, 120, 355, 130, fill="green")
        c.create_text(360, 140, text="P Detector")
        c.create_oval(260, 45, 270, 55, fill="orange")
        c.create_text(290, 50, text="S Detector")

    def start_simulation(self):
        try:
            self.count = int(self.count_entry.get())
        except:
            self.count = 50

        self.bitstream.clear()
        self.post_bits.clear()
        self.canvas.delete("all")
        self.setup_circuit()
        self.status.set("Running...")

        threading.Thread(target=self.simulate_photons).start()

    def simulate_photons(self):
        for i in range(self.count):
            delay = random.randint(30, 100) 
            time.sleep(delay / 1000)

            if ENABLE_ARDUINO:
                try:
                    line = arduino.readline().decode().strip()
                    if line in ['0', '1']:
                        bit = line
                    else:
                        bit = random.choice(['0', '1'])
                except:
                    bit = random.choice(['0', '1'])
            else:
                bit = random.choice(['0', '1'])

            path = 'P' if bit == '1' else 'S'
            photon = Photon(self.canvas, path)

            while True:
                photon.move_step()
                if (photon.path == 'P' and photon.x >= 345) or (photon.path == 'S' and photon.y <= 55):
                    self.canvas.delete(photon.id)
                    self.bitstream.append(bit)
                    self.update_bitstream_display()
                    self.play_beep()
                    self.counter_var.set(f"Photons Processed: {i + 1}")
                    break
                time.sleep(0.005)  # Increased photon speed

        self.status.set("Simulation complete.")
        self.process_post_bits()
        self.plot_entropy()

    def update_bitstream_display(self):
        self.bit_box.delete("1.0", tk.END)
        self.bit_box.insert(tk.END, f"Raw: {''.join(self.bitstream[-60:])}\n")

    def play_beep(self):
        if platform.system() == "Windows":
            winsound.Beep(800, 100)
        else:
            os.system('printf "\\a"')  # Cross-platform fallback beep

    def von_neumann(self, bits):
        result = []
        for i in range(0, len(bits) - 1, 2):
            if bits[i] != bits[i+1]:
                result.append('0' if bits[i] == '0' else '1')
        return result

    def process_post_bits(self):
        self.post_bits = self.von_neumann(self.bitstream)
        self.bit_box.insert(tk.END, f"Post: {''.join(self.post_bits[-60:])}\n")

    def calculate_entropy(self, bits, window=20):
        entropies = []
        for i in range(0, len(bits) - window + 1, window):
            segment = bits[i:i+window]
            p0 = segment.count('0') / window
            p1 = segment.count('1') / window
            entropy = -(p0 * log2(p0) + p1 * log2(p1)) if p0 > 0 and p1 > 0 else 0
            entropies.append(entropy)
        return entropies

    def plot_entropy(self):
        raw_entropy = self.calculate_entropy(self.bitstream)
        post_entropy = self.calculate_entropy(self.post_bits)

        self.ax.clear()
        self.ax.plot(raw_entropy, label="Raw", color='blue')
        self.ax.plot(post_entropy, label="Post", color='green')
        self.ax.set_title("Entropy Graph")
        self.ax.set_ylim(0, 1.05)
        self.ax.set_ylabel("Entropy")
        self.ax.legend()
        self.canvas_plot.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = QRNGApp(root)
    root.mainloop()
