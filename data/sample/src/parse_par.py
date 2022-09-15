from bs4 import BeautifulSoup
import re
import os
import nltk.data
import json
# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline
from tqdm import tqdm

# tokenizer = AutoTokenizer.from_pretrained("Babelscape/wikineural-multilingual-ner")
# tagger = AutoModelForTokenClassification.from_pretrained("Babelscape/wikineural-multilingual-ner")
# nlp = pipeline("ner", model=tagger, tokenizer=tokenizer)
punkt_en = nltk.data.load('tokenizers/punkt/english.pickle')
output_ner = {}
output_coref = {}
pbar = tqdm(total=len(os.listdir("../chapters")))
for filename in os.listdir("../chapters"):
   with open(os.path.join("../chapters", filename), 'r') as f: 
    id = re.match("(life_of_.*?)\.html", filename).group(1)
    soup = BeautifulSoup(f)
    paragraphs = soup.find_all('p')
    output_lst = []
    for par in paragraphs:
        par = re.sub("\[Pg\s.*?\]", "", par.getText())
        sentences = punkt_en.tokenize(par)
        sentences = [re.sub("\-\n", "", sentence) for sentence in sentences]
        sentences = [re.sub("\n", " ", sentence) for sentence in sentences]
        full_text = " ".join(sentences)
        num_of_tokens = len(re.findall(r'\w+', full_text))
        if num_of_tokens >= 100 and num_of_tokens <= 600:
            output_lst.append(full_text)
    output_coref[id]=output_lst
    pbar.update(1)
with open("test_par.json", "w") as fp:
    json.dump(output_coref, fp=fp, indent=4, ensure_ascii=False)


