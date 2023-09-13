import pandas as pd
import os

combined_df = pd.DataFrame()
folder_path = '../results/uniner_subj/5'  # Change this to your folder path

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        combined_df = combined_df.append(df, ignore_index=True)

combined_df.to_csv(folder_path+'/output.csv', index=False)