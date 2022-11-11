import requests
import csv

with open("../data/entities.csv", "r") as f:
    dict_reader = csv.DictReader(f, delimiter=",")
    ground_truth = list(dict_reader)

with open("../data/sentences.csv", "r") as f:
    dict_reader = csv.DictReader(f, delimiter=",")
    data = list(dict_reader)


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

API_URL = "https://rel.cs.ru.nl/api"
output = []

for item in data:
    entities = list()
    text=item["sentence"]
    data_id = item["id"]
    entities = []
    start_positions = []
    end_positions = []
    labels = []
    sentences = []
    wb_ids = []
    scores = []
    surface_forms = [(int(ent["start_pos"]), int(ent["end_pos"]), ent["type"]) for ent in ground_truth \
                     if ent["id"] == data_id]
    for ent in surface_forms:
        start_pos = ent[0]
        end_pos = ent[1]
        result = requests.post(API_URL, json={
            "text": text,
            "spans": [start_pos, end_pos]
        })
        result.raise_for_status()  # raises exception when not a 2xx response
        if result.status_code != 204:
            result = result.json()
            if len(result) > 0:
                for entry in result:
                    print(entry)