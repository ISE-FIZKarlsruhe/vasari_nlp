import csv

def get_statistics(path, lang):
    with open(path+"entities_"+lang+".csv", "r", encoding="utf-8") as f:
        data = list(csv.DictReader(f, delimiter=","))
    f.close()

    entity_dict = {}
    labels_dict = {}
    sentences = 1
    id = 1
    named_entities = 0
    for item in data:
        print(item)
        if int(item["id"]) != id:
            sentences+=1
            id = int(item["id"])
        if int(item["named_entity"])==1:
            named_entities+=1
        
        if item["wb_id"] in entity_dict.keys():
            entity_dict[item["wb_id"]] += 1
        else:
            entity_dict[item["wb_id"]] = 1
        
        if item["type"] in labels_dict.keys():
            labels_dict[item["type"]] += 1
        else:
            labels_dict[item["type"]] = 1


    total_entities = len(data)
    avg_entities = total_entities/sentences
    max_value = max(entity_dict.values())
    max_entities = [k for k, v in entity_dict.items() if v==max_value]
    min_value = min(entity_dict.values())
    min_entities = [k for k, v in entity_dict.items() if v==min_value]
    avg_value = sum(entity_dict.values())/len(entity_dict.keys())

    with open(path+"stats_"+lang+".txt", "w") as f:
        f.write("Sentences: "+str(sentences)+"\n")
        f.write("Total entities in evaluation data: " + str(total_entities) +"\n")
        f.write("Average entities per sentence: "+ str(avg_entities)+"\n")
        f.write("Maximum occurrence of entity in data: "+ str(max_value)+"\n")
        f.write("Minimum occurrence of entity in data: "+ str(min_value)+"\n")
        f.write("Entities with maximum occurrence: "+ str(max_entities)+"\n")
        f.write("Entities with minimum occurrence: "+ str(len(min_entities))+"\n")
        f.write("Average occurrence per entity: " + str(avg_value)+"\n")
        f.write("Entities Out Of Vocabulary: "+str(entity_dict["OOV"])+"\n")
        f.write("Entities with type PER: " + str(labels_dict["PER"]) +"\n")   
        f.write("Entities with type ORG: "+  str(labels_dict["ORG"])+"\n")   
        f.write("Entities with type LOC: "+ str(labels_dict["LOC"])+"\n")
        f.write("Entities with type MISC: "+ str(labels_dict["MISC"])+"\n")
        f.write("Entities with type DATW: "+ str(labels_dict["DATE"])+"\n")
        f.write("Named entities are: "+ str(named_entities)+"\n")
    f.close()

get_statistics("../data/", "it") 