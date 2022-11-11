import sys
import argparse
import json
from collections import defaultdict
import csv
import requests

from tqdm import tqdm
from torch.utils.data import DataLoader, SequentialSampler, TensorDataset
import torch

### setup blink from github
sys.path.insert(0, '../blink_repo/')

from blink.biencoder.biencoder import BiEncoderRanker, load_biencoder
from blink.crossencoder.crossencoder import CrossEncoderRanker, load_crossencoder
from blink.biencoder.data_process import (
    process_mention_data,
    get_candidate_representation,
)
import blink.ner as NER
from blink.indexer.faiss_indexer import DenseFlatIndexer, DenseHNSWFlatIndexer


models_path = '../blink_repo/models/'

config = {
    "test_entities": None,
    "test_mentions": None,
    "interactive": False,
    "top_k": 10,
    "show_url": True,
    "biencoder_model": models_path + "biencoder_wiki_large.bin",
    "biencoder_config": models_path + "biencoder_wiki_large.json",
    "entity_catalogue": models_path + "entity.jsonl",
    "entity_encoding": models_path + "all_entities_large.t7",
    "crossencoder_model": models_path + "crossencoder_wiki_large.bin",
    "crossencoder_config": models_path + "crossencoder_wiki_large.json",
    "fast": False,  # set this to be true if speed is a concern
    "output_path": "../blink_repo/logs/"  # logging directory
}


# def _annotate(ner_model, input_sentences):
#     ner_output_data = ner_model.predict(input_sentences)
#     sentences = ner_output_data["sentences"]
#     mentions = ner_output_data["mentions"]
#     samples = []
#     for mention in mentions:
#         record = {}
#         record["label"] = "unknown"
#         record["label_id"] = -1
#         # LOWERCASE EVERYTHING !
#         record["context_left"] = sentences[mention["sent_idx"]][
#                                  : mention["start_pos"]
#                                  ].lower()
#         record["context_right"] = sentences[mention["sent_idx"]][
#                                   mention["end_pos"]:
#                                   ].lower()
#         record["mention"] = mention["text"].lower()
#         record["start_pos"] = int(mention["start_pos"])
#         record["end_pos"] = int(mention["end_pos"])
#         record["sent_idx"] = mention["sent_idx"]
#         samples.append(record)
#     return samples

def annotate2(data, ner_result):
    sentences = dict()
    samples = []
    for row in data:
        sentences[row["id"]]=row["sentence"]
    for mention in ner_result:
        sent_idx = mention["id"]
        record = {}
        record["label"] = "unknown"
        record["label_id"] = -1
        # LOWERCASE EVERYTHING !
        record["context_left"] = sentences[sent_idx][
                                 : int(mention["start_pos"])
                                 ].lower()
        record["context_right"] = sentences[sent_idx][
                                  int(mention["end_pos"]):
                                  ].lower()
        record["mention"] = mention["surface"].lower()
        record["start_pos"] = int(mention["start_pos"])
        record["end_pos"] = int(mention["end_pos"])
        record["sent_idx"] = sent_idx
        samples.append(record)
    return samples


def _load_candidates(
        entity_catalogue, entity_encoding, faiss_index=None, index_path=None, logger=None
):
    # only load candidate encoding if not using faiss index
    if faiss_index is None:
        candidate_encoding = torch.load(entity_encoding)
        indexer = None
    else:
        if logger:
            logger.info("Using faiss index to retrieve entities.")
        candidate_encoding = None
        assert index_path is not None, "Error! Empty indexer path."
        if faiss_index == "flat":
            indexer = DenseFlatIndexer(1)
        elif faiss_index == "hnsw":
            indexer = DenseHNSWFlatIndexer(1)
        else:
            raise ValueError("Error! Unsupported indexer type! Choose from flat,hnsw.")
        indexer.deserialize_from(index_path)

    # load all the 5903527 entities
    title2id = {}
    id2title = {}
    id2text = {}
    wikipedia_id2local_id = {}
    local_idx = 0
    with open(entity_catalogue, "r") as fin:
        lines = fin.readlines()
        for line in lines:
            entity = json.loads(line)

            if "idx" in entity:
                split = entity["idx"].split("curid=")
                if len(split) > 1:
                    wikipedia_id = int(split[-1].strip())
                else:
                    wikipedia_id = entity["idx"].strip()

                assert wikipedia_id not in wikipedia_id2local_id
                wikipedia_id2local_id[wikipedia_id] = local_idx

            title2id[entity["title"]] = local_idx
            id2title[local_idx] = entity["title"]
            id2text[local_idx] = entity["text"]
            local_idx += 1
    return (
        candidate_encoding,
        title2id,
        id2title,
        id2text,
        wikipedia_id2local_id,
        indexer,
    )


def _process_biencoder_dataloader(samples, tokenizer, biencoder_params):
    _, tensor_data = process_mention_data(
        samples,
        tokenizer,
        biencoder_params["max_context_length"],
        biencoder_params["max_cand_length"],
        silent=True,
        logger=None,
        debug=biencoder_params["debug"],
    )
    sampler = SequentialSampler(tensor_data)
    dataloader = DataLoader(
        tensor_data, sampler=sampler, batch_size=biencoder_params["eval_batch_size"]
    )
    return dataloader


