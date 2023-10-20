import requests
import spacy
import csv
import json
from tqdm import tqdm
from nltk.tokenize import sent_tokenize

with open("../data/sentences.csv", "r", encoding="utf-8") as f:
    data = csv.DictReader(f=f, delimiter=",")
    data = list(data)

nlp = spacy.load("en_core_web_trf")

vn_ids = {"create-26.4", 
"coloring-24", 
"build-26.1", 
"image_impression-25.1", 
"illustrate-25.3",
"carve-21.2", 
"characterize-29.2"}

URL = "http://localhost:8080/predict/semantics"

output = []
pbar=tqdm(total=len(data))
for row in data:
    text = row["sentence"]    
    sentences = [s for s in sent_tokenize(text)]
    sentence_len = 0
    for sentence in sentences:
        PARAMS = {'utterance':sentence}
        doc = nlp(sentence)
        try:
            r = requests.get(url = URL, params = PARAMS)
            response = r.json()
            for prop in response["props"]:
                for vn_id in vn_ids:
                    if prop["sense"].startswith(vn_id):
                        for span in prop["spans"]:
                            if len(span["vn"])>0 and span["vn"] in {"Product", "Theme", "Patient", "Result"}:
                                span_vb = span["text"]
                                span_start = doc[int(span["start"]):int(span["start"]+1)].start_char+sentence_len
                                doc2 = nlp(span_vb)
                                for ent in doc2.ents:
                                    start_pos = ent.start_char+span_start
                                    end_pos = ent.end_char+span_start
                                    surface = ent.text
                                    label = ent.label_
                                    output_dict = {
                                        "doc_id":row["id"],
                                        "surface":surface,
                                        "doc_start_pos":start_pos,
                                        "doc_end_pos":end_pos,
                                        "type":label
                                    }
                                    if label in {"PERSON", "WORK_OF_ART"}:
                                        output.append(output_dict)  
                                           
        except Exception as e:
            print(e)
        sentence_len=sentence_len+len(sentence)+1
    print(output)   
    pbar.update(1)

keys = output[0].keys()
a_file = open("../results/baseline_motifs/output.csv", "w", encoding="utf-8")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(output)
a_file.close()