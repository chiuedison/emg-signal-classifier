import numpy as np

# what happens when window size changes?
# add variable to handle it?


class WindowPredictor:

    def __init__(self):
        """
        Initialize variables/data structures that are
        set when the train function called
        """
        self.trained = False
    
    def train(self, windows, labels):
        """
        Arguments:
            windows: list of 1D numpy array of EMG values
            labels: list of labels for each window
        Return:
            nothing, just set variables
        """
        self.trained = True
        print("no train implementation")

    def label_window(self, window):
        """
        Arguments:
            window: 1D numpy array of EMG values
        Return:
            boolean of whether window is a flex or not
        """
        raise Exception("Implement label_window")
