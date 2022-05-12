import csv
import re
import spacy
from nltk.corpus import stopwords
from tqdm import tqdm

with open("../data/entities_en.csv") as f1:
    data = list(csv.DictReader(f=f1, delimiter=";"))

with open("surfaces.csv") as f2:
    surfaces = list(csv.DictReader(f=f2, delimiter=","))


stop_words_eng = set(stopwords.words('english'))
stop_words_it = set(stopwords.words('italian'))
stop_words_it.update({"de", "d", "dei"})
nlp_en = spacy.load('en_core_web_sm')
nlp_it = spacy.load('it_core_news_sm')


def normalize_str(text, lang):
    no_number_string = re.sub(r'\d+','',text)
    no_romans_string = re.sub(r'\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b',"", no_number_string)
    no_parenthesis_string = re.sub(r'\(.*?\)', "", no_romans_string)
    no_parenthesis_string = re.sub(r'(Saint|St\.?|San|Sant\'?|Santo|Santa)[\s\b]', "S. ", no_parenthesis_string)
    lower_string = no_parenthesis_string.lower()
    no_punc_string = re.sub(r'[^\w\s]','', lower_string)
    no_wspace_string = no_punc_string.strip()
    if lang=="en":
        no_stpwords_string=""
        for i in no_wspace_string.split():
            if i not in stop_words_eng and len(i)>1:
                no_stpwords_string += i+' '
        no_stpwords_string = no_stpwords_string[:-1]   
        doc = nlp_en(no_stpwords_string)
        lemmatized_str = ""
        for token in doc:
            lemma = re.sub("s$", "", token.lemma_)
            lemmatized_str += lemma+" "

    if lang=="it":
        no_stpwords_string=""
        for i in no_wspace_string.split():
            if i not in stop_words_it and len(i)>1:
                no_stpwords_string += i+' '
        no_stpwords_string = no_stpwords_string[:-1]    
        doc = nlp_it(no_stpwords_string)
        lemmatized_str = ""
        for token in doc:
            lemmatized_str += token.lemma_+" "
    lemmatized_str = lemmatized_str[:-1]
    return lemmatized_str


output = []
pbar = tqdm(total=len(data))
for row1 in data:
    if row1["wb_id"] != "OOV":
        item_dict = {
            "id":row1["id"],
            "start_pos":row1["start_pos"],
            "end_pos":row1["end_pos"],
            "surface":row1["surface"],
            "wb_id":row1["wb_id"],
            "matched":False,
            "type":None,
            "kb-surface":None
        }
        for row2 in surfaces:
            if row2["id"]==row1["wb_id"] and row1["surface"].lower() == row2["surface"].lower():
                item_dict["matched"] = True
                type_key = [x for x in row2.keys() if row2[x]=="1"][0]
                item_dict["type"] = type_key
                break
        if item_dict["matched"]==False:
            for row2 in surfaces:
                lang = row2["lang"]
                if item_dict["matched"]!= True and row2["id"]==row1["wb_id"] \
                and normalize_str(row1["surface"], lang) == normalize_str(row2["surface"], lang):
                    item_dict["matched"] = True
                    type_key = [x for x in row2.keys() if row2[x]=="1"][0]
                    item_dict["type"] = type_key
                    item_dict["kb-surface"]= (row2["surface"], normalize_str(row2["surface"], lang))    
        output.append(item_dict)
    pbar.update(1)
pbar.close()

keys = output[0].keys()

a_file = open("entities_matched.csv", "w")
dict_writer = csv.DictWriter(a_file, keys)
dict_writer.writeheader()
dict_writer.writerows(output)
a_file.close()

                