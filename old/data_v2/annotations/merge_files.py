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
        ent_files.append(file+"/entities.csv")
        coref_files.append(file+"/coref.csv")
        works_files.append(file+"/works.csv")
        motifs_files.append(file+"/motifs.csv")
        dates_files.append(file+"/dates.csv")
        sentences_files.append(file+"/sentences.csv")

ent_combined = pd.concat([pd.read_csv(f) for f in ent_files ], ignore_index=True)
coref_combined = pd.concat([pd.read_csv(f) for f in coref_files ], ignore_index=True)
dates_combined = pd.concat([pd.read_csv(f) for f in dates_files ], ignore_index=True)
works_combined = pd.concat([pd.read_csv(f) for f in works_files ], ignore_index=True)
motifs_combined = pd.concat([pd.read_csv(f) for f in motifs_files ], ignore_index=True)
sentences_combined = pd.concat([pd.read_csv(f) for f in sentences_files ], ignore_index=True)
ent_combined.to_csv( "entities.csv", index=False)
coref_combined.to_csv( "coref.csv", index=False)
dates_combined.to_csv( "dates.csv", index=False)
works_combined.to_csv( "works.csv", index=False)
motifs_combined.to_csv( "motifs.csv", index=False)
sentences_combined.to_csv( "sentences.csv", index=False)
