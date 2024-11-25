"""
Calculates the average edit distance among all table cells.
"""

from calculateEditDistance import basepath, text_csvs_with_edit_distance, load_df_from_csv, get_csv_file_paths
import numpy as np

def get_average_edit_distance(df):
    return df['edit_distance'].mean(axis=0)

if __name__=="__main__":
    file_paths = get_csv_file_paths(basepath + "/" + text_csvs_with_edit_distance)
    averages = []
    for file_path in file_paths:
        df = load_df_from_csv(basepath + "/" + text_csvs_with_edit_distance + "/" + file_path, ["position", "text", "detected_text", "edit_distance"])
        print([get_average_edit_distance(df)])
        averages.append([get_average_edit_distance(df)])
    
    print("Average Edit Distance: " + str(np.mean(averages)))
