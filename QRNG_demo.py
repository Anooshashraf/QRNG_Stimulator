import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from math import log2
import random

# Core QRNG Simulation Functions

def simulate_photon_polarization(num_photons):
    return [random.choice(['0', '1']) for _ in range(num_photons)]

def simulate_photodiode_signals(bits):
    data = []
    for bit in bits:
        if bit == '0':
            d0 = np.random.uniform(0.8, 1.0)
            d1 = np.random.uniform(0.0, 0.2)
        else:
            d0 = np.random.uniform(0.0, 0.2)
            d1 = np.random.uniform(0.8, 1.0)
        data.append((d0, d1))
    return data

def generate_bits_from_signals(data):
    bits = []
    for d0, d1 in data:
        if abs(d0 - d1) < 0.05:
            continue
        bits.append('0' if d0 > d1 else '1')
    return bits

def von_neumann_extractor(bits):
    output = []
    for i in range(0, len(bits) - 1, 2):
        a, b = bits[i], bits[i+1]
        if a != b:
            output.append('0' if (a, b) == ('0', '1') else '1')
    return output

def calculate_entropy(bits, window=100):
    entropies = []
    for i in range(0, len(bits) - window + 1, window):
        segment = bits[i:i+window]
        p0 = segment.count('0') / window
        p1 = segment.count('1') / window
        if p0 > 0 and p1 > 0:
            entropy = -(p0 * log2(p0) + p1 * log2(p1))
        else:
            entropy = 0
        entropies.append(entropy)
    return entropies

def plot_entropy(entropies, title):
    plt.figure(figsize=(8, 4))
    plt.plot(entropies, marker='o')
    plt.title(title)
    plt.xlabel("Window Index")
    plt.ylabel("Entropy")
    plt.ylim(0, 1.05)
    plt.grid(True)
    plt.show()


class QRNG_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Random Number Generator (QRNG) Simulator")

        self.num_photons = tk.IntVar(value=1000)
        self.raw_bits = []
        self.post_bits = []

        # Layout
        tk.Label(root, text="Number of Photons:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(root, textvariable=self.num_photons).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(root, text="Generate Random Bits", command=self.run_simulation).grid(row=0, column=2, padx=5)
        tk.Button(root, text="Plot Entropy", command=self.plot_entropy_graphs).grid(row=0, column=3, padx=5)
        tk.Button(root, text="Save Bitstream", command=self.save_bitstream).grid(row=0, column=4, padx=5)

        self.output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
        self.output_box.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

    def run_simulation(self):
        n = self.num_photons.get()
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"Simulating {n} photons...\n")

        bitstream = simulate_photon_polarization(n)
        analog_signals = simulate_photodiode_signals(bitstream)
        self.raw_bits = generate_bits_from_signals(analog_signals)
        self.post_bits = von_neumann_extractor(self.raw_bits)

        self.output_box.insert(tk.END, f"Raw Bits ({len(self.raw_bits)}):\n{''.join(self.raw_bits[:100])}...\n\n")
        self.output_box.insert(tk.END, f"Post-Processed Bits ({len(self.post_bits)}):\n{''.join(self.post_bits[:100])}...\n\n")
        self.output_box.insert(tk.END, f"Simulation complete.\n")

    def plot_entropy_graphs(self):
        if not self.raw_bits:
            messagebox.showwarning("Warning", "Run the simulation first.")
            return
        raw_entropy = calculate_entropy(self.raw_bits)
        post_entropy = calculate_entropy(self.post_bits)
        plot_entropy(raw_entropy, "Entropy of Raw Bitstream")
        plot_entropy(post_entropy, "Entropy of Post-Processed Bitstream")

    def save_bitstream(self):
        if not self.post_bits:
            messagebox.showwarning("Warning", "No data to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(''.join(self.post_bits))
            messagebox.showinfo("Success", f"Saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRNG_GUI(root)
    root.mainloop()
