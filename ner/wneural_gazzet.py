import csv
import re
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import marisa_trie
from flair.data import Sentence
from flair.models import SequenceTagger
import itertools


with open("../vasari-kg.github.io/extra/surfaces.csv", "r", encoding="utf-8") as f:
    surfaces = csv.DictReader(f=f, delimiter=",")
    set_of_surfaces = set([surface["surface"].lower() for surface in surfaces])

with open("../vasari-kg.github.io/data/sentences_en.csv", "r") as f:
    sentences = list(csv.DictReader(f=f, delimiter=","))

trie = marisa_trie.Trie(list(set_of_surfaces))
pos_tagger = SequenceTagger.load("flair/upos-multi")
tokenizer = AutoTokenizer.from_pretrained("Babelscape/wikineural-multilingual-ner")
ner_tagger = AutoModelForTokenClassification.from_pretrained("Babelscape/wikineural-multilingual-ner")
nlp = pipeline("ner", model=ner_tagger, tokenizer=tokenizer)


def filter_candidates(candidates):
    output = []
    jj_nn = "((ADJ|PRON)\s)?((NOUN|PROPN)\s?)+"
    post_mod = "(\s(NUM|DET\s(ADJ|NOUN)))?"
    prop_phrase = "(\sADP\s((ADJ|PRON)\s)?((NOUN|PROPN)\s?)+){0,2}$"
    for item in candidates:
        tags = " ".join([tag for tag in item["tags"] if tag != "PUNCT"])
        if re.match(jj_nn+post_mod+prop_phrase, tags):
            if len(output)==0:
                output.append(item)
            else:
                last_range = range(output[-1]["start_pos"], output[-1]["end_pos"])
                curr_range = range(item["start_pos"], item["end_pos"])
                if set(last_range).intersection(set(curr_range)):
                    if len(output[-1]["surface"])<len(item["surface"]):
                        output[-1]=item
                else:
                    output.append(item)
    return output


def get_entity_spans(sent_idx, sentence, pos_tagger):
    counter = 0
    candidates = []
    sentence = Sentence(sentence)
    pos_tagger.predict(sentence)
    while counter < len(sentence):
        idx = counter
        counter+=1
        candidate = None
        prefix = None
        for idx2 in range(idx, len(sentence)):
            if prefix == None and sentence[idx2].get_label("upos").value in {"DET", "PUNCT"}:
                break
            elif prefix == None:
                prefix = sentence[idx2].text.lower()
                start_pos = sentence[idx2].start_pos
                end_pos = sentence[idx2].end_pos
                tags = [sentence[idx2].get_label("upos").value]
            else:
                prefix += " "+sentence[idx2].text.lower()
                end_pos = sentence[idx2].end_pos
                tags.append(sentence[idx2].get_label("upos").value)
                
            matches = trie.keys(prefix)
            if len(matches)<1:
                if candidate!=None:
                    del candidate["tags"][-1]
                    candidates.append(candidate)
                break
            else:
                if prefix in matches:
                    candidate = {"id":sent_idx,"surface":prefix, "start_pos":start_pos, "end_pos":end_pos, "tags":tags}
                    if idx2 == len(sentence)-1:
                        candidates.append(candidate)
    candidates = filter_candidates(candidates)
    return candidates

ner_output = []
dict_candidates = []

pbar = tqdm(total=len(sentences))
for sample in sentences:
    sent_idx = sample["id"]
    text = sample["sentence"]
    ner = nlp(text, aggregation_strategy="simple")
    for ent in ner:
        if len(ner_output)==0:
            ner_output.append({
                "id":sent_idx,
                "start_pos":ent["start"],
                "end_pos":ent["end"],
                "surface":ent["word"],
                "type":ent["entity_group"],
            })
        elif ner_output[-1]["end_pos"]!=ent["start"]:
            ner_output.append({
                "id":sent_idx,
                "start_pos":ent["start"],
                "end_pos":ent["end"],
                "surface":ent["word"],
                "type":ent["entity_group"],
            })
        else:
            ner_output[-1] = {
                "id":sent_idx,
                "start_pos":ner_output[-1]["start_pos"],
                "end_pos":ent["end"],
                "surface":ner_output[-1]["surface"]+ent["word"].replace("#", ""),
                "type":ner_output[-1]["type"],
            }
    candidates = get_entity_spans(sent_idx, text, pos_tagger)
    dict_candidates.extend(candidates)
    pbar.update(1)
pbar.close()

dict_output = []


for item1 in dict_candidates:
    overlap = False
    range1 = range(item1["start_pos"], item1["end_pos"])
    for item2 in ner_output:
        range2 = range(item2["start_pos"], item2["end_pos"])
        if item1["id"]==item2["id"] and set(range1).intersection(set(range2)):
            overlap = True
    if overlap==False:
        dict_output.append({
            "id":item1["id"],
            "start_pos":item1["start_pos"],
            "end_pos":item1["end_pos"],
            "surface":item1["surface"],
            "type":"MISC"
            })
            

keys = ner_output[0].keys()
a_file = open("results/wikineural_dict/output.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(ner_output)
dict_writer.writerows(dict_output)
a_file.close()




  
