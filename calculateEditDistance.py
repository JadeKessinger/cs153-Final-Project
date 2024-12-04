"""
Calculates the edit distance between the text and detected text for each table cell. Saves the result to a csv.
"""

from Levenshtein import distance
import pandas as pd
import os
from recognizeCellText import basepath, text_csv_dir

text_csvs_with_edit_distance = "edit_distance_csvs"

def get_csv_file_paths(dir_path):
    return os.listdir(dir_path)

def load_df_from_csv(file_path, cols):
    return pd.read_csv(file_path, usecols=cols)

def distance_from_list(text):
    return distance(text[0], text[1])

def accuracy_from_edit_distance(stats):
    edit_distance = stats[0]
    text_length = stats[1]
    if text_length == 0:
        return 1 - edit_distance
    return 1 - edit_distance / text_length

def calculate_edit_distance(df):
    df.fillna("", inplace=True)
    df = df.astype(str)
    df['edit_distance'] = df[["text", "detected_text"]].apply(distance_from_list, axis = 1)
    return df

def calculate_text_length(df):
    df['text_length'] = df["text"].str.len()
    return df

def calculate_accuracy(df):
    df['accuracy'] = df[["edit_distance", "text_length"]].apply(accuracy_from_edit_distance, axis=1)
    return df

if __name__=="__main__":
    if not os.path.isdir(basepath + "/" + text_csvs_with_edit_distance):
        os.mkdir(basepath + "/" + text_csvs_with_edit_distance)
    
    csv_file_paths = get_csv_file_paths(basepath + "/" + text_csv_dir)
    for file_path in csv_file_paths:
        df = load_df_from_csv(basepath + "/" + text_csv_dir + "/" + file_path, ["position", "text", "detected_text"])
        df = calculate_edit_distance(df)
        df = calculate_text_length(df)
        df = calculate_accuracy(df)
        df.to_csv(basepath + "/" + text_csvs_with_edit_distance + "/" + file_path, encoding='utf-8', index=False)
