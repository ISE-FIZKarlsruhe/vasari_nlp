import spacyopentapioca
import spacy
import csv

with open("../data/sentences.csv", "r") as f:
    dict_reader = csv.DictReader(f, delimiter=",")
    data = list(dict_reader)


output = []
nlp = spacy.blank("en")
nlp.add_pipe('opentapioca')

for item in data:
    text = item["sentence"]
    doc = nlp(text)
    for span in doc.ents:
        output.append(
            {
                "id":item["id"],
                "start_pos":span.start_char,
                "end_pos":span.end_char,
                "surface":text[span.start_char:span.end_char],
                "label":span.label_,
                "wb_id":span.kb_id_,
                "score":span._.score
            }
        )

keys = output[0].keys()
a_file = open("./results/opentapioca_el/output_nel.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(output)
a_file.close()