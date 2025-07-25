# Quantum Random Number Generator (QRNG) Simulator

This project is a graphical simulator for a Quantum Random Number Generator (QRNG) using Python and Tkinter. It visually demonstrates the process of generating random bits using quantum principles and provides entropy analysis of the generated bitstreams. Optionally, it can interface with an Arduino for real hardware-based randomness.

---

## Features

- **Photon Simulation:** Visualizes photons passing through a quantum circuit.
- **Random Bit Generation:** Simulates quantum randomness or reads from Arduino.
- **Von Neumann Post-Processing:** Reduces bias in the raw bitstream.
- **Entropy Plotting:** Visualizes entropy of raw and post-processed bits.
- **Sound Feedback:** Plays a beep for each detected photon.
- **Easy GUI:** User-friendly interface for simulation control.
- **Arduino Support:** (Optional) Use real quantum random data from Arduino.

---

## Requirements

- Python 3.7 or newer
- `numpy`
- `matplotlib`
- (Optional, for Arduino) `pyserial`

Install dependencies with:

```
pip install -r requirements.txt
```

---

## Usage

1. **Run the Simulator:**

   ```
   python QRNG_demo.py
   ```

2. **Controls:**

   - Set the number of photons to simulate.
   - Click **Start Simulation** to begin.
   - View the raw and post-processed bitstreams.
   - Click **Plot Entropy** to see entropy graphs.

3. **Arduino Mode (Optional):**
   - Set `ENABLE_ARDUINO = True` in the script.
   - Install `pyserial`:
     ```
     pip install pyserial
     ```
   - Connect your Arduino and ensure `ARDUINO_PORT` matches your device.
   - Upload code to Arduino that outputs `'0'` or `'1'` over serial.

---

## File Structure

```
QRNG_Stimulator/
│
├── QRNG_demo.py
├── requirements.txt
└── README.md
```

---

## Example

![Screenshot of the QRNG Simulator GUI](screenshot.png) <!-- Add a screenshot if available -->

---

## Notes

- `tkinter` is included with most Python installations.
- For Arduino support, ensure your board outputs single-character `'0'` or `'1'` values over serial.
- The entropy plot helps visualize the randomness quality of your bitstreams.

---

## License

This project is for educational and research purposes.
