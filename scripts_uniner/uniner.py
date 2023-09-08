from langchain import HuggingFacePipeline, PromptTemplate,  LLMChain
from transformers import AutoTokenizer, AutoModelForCausalLM
from nltk.tokenize import sent_tokenize
import transformers
import torch
from torch.nn import DataParallel
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import csv
import ast
import re
from tqdm import tqdm

device_ids = [0, 1]


model = "Universal-NER/UniNER-7B-all"

tokenizer = AutoTokenizer.from_pretrained(model)

# Initialize the model on multiple GPUs
model = AutoModelForCausalLM.from_pretrained(model)
model = DataParallel(model, device_ids=device_ids)  # Parallelize the model
model = model.to(device_ids[0])  # Move the model to the first GPU

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",  # task
    model=model.module,  # Use model.module when using DataParallel
    tokenizer=tokenizer,
    trust_remote_code=True,
    device_map=device_ids,
    torch_dtype=torch.bfloat16,
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)


llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0, 'batch_size': 1})

template = """
              A virtual assistant answers questions from a user based on the provided text.
              USER: Text: {input_text}
              ASSISTANT: I’ve read this text.
              USER: What describes {entity_type} in the text?
              ASSISTANT:
           """

prompt = PromptTemplate(template=template, input_variables=["input_text","entity_type"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

with open("../data/sentences.csv", "r", encoding="utf-8") as f:
    data = csv.DictReader(f, delimiter=",")
    data = list(data)

entity_types = {"Artwork"}
pbar = tqdm(total=len(data))
for sample in data:
    output = []
    text = sample["sentence"]
    doc_id = sample["id"]
    sentences = [s for s in sent_tokenize(text)]
    curr_pos = 0
    for sentence_id, sentence in enumerate(sentences):
        for _type in entity_types:
            # example result = "['Madonna', 'S. Cosimo', 'Annunciation']"
            result_string = llm_chain.run({"input_text":sentence,"entity_type":_type})
            result_lst = ast.literal_eval(result_string)
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
    keys = output[0].keys()
    a_file = open("../results/uniner/output_+"+doc_id+".csv", "w", encoding="utf-8")
    dict_writer = csv.DictWriter(a_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(output)
    a_file.close()
    pbar.update(1)
pbar.close()




