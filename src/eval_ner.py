import csv

def eval_ner(path_data, path_model):
    with open(path_data+"entities_en.csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=";"))
    with open(path_model+"output_nel.csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = []
    fp = []
    fn = []
    matches = []

    for entity1 in data:
        id1 = int(entity1["id"])
        start_pos1 = int(entity1["start_pos"])
        end_pos1 = int(entity1["end_pos"])
        for entity2 in model_result:
            id2 = int(entity2["id"])
            start_pos2 = int(entity2["start_pos"])
            end_pos2 = int(entity2["end_pos"])
            if id2 == id1 and start_pos2==start_pos1 \
                and end_pos2 == end_pos1:
                matches.append(entity1)
                tp.append(entity2)
            
    for entity1 in data:
        if entity1 not in matches:
            fn.append(entity1)

    for entity2 in model_result:
        if entity2 not in tp:
            fp.append(entity2)

    precision = len(tp)/(len(tp)+len(fp))
    recall = len(tp)/(len(tp)+len(fn))
    f1 = (2*precision*recall)/(precision+recall)

    matched_types = 0
    for x1, x2 in zip(matches, tp):
        if x1["label"]==x2["label"]:
            matched_types += 1


    with open(path_model+"result_ner.txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("False Negatives: "+str(len(fn))+"\n\n")
        output.write("Precision: "+ str(precision)+ "\n\n")
        output.write("Recall: "+ str(recall)+ "\n\n")
        output.write("F1: "+ str(f1)+"\n\n")
        output.write(str(matched_types)+ " matched types out of "+ str(len(tp))+" true positives")
    
    
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

eval_ner(path_data="../data/", path_model="../results/mgenre_babel_en/")



    

