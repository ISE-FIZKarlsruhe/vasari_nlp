import csv

def eval_ner(path_data, path_model):
    with open(path_data+"works.csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=","))
    with open(path_model+"output.csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = []
    fp = []
    fn = []
    matches = []

    for entity1 in data:
        id1 = int(entity1["id"])
        fuzzy_start = entity1["start_pos"].split("|")
        fuzzy_end = entity1["end_pos"].split("|")
        fuzzy_surface = entity1["surface"].split("|")
        matched = None
        for start, end, surface in zip(fuzzy_start, fuzzy_end, fuzzy_surface):
            start_pos1 = int(start)
            end_pos1 = int(end)
            surface1 = set(surface.split(" "))
            for entity2 in model_result:
                id2 = int(entity2["doc_id"])
                start_pos2 = int(entity2["doc_start_pos"])
                end_pos2 = int(entity2["doc_end_pos"])
                surface2 = set(entity2["surface"].split(" "))
                if id2 == id1 and len(set(range(start_pos1, end_pos1)).intersection(set(range(start_pos2, end_pos2))))>0 \
                    and len(surface1.intersection(surface2))>0:
                    matched=True
                    tp.append(entity2)
        if matched==True:
            matches.append(entity1)
            
    for entity1 in data:
        if entity1 not in matches:
            fn.append(entity1)

    for entity2 in model_result:
        if entity2 not in tp:
            fp.append(entity2)

    precision = len(tp)/(len(tp)+len(fp))
    recall = len(tp)/(len(tp)+len(fn))
    f1 = (2*precision*recall)/(precision+recall)



    with open(path_model+"result.txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("False Negatives: "+str(len(fn))+"\n\n")
        output.write("Precision: "+ str(precision)+ "\n\n")
        output.write("Recall: "+ str(recall)+ "\n\n")
        output.write("F1: "+ str(f1)+"\n\n")
    
    
    p_keys = tp[0].keys()
    n_keys = fn[0].keys()

    tp_file = open(path_model+"tp_ner.csv", "w")
    dict_writer = csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(tp)
    tp_file.close()
    
    fp_file = open(path_model+"fp_ner.csv", "w")
    dict_writer = csv.DictWriter(fp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()

    fn_file = open(path_model+"fn_ner.csv", "w")
    dict_writer = csv.DictWriter(fn_file, n_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fn)
    fn_file.close()

eval_ner(path_data="../data/", path_model="../results/uniner_works/")



    

