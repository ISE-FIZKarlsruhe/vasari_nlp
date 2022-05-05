import csv

def eval_ed_exact(path_data, path_results, lang):
    with open(path_data+"entities_"+lang+".csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=";"))
    with open(path_results+"output_ed_"+lang+".csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = []
    fp = []

    for entity1, entity2 in zip(data, model_result):
        if entity1["exact"]=="1":
            if entity1["wb_id"]==entity2["wb_id"]:
                tp.append(entity1)
            else:
                fp.append({
                    "id":entity1["id"],
                    "start_pos":entity1["start_pos"],
                    "end_pos":entity1["end_pos"],
                    "surface":entity1["surface"],
                    "type":entity1["type"],
                    "true_id":entity1["wb_id"],
                    "output_id":entity2["wb_id"],
                    "output_wiki":entity2["alias"],
                    "score":entity2["score"],
                    "relation":None
                }
                )
            

    accuracy = len(tp)/(len(tp)+len(fp))
    with open(path_results+"result_e_"+lang+".txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("Accuracy: "+ str(accuracy)+ "\n\n")
    
    
    p_keys = tp[0].keys()
    n_keys = fp[0].keys()

    tp_file = open(path_results+"tp_e_"+lang+".csv", "w")
    dict_writer = csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(tp)
    tp_file.close()
    
    fp_file = open(path_results+"fp_e_"+lang+".csv", "w")
    dict_writer = csv.DictWriter(fp_file, n_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()



def eval_ed_exact_and_close(path_data, path_results, lang):
    with open(path_data+"entities_"+lang+".csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=";"))
    with open(path_results+"output_ed_"+lang+".csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = []
    fp = []

    for entity1, entity2 in zip(data, model_result):
        if entity1["exact"]=="1" or entity1["close"]=="1":
            if entity1["wb_id"]==entity2["wb_id"]:
                tp.append(entity1)
            else:
                fp.append({
                    "id":entity1["id"],
                    "start_pos":entity1["start_pos"],
                    "end_pos":entity1["end_pos"],
                    "surface":entity1["surface"],
                    "type":entity1["type"],
                    "true_id":entity1["wb_id"],
                    "output_id":entity2["wb_id"],
                    "output_wiki":entity2["alias"],
                    "score":entity2["score"],
                    "relation":None
                }
                )
            

    accuracy = len(tp)/(len(tp)+len(fp))
    with open(path_results+"result_e+c_"+lang+".txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("Accuracy: "+ str(accuracy)+ "\n\n")
    
    
    p_keys = tp[0].keys()
    n_keys = fp[0].keys()

    tp_file = open(path_results+"tp_e+c_"+lang+".csv", "w")
    dict_writer = csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(tp)
    tp_file.close()
    
    fp_file = open(path_results+"fp_e+c_"+lang+".csv", "w")
    dict_writer = csv.DictWriter(fp_file, n_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()


def eval_ed_no_oov(path_data, path_results, lang):
    with open(path_data+"entities_"+lang+".csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=";"))
    with open(path_results+"output_ed_"+lang+".csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = []
    fp = []

    for entity1, entity2 in zip(data, model_result):
        if entity1["wb_id"]!="OOV":
            if entity1["wb_id"]==entity2["wb_id"]:
                tp.append(entity1)
            else:
                fp.append({
                    "id":entity1["id"],
                    "start_pos":entity1["start_pos"],
                    "end_pos":entity1["end_pos"],
                    "surface":entity1["surface"],
                    "type":entity1["type"],
                    "true_id":entity1["wb_id"],
                    "output_id":entity2["wb_id"],
                    "output_wiki":entity2["alias"],
                    "score":entity2["score"],
                    "relation":None
                }
                )
            

    accuracy = len(tp)/(len(tp)+len(fp))
    with open(path_results+"result_"+lang+".txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("Accuracy: "+ str(accuracy)+ "\n\n")
    
    
    p_keys = tp[0].keys()
    n_keys = fp[0].keys()

    tp_file = open(path_results+"tp_"+lang+".csv", "w")
    dict_writer = csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(tp)
    tp_file.close()
    
    fp_file = open(path_results+"fp_"+lang+".csv", "w")
    dict_writer = csv.DictWriter(fp_file, n_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()



eval_ed_exact(path_data="../data/", path_results="../results/mgenre_ed/", lang="en")
eval_ed_exact_and_close(path_data="../data/", path_results="../results/mgenre_ed/", lang="en")
eval_ed_no_oov(path_data="../data/", path_results="../results/mgenre_ed/", lang="en")