def _run_biencoder(biencoder, dataloader, candidate_encoding, top_k=100, indexer=None):
    biencoder.model.eval()
    labels = []
    nns = []
    all_scores = []
    for batch in tqdm(dataloader):
        context_input, _, label_ids = batch
        with torch.no_grad():
            if indexer is not None:
                context_encoding = biencoder.encode_context(context_input).numpy()
                context_encoding = np.ascontiguousarray(context_encoding)
                scores, indicies = indexer.search_knn(context_encoding, top_k)
            else:
                scores = biencoder.score_candidate(
                    context_input, None, cand_encs=candidate_encoding  # .to(device)
                )
                scores, indicies = scores.topk(top_k)
                scores = scores.data.numpy()
                indicies = indicies.data.numpy()

        labels.extend(label_ids.data.numpy())
        nns.extend(indicies)
        all_scores.extend(scores)
    return labels, nns, all_scores




def load_models(args, logger=None):
    # load biencoder model
    if logger:
        logger.info("loading biencoder model")
    with open(args.biencoder_config) as json_file:
        biencoder_params = json.load(json_file)
        biencoder_params["path_to_model"] = args.biencoder_model
    biencoder = load_biencoder(biencoder_params)

    crossencoder = None
    crossencoder_params = None
    if not args.fast:
        # load crossencoder model
        if logger:
            logger.info("loading crossencoder model")
        with open(args.crossencoder_config) as json_file:
            crossencoder_params = json.load(json_file)
            crossencoder_params["path_to_model"] = args.crossencoder_model
        crossencoder = load_crossencoder(crossencoder_params)

    # load candidate entities
    if logger:
        logger.info("loading candidate entities")
    (
        candidate_encoding,
        title2id,
        id2title,
        id2text,
        wikipedia_id2local_id,
        faiss_indexer,
    ) = _load_candidates(
        args.entity_catalogue,
        args.entity_encoding,
        faiss_index=getattr(args, 'faiss_index', None),
        index_path=getattr(args, 'index_path', None),
        logger=logger,
    )

    return (
        biencoder,
        biencoder_params,
        crossencoder,
        crossencoder_params,
        candidate_encoding,
        title2id,
        id2title,
        id2text,
        wikipedia_id2local_id,
        faiss_indexer,
    )


def load_prerequisites(config):
    args = argparse.Namespace(**config)
    models = load_models(args)
    ner_model = NER.get_model()
    
    return ner_model, models,args

def get_wikidata(wikipage):
    response = requests.get(
        url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&sites=enwiki&titles="+wikipage
        )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return None
    else:
        response = response.json()
        wbitem = list(response["entities"].keys())[0]
        if wbitem == "-1":
            response = requests.get(
                url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&sites=enwiki&titles="+wikipage+"&normalize=1"
            )
            response = response.json()
            wbitem = list(response["entities"].keys())[0]
        return wbitem

def get_entities_from_sentences(data, ner_result, models,args):
    
    # annotate sentence first.
    samples = annotate2(data=data, ner_result=ner_result)
    biencoder, biencoder_params, crossencoder, crossencoder_params, candidate_encoding, title2id, id2title, id2text, wikipedia_id2local_id, faiss_indexer = models

    dataloader = _process_biencoder_dataloader(
        samples, biencoder.tokenizer, biencoder_params
    )

    top_k = args.top_k
    labels, nns, scores = _run_biencoder(
        biencoder, dataloader, candidate_encoding, top_k, faiss_indexer
    )

    id2url = {
        v: "https://en.wikipedia.org/wiki?curid=%s" % k
        for k, v in wikipedia_id2local_id.items()
    }
    output = []
    
    for entity_list, sample, score_list in zip(nns, samples, scores):
        sent_idx = sample['sent_idx']
        mention=sample['mention']
        start_pos = sample['start_pos']
        end_pos = sample['end_pos']
        e_id = entity_list[0]
        score = score_list[0]
        e_title = id2title[e_id]
        e_url = id2url[e_id]
        wb_id = get_wikidata(e_title)
        entity_dict ={
                    'id':sent_idx,
                    'start_pos':start_pos,
                    'end_pos':end_pos,
                    'surface':mention,
                    'entity':e_title, 
                    'wb_id':wb_id,
                    'score':score
                }
        output.append(entity_dict)
    return output

if __name__ == '__main__':
    ner_model, models, args = load_prerequisites(config)
    
    
    with open("../data/sentences.csv", "r", encoding="utf-8") as f1:
        data = csv.DictReader(f=f1, delimiter=",")
        data = list(data)
    
    with open("../data/entities.csv", "r") as f2:
        ner_result = csv.DictReader(f=f2, delimiter=",")
        ner_result = list(ner_result)

  
    output = get_entities_from_sentences(data, ner_result, models, args)
    keyz = output[0].keys()
    a_file = open("results/blink_ed/output_ed.csv", "w")
    dict_writer = csv.DictWriter(a_file, keyz)
    dict_writer.writeheader()
    dict_writer.writerows(output)
    a_file.close()
