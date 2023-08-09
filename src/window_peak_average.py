import numpy as np
import pandas as pd
from window_predictor import WindowPredictor
import math

def window_peak_val(window_array):
    #Determine the peak of the window
    peak_idx = np.argmax(window_array)
    peak_val = window_array[peak_idx]

    return peak_val

class Average_window_max_predictor(WindowPredictor):

    def __init__(self):
        super().__init__()
        self.peak = None
        self.peaks_flexing_avg = 0
        self.peaks_resting_avg = 0

    def train(self, windows, labels):
        window_count = len(windows)

        peaks_flexing = np.zeros((window_count))
        peaks_resting = np.zeros((window_count))

        for idx in range(len(windows)):
            window_arr = windows[idx]
            window_peak = window_peak_val(window_arr)

            if labels[idx] == 1:
                peaks_flexing[idx] = window_peak
            elif labels[idx] == 0:
                peaks_resting[idx] = window_peak

            idx += 1

        self.peaks_flexing_avg = np.average(peaks_flexing)
        self.peaks_resting_avg = np.average(peaks_resting)

        self.trained = True

    def label_window(self, window_arr):
        window_peak = window_peak_val(window_arr)
        
        flex_diff = abs(window_peak - self.peaks_flexing_avg)
        resting_diff = abs(window_peak - self.peaks_resting_avg)

        if(flex_diff < resting_diff):
            return 1

        return 0