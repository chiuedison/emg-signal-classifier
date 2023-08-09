import pandas as pd
import os
import pickle

# Combine data from EMG_data_for_gestures-master into one dataframe
def get_ring_dataset():
    fileList = []
    personNum = ""
    # Iterate through numbers 1-36
    for i in range (1, 37):
        # If i is a single digit, add a 0 to the front
        if i < 10:
            personNum = "0" + str(i)
        # Otherwise just convert it to a string
        else:
            personNum = str(i)
        # Iterate through all the files in the directory
        smallList = os.listdir("EMG_data_for_gestures-master/" + personNum)
        for i in range(2):
            smallList[i] = "EMG_data_for_gestures-master/" + personNum + "/" + smallList[i]

    fileList.extend(smallList)
    # Create a dataframe from the list of files
    df_list = [pd.read_table(file) for file in fileList]
    raw_df = pd.concat(df_list)
    return raw_df

combined_data = get_ring_dataset()
combined_data.to_pickle("combined_data.pkl")
combined_data.to_csv("combined_data.csv")
