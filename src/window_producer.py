import numpy as np
import pandas as pd
import math


def even_windows(window_size, data):
    """
    Arguments:
        window_size: int
        data: numpy array
    Return:
        list of numpy arrays of size window_size
    """
    data_len = len(data)
    window_count = math.floor(data_len / window_size)
    return np.array_split(data, window_count)


def window_by_labels(X, y, min_window_size=50, padding=10):
    """
    Arguments:
        X: 1D numpy array
        y: 1D numpy array
    Return:
        x_windows: list of numpy arrays (windows)
        y_labels: label for each window

    Labeling strategy:
        continuous series of true values 
        surrounded by negative values
    """
    x_windows = []
    y_labels = []
    X_len = len(X)
    idx = 0
    while idx < X_len:
        if y[idx] == 1:
            true_start = max(idx - padding, 0)
            while idx < X_len and y[idx] == 1:
                idx += 1
            true_end = min(idx + padding, X_len-1) 
            if true_end - true_start >= min_window_size:
                x_windows.append(X[true_start:true_end])
                y_labels.append(1)
        else:
            false_start = max(idx - padding, 0)
            while idx < X_len and y[idx] == 0:
                idx += 1
            false_end = min(idx + padding, X_len-1) 
            if false_end - false_start >= min_window_size:
                x_windows.append(X[false_start:false_end])
                y_labels.append(0)
    return x_windows, y_labels


def raw_to_labeled_windows(raw_df, min_window_size=50, padding=10):
    """
    Arguments:
        raw_df: pandas dataframe with columns x, y
    Return:
        X: list of 1D numpy arrays (windows)
        y: list of labels for each window in X
    """
    x_list = list(raw_df['x'])
    y_list = list(raw_df['y'])
    x_windows, y_labels = window_by_labels(x_list, y_list, min_window_size, padding)
    return x_windows, y_labels


if __name__=="__main__":
    exit(0)
