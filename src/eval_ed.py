import csv

def eval_nel(path_data, path_results):
    with open(path_data+"entities_en.csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=";"))
    with open(path_results+"output_ed.csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = []
    fp = []
    matches = []

    for entity1, entity2 in zip(data, model_result):
        if entity1["wb_id"]==entity2["wb_id"]:
            tp.append(entity1)
        else:
            fp.append(entity1)
            

    accuracy = tp/(tp+fp)
    non_exact_mappings = [ent for ent in fp if ent["exact"]!="1"]
    with open(path_results+"result.txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("Accuracy: "+ str(accuracy)+ "\n\n")
        output.write("Non-exact errors: "+str(len(non_exact_mappings))+ "\n\n")
    
    
    p_keys = tp[0].keys()
    n_keys = fp[0].keys()

    tp_file = open(path_results+"tp.csv", "w")
    dict_writer = csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(tp)
    tp_file.close()
    
    fp_file = open(path_results+"fp.csv", "w")
    dict_writer = csv.DictWriter(fp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()



eval_nel(path_data="../data/", path_results="../results/mgenre_ed/")