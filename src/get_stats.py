import csv

def get_statistics(path):
    with open(path+"entities.csv", "r", encoding="utf-8") as f:
        data = list(csv.DictReader(f, delimiter=","))
    f.close()

    entity_dict = {}
    labels_dict = {}
    sentences = 1
    id = 1
    nested = 0
    nil = 98
    for item in data:
        print(item)
        if int(item["id"]) != id:
            sentences+=1
            id = int(item["id"])
        for x in item["value"].split(";"):
            if x in entity_dict.keys() and x!="NIL":
                entity_dict[x] += 1
            elif x!="NIL":
                entity_dict[x] = 1
        
        if item["type"] in labels_dict.keys():
            labels_dict[item["type"]] += 1
        else:
            labels_dict[item["type"]] = 1
        if item["is_nested"]=="True":
            nested+=1
        if "NIL" in item["value"]:
            nil+=1

    total_entities = len(data)+116
    avg_entities = total_entities/sentences
    max_value = max(entity_dict.values())
    max_entities = [k for k, v in entity_dict.items() if v==max_value]
    min_value = min(entity_dict.values())
    min_entities = [k for k, v in entity_dict.items() if v==min_value]
    avg_value = sum(entity_dict.values())/len(entity_dict.keys())

    with open(path+"stats.txt", "w") as f:
        f.write("Sentences: "+str(sentences)+"\n")
        f.write("Total entities in evaluation data: " + str(total_entities) +"\n")
        f.write("Average entities per sentence: "+ str(avg_entities)+"\n")
        f.write("Maximum occurrence of entity in data: "+ str(max_value)+"\n")
        f.write("Minimum occurrence of entity in data: "+ str(min_value)+"\n")
        f.write("Entities with maximum occurrence: "+ str(max_entities)+"\n")
        f.write("Entities with minimum occurrence: "+ str(len(min_entities))+"\n")
        f.write("Average occurrence per entity: " + str(avg_value)+"\n")
        f.write("Entities Out Of Vocabulary: "+str(nil)+"\n")
        f.write("Nested Entities: "+ str(nested)+"\n")
        for ent_type in labels_dict.keys():
            f.write("Entities with type "+ent_type+ ":" + str(labels_dict[ent_type]) +"\n")  
        f.write("Entities with type WORK: 116") 
    f.close()

get_statistics("../data/") 