import json
import csv

import os
import pandas as pd

ent_files = []
coref_files = []
dates_files = []
works_files = []
motifs_files = []
sentences_files = []

rootdir = './'
for file in os.listdir("./"):
    if os.path.isdir(file):
        for csv_file in os.listdir("./"+file):
            if csv_file == "entities.csv":
                ent_files.append(os.path.join(file, csv_file))
            elif csv_file == "coref.csv":
                coref_files.append(os.path.join(file, csv_file))
            elif csv_file == "works.csv":
                works_files.append(os.path.join(file, csv_file))
            elif csv_file == "motifs.csv":
                motifs_files.append(os.path.join(file, csv_file))
            elif csv_file == "dates.csv":
                dates_files.append(os.path.join(file, csv_file))
            elif csv_file == "sentences.csv":
                sentences_files.append(os.path.join(file, csv_file))

        

ent_combined = pd.concat([pd.read_csv(f) for f in ent_files ], ignore_index=True)
coref_combined = pd.concat([pd.read_csv(f) for f in coref_files ], ignore_index=True)
dates_combined = pd.concat([pd.read_csv(f) for f in dates_files], ignore_index=True)
works_combined = pd.concat([pd.read_csv(f) for f in works_files ], ignore_index=True)
motifs_combined = pd.concat([pd.read_csv(f) for f in motifs_files ], ignore_index=True)
sentences_combined = pd.concat([pd.read_csv(f) for f in sentences_files ], ignore_index=True)
ent_combined.to_csv( "entities.csv", index=False)
coref_combined.to_csv( "coref.csv", index=False)
dates_combined.to_csv( "dates.csv", index=False)
works_combined.to_csv( "works.csv", index=False)
motifs_combined.to_csv( "motifs.csv", index=False)
sentences_combined.to_csv( "sentences.csv", index=False)
