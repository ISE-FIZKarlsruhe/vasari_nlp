import json
import csv

import os
 
file = "verrocchio"
with open(file+'.jsonl', 'r', encoding="utf-8") as json_file:
    json_list = list(json_file)
    sent_dict = []
    coref_dict = []
    entities_dict = []
    time_dict = []
    motifs_dict = []
    works_dict = []

    for json_str in json_list:
        data = json.loads(json_str)
        sent_id = file+":"+str(data["id"])
        sentence = data["text"]
        sent_dict.append({
            "id":sent_id,
            "sentence":sentence
        })
        entities = data["label"]
        for item in entities:
            start_pos = item[0]
            end_pos = item[1]
            label = item[2]
            if label == "WORK":
                item_dict = {
                    "id":sent_id,
                    "start_pos":start_pos,
                    "end_pos":end_pos,
                    "surface":sentence[start_pos:end_pos],
                    "wikidata":None,
                    "zericatalog":None,
                    "arco":None
                }
                if item_dict not in works_dict:
                    works_dict.append(item_dict)
            elif label == "MOTIF":
                item_dict = {
                    "id":sent_id,
                    "start_pos":start_pos,
                    "end_pos":end_pos,
                    "surface":sentence[start_pos:end_pos],
                    "iconclass_ID":None
                }
                if item_dict not in motifs_dict:
                    motifs_dict.append(item_dict)
            elif label == "TIME":
                item_dict = {
                        "id":sent_id,
                        "type":None,
                        "start_pos":start_pos,
                        "end_pos":end_pos,
                        "surface":sentence[start_pos:end_pos],
                        "beginDate":None,
                        "end_date":None,
                        "value":None
                    }
                if item_dict not in time_dict:
                    time_dict.append(item_dict)
            else:
                if label == "PRON":
                    item_dict = {
                        "id":sent_id,
                        "type":"PRON",
                        "start_pos":start_pos,
                        "end_pos":end_pos,
                        "surface":sentence[start_pos:end_pos],
                        "coref_id":None
                    }
                    if item_dict not in coref_dict:
                        coref_dict.append(item_dict)
                else:
                    if "PRON" in json_str:
                        item_dict = {
                            "id":sent_id,
                            "type":"ENT",
                            "start_pos":start_pos,
                            "end_pos":end_pos,
                            "surface":sentence[start_pos:end_pos],
                            "coref_id":None
                        }
                        if item_dict not in coref_dict:
                            coref_dict.append(item_dict)
                    entity_dict = {
                        "id":sent_id,
                        "type":label,
                        "start_pos":start_pos,
                        "end_pos":end_pos,
                        "surface":sentence[start_pos:end_pos],
                        "wb_id":None,
                        "has_nested":None,
                        "is_nested":None
                    }
                    if entity_dict not in entities_dict:
                        entities_dict.append(entity_dict)

sent_keys = sent_dict[0].keys()
sent_file = open(file+"/sentences.csv", "w", encoding="utf-8")
dict_writer = csv.DictWriter(sent_file, sent_keys)
dict_writer.writeheader()
dict_writer.writerows(sent_dict)
sent_file.close()

coref_keys = coref_dict[0].keys()
coref_file = open(file+"/coref.csv", "w", encoding="utf-8")
dict_writer = csv.DictWriter(coref_file, coref_keys)
dict_writer.writeheader()
dict_writer.writerows(coref_dict)
coref_file.close()
try:
    time_keys = time_dict[0].keys()
    time_file = open(file+"/dates.csv", "w", encoding="utf-8")
    dict_writer = csv.DictWriter(time_file, time_keys)
    dict_writer.writeheader()
    dict_writer.writerows(time_dict)
    time_file.close()
except:
    None
# try:
#     motifs_keys = motifs_dict[0].keys()
#     motifs_file = open(file+"/motifs.csv", "w", encoding="utf-8")
#     dict_writer = csv.DictWriter(motifs_file, motifs_keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(motifs_dict)
#     motifs_file.close()
# except: 
#     None
# try:
#     works_keys = works_dict[0].keys()
#     works_file = open(file+"/works.csv", "w", encoding="utf-8")
#     dict_writer = csv.DictWriter(works_file, works_keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(works_dict)
#     works_file.close()
# except:
#     None
entities_keys = entities_dict[0].keys()
entities_file = open(file+"/entities.csv", "w", encoding="utf-8")
dict_writer = csv.DictWriter(entities_file, entities_keys)
dict_writer.writeheader()
dict_writer.writerows(entities_dict)
entities_file.close()