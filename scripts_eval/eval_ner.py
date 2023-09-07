import csv

def eval_ner(path_data, path_model):
    with open(path_data+"entities.csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=","))
    with open(path_model+"output.csv", "r") as f2:
        model_result = list(csv.DictReader(f2, delimiter=","))
    
    tp = [] #true positive
    fp = [] #false positive
    fn = [] #false negative
    matches = [] #matched annotations
    matched_sf=0

    for entity1 in data:
        id1 = int(entity1["id"])
        start_pos1 = int(entity1["start_pos"])
        end_pos1 = int(entity1["end_pos"])
        ent_type1 = entity1["type"]
        surface1 = set(entity1["surface"].split(" "))
        matched_sf_value = False
        for entity2 in model_result:
            id2 = int(entity2["doc_id"])
            start_pos2 = int(entity2["doc_start_pos"])
            end_pos2 = int(entity2["doc_end_pos"])
            ent_type2 = entity2["type"]
            surface2 = set(entity2["surface"].split(" "))
            if id2 == id1 and len(set(range(start_pos1,end_pos1)).intersection(set(range(start_pos2,end_pos2))))>0:
                if ent_type1==ent_type2 and len(surface1.intersection(surface2))>0:
                    matches.append(entity1)
                    tp.append(entity2)
                    break
                else:
                    matched_sf_value = True
        if matched_sf_value==True:
            matched_sf+=1
            
    for entity1 in data:
        if entity1 not in matches:
            fn.append(entity1)

    for entity2 in model_result:
        if entity2 not in tp:
            fp.append(entity2)

    precision = len(matches)/(len(matches)+len(fp))
    recall = len(matches)/(len(matches)+len(fn))
    f1 = (2*precision*recall)/(precision+recall)



    with open(path_model+"result.txt", "w") as output:
        output.write("True Positives: "+str(len(tp))+"\n\n")
        output.write("False Positives: "+str(len(fp))+"\n\n")
        output.write("False Negatives: "+str(len(fn))+"\n\n")
        output.write("Precision: "+ str(precision)+ "\n\n")
        output.write("Recall: "+ str(recall)+ "\n\n")
        output.write("F1: "+ str(f1)+"\n\n")
        output.write("Matched Sf: "+ str(matched_sf)+"\n\n")
    
    
    p_keys = matches[0].keys()
    n_keys = fn[0].keys()
    fp_keys = fp[0].keys()

    tp_file = open(path_model+"tp_ner.csv", "w")
    dict_writer= csv.DictWriter(tp_file, p_keys)
    dict_writer.writeheader()
    dict_writer.writerows(matches)
    tp_file.close()
    
    fp_file = open(path_model+"fp_ner.csv", "w")
    dict_writer = csv.DictWriter(fp_file, fp_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fp)
    fp_file.close()

    fn_file = open(path_model+"fn_ner.csv", "w")
    dict_writer = csv.DictWriter(fn_file, n_keys)
    dict_writer.writeheader()
    dict_writer.writerows(fn)
    fn_file.close()

eval_ner(path_data="../data/", path_model="../results/ontonotes/")
eval_ner(path_data="../data/", path_model="../results/flair_ner/")
eval_ner(path_data="../data/", path_model="../results/wikineural/")

# # Evaluation without nested entities


# def eval_ner_no_nest(path_data, path_model):
#     with open(path_data+"entities.csv", "r") as f1:
#         data = list(csv.DictReader(f1, delimiter=","))
#     with open(path_model+"output.csv", "r") as f2:
#         model_result = list(csv.DictReader(f2, delimiter=","))
    
#     tp = []
#     fp = []
#     fn = []
#     matches = []

#     for entity1 in data:
#         if entity1["is_nested"]!="True":
#             id1 = int(entity1["id"])
#             start_pos1 = int(entity1["start_pos"])
#             end_pos1 = int(entity1["end_pos"])
#             ent_type1 = entity1["type"]
#             surface1 = set(entity1["surface"].split(" "))
#             for entity2 in model_result:
#                 id2 = int(entity2["doc_id"])
#                 start_pos2 = int(entity2["doc_start_pos"])
#                 end_pos2 = int(entity2["doc_end_pos"])
#                 ent_type2 = entity2["type"]
#                 surface2 = set(entity2["surface"].split(" "))
#                 if id2 == id1 and len(set(range(start_pos1,end_pos1)).intersection(set(range(start_pos2,end_pos2))))>0 \
#                     and ent_type1==ent_type2 and len(surface1.intersection(surface2))>0:
#                     matches.append(entity1)
#                     tp.append(entity2)
#                     break

            
#         for entity1 in data:
#             if entity1 not in matches and entity1["is_nested"]!="True":
#                 fn.append(entity1)

#         for entity2 in model_result:
#             if entity2 not in tp:
#                 fp.append(entity2)

#         precision = len(matches)/(len(matches)+len(fp))
#         recall = len(matches)/(len(matches)+len(fn))
#         f1 = (2*precision*recall)/(precision+recall)


#         with open(path_model+"result_min.txt", "w") as output:
#             output.write("True Positives: "+str(len(tp))+"\n\n")
#             output.write("False Positives: "+str(len(fp))+"\n\n")
#             output.write("False Negatives: "+str(len(fn))+"\n\n")
#             output.write("Precision: "+ str(precision)+ "\n\n")
#             output.write("Recall: "+ str(recall)+ "\n\n")
#             output.write("F1: "+ str(f1)+"\n\n")
        
        
#         p_keys = matches[0].keys()
#         n_keys = fn[0].keys()
#         fp_keys = fp[0].keys()

#         tp_file = open(path_model+"tp_ner_min.csv", "w")
#         dict_writer= csv.DictWriter(tp_file, p_keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(matches)
#         tp_file.close()
        
#         fp_file = open(path_model+"fp_ner_min.csv", "w")
#         dict_writer = csv.DictWriter(fp_file, fp_keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(fp)
#         fp_file.close()

#         fn_file = open(path_model+"fn_ner_min.csv", "w")
#         dict_writer = csv.DictWriter(fn_file, n_keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(fn)
#         fn_file.close()



# eval_ner_no_nest(path_data="../data/", path_model="../results/ontonotes/")
# eval_ner_no_nest(path_data="../data/", path_model="../results/flair_ner/")

    

