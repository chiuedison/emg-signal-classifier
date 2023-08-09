import numpy as np
from window_predictor import WindowPredictor
from window_producer import *


def get_rising_falling_slopes(window_arr):
    max_idx = np.argmax(window_arr)
    max_val = window_arr[max_idx]
    if max_idx == 0:
        min_rising_idx = 0
    else:
        min_rising_idx = np.argmin(window_arr[0:max_idx])
    min_rising_val = window_arr[min_rising_idx]
    if max_idx == len(window_arr) - 1:
        min_falling_idx = len(window_arr) - 1
    else:
        min_falling_idx = np.argmin(window_arr[max_idx:len(window_arr)])
    min_falling_val = window_arr[min_falling_idx]

    rising_x_diff = max_idx - min_rising_idx
    if rising_x_diff == 0:
        rising_slope = 0
    else:
        rising_slope = (max_val - min_rising_val) / rising_x_diff
    falling_x_diff = min_falling_idx - max_idx
    if falling_x_diff == 0:
        falling_slope = 0
    else:
        falling_slope = (min_falling_val - max_val) / falling_x_diff

    return rising_slope, falling_slope

class LinearSlopePredictor(WindowPredictor):

    def __init__(self):
        self.trained = False
        self.rising_slope_min = None
        self.falling_slope_max = None

    def train(self, windows, labels):
        window_count = len(windows)
        rising_slopes_true = np.zeros((window_count))
        falling_slopes_true = np.zeros((window_count))
        rising_slopes_false = np.zeros((window_count))
        falling_slopes_false = np.zeros((window_count))
        for idx in range(len(windows)):
            window_arr = windows[idx]
            rising_slope, falling_slope = get_rising_falling_slopes(window_arr)

            if labels[idx] == 1:
                rising_slopes_true[idx] = rising_slope
                falling_slopes_true[idx] = falling_slope
            elif labels[idx] == 0:
                rising_slopes_false[idx] = rising_slope
                falling_slopes_false[idx] = falling_slope

            idx += 1

        rising_slopes_true_avg = np.average(rising_slopes_true)
        falling_slopes_true_avg = np.average(falling_slopes_true)

        rising_slopes_false_avg = np.average(rising_slopes_false)
        falling_slopes_false_avg = np.average(falling_slopes_false)
        
        self.rising_slope_min = (rising_slopes_true_avg + rising_slopes_false_avg) / 2
        self.falling_slope_max = (falling_slopes_true_avg + falling_slopes_false_avg) / 2

        self.trained = True

    def label_window(self, window):
        rising_slope, falling_slope = get_rising_falling_slopes(window)
        return rising_slope >= self.rising_slope_min and \
                falling_slope <= self.falling_slope_max


if __name__ == "__main__":
    raw_data = pd.read_pickle("combined_data.pkl")
    raw_data = raw_data[raw_data['class'] != 0]
    raw_data.loc[raw_data['class'] != 2] = 0
    raw_data.loc[raw_data['class'] == 2] = 1
    raw_data = raw_data.rename(columns={
        "class": "y",
        "channel1": "x"
    })
    train_data = raw_data.head(1000000)
    x_windows, y_labels = raw_to_labeled_windows(train_data)
    linear_predictor = LinearSlopePredictor()
    linear_predictor.train(x_windows, y_labels)
    print(linear_predictor.rising_slope_min, linear_predictor.falling_slope_max)

    test_data = raw_data.tail(1000000)
    x_labels, y_labels = raw_to_labeled_windows(test_data)
    tp = fp = tn = fn = 0
    for i in range(len(x_labels)):
        pred = linear_predictor.label_window(x_labels[i])
        actual = y_labels[i]

        if pred and actual:
            tp += 1
        elif pred and not actual:
            fp += 1
        elif not pred and not actual:
            tn += 1
        elif not pred and actual:
            fn += 1
        else:
            print("Not right")
            exit(1)
    print(f"true positive: {tp}")
    print(f"false positive: {fp}")
    print(f"true negative: {tn}")
    print(f"false negative: {fn}")


