"""
Calculates the average edit distance among all table cells.
"""

from calculateEditDistance import basepath, text_csvs_with_edit_distance, load_df_from_csv, get_csv_file_paths
import numpy as np

def get_average_text_length(df):
    return df['text_length'].mean(axis=0)

def get_average_edit_distance(df):
    return df['edit_distance'].mean(axis=0)

def get_accuracy(df):
    return df['accuracy'].mean(axis=0)

if __name__=="__main__":
    file_paths = get_csv_file_paths(basepath + "/" + text_csvs_with_edit_distance)
    edit_distances = []
    lengths = []
    accuracies = []
    for file_path in file_paths:
        df = load_df_from_csv(basepath + "/" + text_csvs_with_edit_distance + "/" + file_path, ["position", "text", "detected_text", "edit_distance", "text_length", "accuracy"])
        edit_distances.append([get_average_edit_distance(df)])
        lengths.append([get_average_text_length(df)])

        accuracy = get_accuracy(df)
        accuracies.append(accuracy)
    
    print("Average edit distance: " + str(np.mean(edit_distances)))
    print("Average text length: " + str(np.mean(lengths)))
    print("Average accuracy: " + str(np.mean(accuracies)))
    print("Median accuracy: " + str(np.median(accuracies)))
    print("Minimum Accuracy: " + str(np.min(accuracies)))
    print("Images with accuracies < 0: " + str(len(list(filter(lambda x: x < 0, accuracies)))))
    print("Total images: " + str(len(accuracies)))
