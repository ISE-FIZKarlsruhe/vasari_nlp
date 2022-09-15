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
num_of_tokens = 0
pbar = tqdm(total=len(os.listdir("../chapters")))
for filename in os.listdir("../chapters"):
   with open(os.path.join("../chapters", filename), 'r') as f: 
    id = re.match("(life_of_.*?)\.html", filename).group(1)
    soup = BeautifulSoup(f)
    paragraphs = soup.find_all('p')
    paragraphs = [re.sub("\[Pg\s.*?\]", "", par.getText()) for par in paragraphs if len(par.getText())>0]
    full_text = "\n".join(paragraphs)
    sentences = punkt_en.tokenize(full_text)
    sentences = [re.sub("\-\n", "", sentence) for sentence in sentences]
    sentences = [re.sub("\n", " ", sentence) for sentence in sentences]
    num_of_tokens += sum([len(re.findall(r'\w+', sentence)) for sentence in sentences[:7]])
    output_coref[id]=[" ".join(sentences[:7])]
    # paragraph_max_ent = (None, 0)
    # for idx, paragraph in enumerate(paragraphs):
    #     entities = []
    #     sentences = punkt_en.tokenize(paragraph)
    #     sentences = [re.sub("\-\n", "", sentence) for sentence in sentences]
    #     sentences = [re.sub("\n", " ", sentence) for sentence in sentences]
    #     for sentence in sentences:
    #         ner = nlp(paragraph, aggregation_strategy="simple")
    #         entities.extend(ner)
    #     if len(entities)>=paragraph_max_ent[1]:
    #         paragraph_max_ent = (idx, len(entities))
    # paragraph = paragraphs[paragraph_max_ent[0]]
    # sentences = punkt_en.tokenize(paragraph)
    # sentences = [re.sub("\-\n", "", sentence) for sentence in sentences]
    # sentences = [re.sub("\n", " ", sentence) for sentence in sentences]
    # output_ner[id]=sentences
    pbar.update(1)
with open("test_coref.json", "w", encoding="utf-8") as fp:
    json.dump(output_coref, fp=fp, indent=4)

print("Num of tokens: "+ str(num_of_tokens))
print("Num of tokens per artist: "+str(num_of_tokens/27))


