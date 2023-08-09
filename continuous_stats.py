from datetime import datetime
import numpy as np


class Emg:
    def __init__(self):
        self.avg = 0
        self.num_points = 0
        self.std_dev = 0
        