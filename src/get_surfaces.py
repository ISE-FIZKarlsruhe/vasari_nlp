import re, requests
from tqdm import tqdm
import csv
from nltk.corpus import stopwords

def get_surface(ids, langs):
    output = []
    pbar = tqdm(total=len(ids))
    stop_words_eng = set(stopwords.words('english'))
    stop_words_it = set(stopwords.words('italian')) 

    for id in ids:
        for lang in langs:
            labels = set()
            WData_Api = "https://www.wikidata.org/w/api.php"
            r_labels = requests.get(WData_Api,
                            params = {'action': 'wbgetentities', 'props': 'labels|aliases', 'ids':id, 'format':'json', 'languages':lang}).json()
            label = r_labels["entities"][id]["labels"].get(lang, None)

            if label != None:
                labels.add(label["value"])
            aliases = r_labels["entities"][id]["aliases"].get(lang, None)
            if aliases != None:
                for alias in aliases:
                    labels.add(alias["value"])

            #get page title
            title = None
            r_titles = requests.get(WData_Api,
                            params = {'action': 'wbgetentities', 'props': 'sitelinks', 'ids':id, 'format':'json'}).json()
            title = r_titles["entities"][id]["sitelinks"].get(lang+"wiki", None)
            redirects = set()
            disambig_pages = set()
            anchor_texts = set()
            if title != None:
                title = title["title"]

                #get redirect links
                Wpedia_Api = "https://"+lang+".wikipedia.org/w/api.php"
                r_redirects = requests.get(Wpedia_Api,
                                params = {'action': 'query', 
                                'prop': 'redirects', 
                                'titles':title, 
                                'format':'json', 
                                'rdlimit':500}).json()
                
                page_id = list(r_redirects["query"]["pages"].keys())[0]
                redirects_lst = r_redirects["query"]["pages"][page_id].get("redirects", None)
                if redirects_lst:
                    for item in redirects_lst:
                        if len(item["title"]) > 1 and "list of" not in item["title"].lower():
                            redirects.add(item["title"])

                #get external pages
                ext_pages = set()
                r_linkshere = requests.get(Wpedia_Api, params = {
                                "action": "query",
                                "titles": title,
                                "prop": "linkshere",
                                "format": "json",
                                "lhlimit":500
                                }).json()

                ext_pages_lst = r_linkshere["query"]["pages"][page_id].get("linkshere", None)
                if ext_pages_lst:
                    for item in ext_pages_lst:
                        ext_pages.add(item["title"])
                    if "(disambiguation)" in item["title"] or "(disambiguazione)" in item["title"]:
                        disambig_pages.add(item["title"])

                links = list()
                links.append(title)
                links.extend(redirects)
                links = [re.escape(x) for x in links]
                for page in ext_pages:
                    r_wikitext = requests.get(Wpedia_Api,
                                    params = {
                                    "action": "parse",
                                    "page": page,
                                    "prop": "wikitext",
                                    "format": "json"
                                    }).json()
                    try:
                        wikitext = r_wikitext["parse"]["wikitext"]["*"]
                        capt_groups = re.findall("\[\[("+"|".join(links)+")\|(.*?)\]\]", wikitext)
                        for group in capt_groups:
                            a_t = group[-1]
                            if a_t not in stop_words_eng and a_t not in stop_words_it and len(a_t) > 1: 
                                a_t = re.sub(r'<.*?>', "", a_t)
                                anchor_texts.add(a_t)
                    except KeyError:
                        print(r_wikitext)
                        continue
                
            if title != None:
                output.append(
                    {"id":id,
                    "lang":lang,
                    "surface":title,
                    "title":1,
                    "label":None,
                    "redirect":None,
                    "disambiguation":None,
                    "anchor_text":None
                    }
                )
            for item in labels:
                if item != title:
                    output.append(
                        {
                            "id":id,
                            "lang":lang,
                            "surface":item,
                            "title":None,
                            "label":1,
                            "redirect":None,
                            "disambiguation":None,
                            "anchor_text":None
                        }
                    )
            for item in redirects:
                if item not in labels and item != title:
                    output.append(
                        {
                            "id":id,
                            "lang":lang,
                            "surface":item,
                            "title":None,
                            "label":None,
                            "redirect":1,
                            "disambiguation":None,
                            "anchor_text":None
                        }
                    )
            for item in disambig_pages:
                if item not in labels and item != title and item not in redirects:
                    output.append(
                        {
                            "id":id,
                            "lang":lang,
                            "surface":item,
                            "title":None,
                            "label":None,
                            "redirect":None,
                            "disambiguation":1,
                            "anchor_text":None
                        }
                    )
            for item in anchor_texts:
                if item not in labels and item != title and item not in redirects:
                    output.append(
                        {
                            "id":id,
                            "lang":lang,
                            "surface":item,
                            "title":None,
                            "label":None,
                            "redirect":None,
                            "disambiguation":None,
                            "anchor_text":1
                        }
                    )
        pbar.update(1)
    pbar.close()        
    keys = output[0].keys()

    a_file = open("test.csv", "w")
    dict_writer = csv.DictWriter(a_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(output)
    a_file.close()

with open("../data/entities_en.csv", "r") as f:
    data = csv.DictReader(f=f, delimiter=",")
    data1 = list(data)

with open("../data/entities_it.csv", "r") as f:
    data = csv.DictReader(f=f, delimiter=";")
    data2 = list(data)

ids1 = set([row["wb_id"] for row in data1 if row["wb_id"]!="OOV"])
ids2 = set([row["wb_id"] for row in data2 if row["wb_id"]!="OOV"])
ids1.update(ids2)
get_surface(ids=ids1, langs=["en", "it"])
