import numpy as np
from scipy.signal import welch

class EEGAnalyzer:
    def __init__(self, fs=256, nperseg=256):
        self.fs = fs
        self.nperseg = nperseg

    def compute_power_spectrum(self, eeg_data):
        frequencies, power_spectrum = welch(eeg_data, fs=self.fs, nperseg=self.nperseg)
        return frequencies, power_spectrum

    def convert_to_db(self, power_spectrum):
        power_spectrum_db = 10 * np.log10(power_spectrum)
        return power_spectrum_db
