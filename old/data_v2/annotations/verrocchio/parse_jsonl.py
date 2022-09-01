import json
import csv

with open('life_of_agostino_and_agnolo_of_siena.jsonl', 'r') as json_file:
    json_list = list(json_file)

sent_dict = []
coref_dict = []
entities_dict = []
time_dict = []
motifs_dict = []
works_dict = []

for json_str in json_list:
    data = json.loads(json_str)
    sent_id = data["id"]
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
            works_dict.append({
                "id":sent_id,
                "start_pos":start_pos,
                "end_pos":end_pos,
                "surface":sentence[start_pos:end_pos],
                "KB":None,
                "KB_id":None
            })
        elif label == "MOTIF":
            motifs_dict.append({
                "id":sent_id,
                "start_pos":start_pos,
                "end_pos":end_pos,
                "surface":sentence[start_pos:end_pos],
                "iconclass_ID":None
            })
        elif label == "TIME":
            time_dict.append({
                    "id":sent_id,
                    "type":None,
                    "start_pos":start_pos,
                    "end_pos":end_pos,
                    "surface":sentence[start_pos:end_pos],
                    "beginDate":None,
                    "end_date":None,
                    "value":None
                })
        else:
            if label == "PRON":
                coref_dict.append({
                    "id":sent_id,
                    "type":"PRON",
                    "start_pos":start_pos,
                    "end_pos":end_pos,
                    "surface":sentence[start_pos:end_pos],
                    "coref_id":None
                })
            else:
                coref_dict.append({
                    "id":sent_id,
                    "type":"ENT",
                    "start_pos":start_pos,
                    "end_pos":end_pos,
                    "surface":sentence[start_pos:end_pos],
                    "coref_id":None
                })
                entities_dict.append({
                    "id":sent_id,
                    "type":label,
                    "start_pos":start_pos,
                    "end_pos":end_pos,
                    "surface":sentence[start_pos:end_pos],
                    "wb_id":None,
                    "has_nested":None,
                    "is_nested":None
                })

sent_keys = sent_dict[0].keys()
sent_file = open("sent.csv", "w")
dict_writer = csv.DictWriter(sent_file, sent_keys)
dict_writer.writerows(sent_dict)
sent_file.close()

coref_keys = coref_dict[0].keys()
coref_file = open("coref.csv", "w")
dict_writer = csv.DictWriter(coref_file, coref_keys)
dict_writer.writeheader()
dict_writer.writerows(coref_dict)
coref_file.close()

time_keys = time_dict[0].keys()
time_file = open("time.csv", "w")
dict_writer = csv.DictWriter(time_file, time_keys)
dict_writer.writeheader()
dict_writer.writerows(time_dict)
time_file.close()

motifs_keys = motifs_dict[0].keys()
motifs_file = open("motifs.csv", "w")
dict_writer = csv.DictWriter(motifs_file, motifs_keys)
dict_writer.writeheader()
dict_writer.writerows(motifs_dict)
motifs_file.close()
    
works_keys = works_dict[0].keys()
works_file = open("works.csv", "w")
dict_writer = csv.DictWriter(works_file, works_keys)
dict_writer.writeheader()
dict_writer.writerows(works_dict)
works_file.close()

entities_keys = entities_dict[0].keys()
entities_file = open("entities.csv", "w")
dict_writer = csv.DictWriter(entities_file, entities_keys)
dict_writer.writeheader()
dict_writer.writerows(entities_dict)
entities_file.close()