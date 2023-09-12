from langchain import HuggingFacePipeline
from langchain import PromptTemplate,  LLMChain
from transformers import AutoTokenizer, AutoModelForCausalLM
from nltk.tokenize import sent_tokenize
import transformers
from torch import cuda, bfloat16
import torch
import csv
import re
import json
from tqdm import tqdm
import time

model_name = "Universal-NER/UniNER-7B-all"

device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

model = transformers.AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    quantization_config=bnb_config,
    device_map='auto'
)
model.eval()
print(f"Model loaded on {device}")

tokenizer = AutoTokenizer.from_pretrained(model_name)

pipeline = transformers.pipeline(
    "text-generation", #task
    model=model,
    tokenizer=tokenizer,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,

)

llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0, "batch_size":1})

template = """
              A virtual assistant answers questions from a user based on the provided text.
              USER: Text: {input_text}
              ASSISTANT: I’ve read this text.
              USER: What describes {entity_type} in the text?
              ASSISTANT:
           """

prompt = PromptTemplate(template=template, input_variables=["input_text","entity_type"])

with open("../data/sentences.csv", "r", encoding="utf-8") as f:
    data = csv.DictReader(f, delimiter=",")
    data = list(data)

entity_types = {"Artwork"}
pbar = tqdm(total=len(data))


for sample in data:
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    output = []
    text = sample["sentence"] # document with multiple sentences
    doc_id = sample["id"] # document id
    sentences = [s for s in sent_tokenize(text)] # document parsed into sentences
    curr_pos = 0 # position of character in document
    for sentence_id, sentence in enumerate(sentences): # (sentence_id, sentence)
        for _type in entity_types: # set of entity types
            result_string = llm_chain.run({"input_text":sentence,"entity_type":_type})
            if result_string:
                result_lst = json.loads(result_string)
                counter = 0
                for ent in result_lst:
                    matches = re.finditer(ent, sentence)
                    spans = [(match.start(), match.end()) for match in matches]
                    for span in spans:
                        if span[0]>=counter:
                            output.append({
                                "doc_id":doc_id,
                                "sent_id":sentence_id,
                                "doc_start_pos":curr_pos+span[0],
                                "doc_end_pos":curr_pos+span[1],
                                "sent_start_pos":span[0],
                                "sent_end_pos":span[1],
                                "surface":sentence[span[0]:span[1]],
                                "type":_type
                            })
                            counter=span[0]
                            break
        curr_pos=curr_pos+len(sentence)+1
    pbar.update(1)
    if len(output)>0:
        keys = output[0].keys()
        a_file = open("../results/uniner_subj/output_"+doc_id+".csv", "w", encoding="utf-8")
        dict_writer = csv.DictWriter(a_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(output)
        a_file.close()
        


