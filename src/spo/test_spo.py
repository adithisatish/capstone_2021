# Dataset obtained from https://github.com/ytsvetko/metaphor/tree/master/input

from SPODetector import SPO
import pandas as pd 
import numpy as np
from sklearn.metrics import accuracy_score
import os

path = "\\".join(os.getcwd().split("\\")[:-2] + ['data'])
data = pd.read_csv(os.path.join(path, "svo.csv"))
print(data.head())
paragraph = 1