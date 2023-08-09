# Accuracy of 1.000
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from get_raw_data import get_ring_dataset


# Read data from files
raw_df = get_ring_dataset()


"""
0 - unmarked data,
1 - hand at rest, 
2 - hand clenched in a fist, 
3 - wrist flexion,
4 – wrist extension,
5 – radial deviations,
6 - ulnar deviations,
7 - extended palm (the gesture was not performed by all subjects).
"""
# Getting just two classes (hand at rest and hand clenched in fist) from data
rest_and_clenched_df = raw_df
rest_and_clenched_df = rest_and_clenched_df.loc[(rest_and_clenched_df['class'] == 2) | (rest_and_clenched_df['class'] == 1)]

# Get class list
class_list = rest_and_clenched_df['class'].tolist()
# Get data list of lists
data_list = rest_and_clenched_df.drop(columns=['time', 'class'], axis=1).values.tolist()


# Split testing and training data
data_train, data_test, class_train, class_test = train_test_split(data_list, class_list, test_size=0.25, random_state=0)


# Train with SVM classifier
model = SVC(C = 1.0, kernel = 'rbf')
model.fit(data_train, class_train)
# Test model
prediction = model.predict(data_test)
print(prediction)
# Check results
cm = confusion_matrix(class_test, prediction)
TN, FP, FN, TP = cm.ravel()

print('True Positive(TP)  = ', TP)
print('False Positive(FP) = ', FP)
print('True Negative(TN)  = ', TN)
print('False Negative(FN) = ', FN)

accuracy =  (TP+TN) /(TP+FP+TN+FN)

print('Accuracy of the binary classification = {:0.3f}'.format(accuracy))
