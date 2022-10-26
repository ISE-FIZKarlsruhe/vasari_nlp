import csv


def eval_ed(path_data, path_results):
    with open(path_data+"entities.csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=","))
    with open(path_results+"output_ed.csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = []
    fp = []
    fn = []
    matches = []

    for entity1 in data:
        id1 = int(entity1["id"])
        start_pos1 = int(entity1["start_pos"])
        end_pos1 = int(entity1["end_pos"])
        wb_id1 = entity1["value"]
        for entity2 in model_result:
            id2 = int(entity2["id"])
            start_pos2 = int(entity2["start_pos"])
            end_pos2 = int(entity2["end_pos"])
            wb_id2 = entity2["wb_id"]
            if id2 == id1 and start_pos1 == start_pos2 and end_pos1 == end_pos2 and wb_id2 in wb_id1:
                matches.append(entity1)
                tp.append(entity2)

    for entity1 in data:
        if entity1 not in matches:
            fn.append(entity1)

    for entity2 in model_result:
        if entity2 not in tp:
            fp.append(entity2)

    accuracy = len(tp)/(len(tp)+len(fp))

    with open(path_results+"result_nel.txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("False Negatives: "+str(len(fn))+"\n\n")
        output.write("Accuracy: "+ str(accuracy))
    
    
    p_keys = tp[0].keys()
    n_keys = fn[0].keys()

    tp_file = open(path_results+"tp_ed.csv", "w")
    dict_writer = csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(tp)
    tp_file.close()
    
    fp_file = open(path_results+"fp_ed.csv", "w")
    dict_writer = csv.DictWriter(fp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()

    fn_file = open(path_results+"fn_ed.csv", "w")
    dict_writer = csv.DictWriter(fn_file, n_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fn)
    fn_file.close()





eval_ed(path_data="../data/", path_results="../entity_linking/results/blink_ed/")



