import requests
import re
import csv
import json
from tqdm import tqdm

import pickle
from genre.trie import Trie, MarisaTrie
from genre.fairseq_model import mGENRE

with open("../GENRE/data/lang_title2wikidataID-normalized_with_redirect.pkl", "rb") as f:
    lang_title2wikidataID = pickle.load(f)

with open("../GENRE/data/titles_lang_all105_marisa_trie_with_redirect.pkl", "rb") as f2:
    trie = pickle.load(f2)
    
model = mGENRE.from_pretrained("../GENRE/models/fairseq_multilingual_entity_disambiguation").eval()

with open("../data/sentences.csv", "r", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f, delimiter=",")
    data = list(dict_reader)

with open("../data/entities.csv", "r") as f:
    dict_reader = csv.DictReader(f, delimiter=",")
    ner_output = list(dict_reader)

output=[]

pbar = tqdm(total=len(data))
for item in data:
    entities = list()
    text=item["sentence"]
    data_id = item["id"]
    entities = []
    begin = []
    end = []
    labels = []
    sentences = []
    wb_ids = []
    scores = []
    surface_forms = [(int(ent["start_pos"]), int(ent["end_pos"]), ent["type"]) for ent in ner_output \
                     if ent["id"] == data_id]
    for ent in surface_forms:
        start_pos = ent[0]
        end_pos = ent[1]
        label = ent[2]
        mention = text[0:start_pos]+" [START] "+ text[start_pos:end_pos]+ " [END]"+text[end_pos:]
        begin.append(start_pos)
        end.append(end_pos)
        labels.append(label)
        sentences.append(mention)
    results = model.sample(
        sentences,
        prefix_allowed_tokens_fn=lambda batch_id, sent: [
            e for e in trie.get(sent.tolist()) if e < len(model.task.target_dictionary)
            ],
            text_to_id=lambda x: max(lang_title2wikidataID[tuple(reversed(x.split(" >> ")))], key=lambda y: int(y[1:])),
            marginalize=True,
        )
    
    for result in results:
        candidate = result[0]
        name = candidate["texts"][0]
        score = candidate["score"].item()
        wb_id = candidate["id"]
        entities.append(name)
        scores.append(score)
        wb_ids.append(wb_id)
    
    labels = list(zip(begin, end, labels, scores, entities, wb_ids))
    for start_pos, end_pos, label, score, alias, wb_ids in labels:
        output.append(
            {
                "id":item["id"],
                "start_pos":start_pos,
                "end_pos":end_pos,
                "type":label,
                "alias":alias,
                "wb_id":wb_ids,
                "score":score
            }
        )
    pbar.update(1)
pbar.close()

keys = output[0].keys()

a_file = open("results/mgenre_ed/output_nel.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(output)
a_file.close()