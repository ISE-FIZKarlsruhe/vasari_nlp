import csv
import matplotlib.pyplot as plt
import numpy as np

def compute_match(type, entity1, entity2):
    start_pos1 = int(entity1["start_pos"])
    end_pos1 = int(entity1["end_pos"])
    start_pos2 = int(entity2["start_pos"])
    end_pos2 = int(entity2["end_pos"])
    if type == "exact":
        if start_pos1==start_pos2 and end_pos1==end_pos2:
            return True
        else:
            return False
    if type == "relaxed":
        if start_pos1 <= start_pos2 and end_pos1 >= end_pos2:
            return True
        elif len(set(range(start_pos1,end_pos1)).intersection(set(range(start_pos2,end_pos2))))>0:
            return True
        else:
            return False


def eval_nel_threshold(path_data, path_results, threshold):
    with open(path_data+"entities.csv", "r") as f1:
        data = list(csv.DictReader(f1, delimiter=","))
    with open(path_results+"output_ed.csv", "r", encoding="utf-8") as f2:
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
            if float(entity2["score"])>=threshold:
                id2 = int(entity2["id"])
                start_pos2 = int(entity2["start_pos"])
                end_pos2 = int(entity2["end_pos"])
                wb_id2 = entity2["wb_id"]
                if id2 == id1 and compute_match(type="relaxed", entity1=entity1, entity2=entity2)==True and wb_id1==wb_id2:
                    matches.append(entity1)
                    tp.append(entity2)

    for entity1 in data:
        if entity1 not in matches:
            fn.append(entity1)

    for entity2 in model_result:
        if entity2 not in tp and float(entity2["score"])>=threshold:
            fp.append(entity2)
    if len(tp)>0 or len(fp)>0:
        precision = len(tp)/(len(tp)+len(fp))
        recall = len(tp)/(len(tp)+len(fn))
        f1 = (2*precision*recall)/(precision+recall)
        return precision, recall, f1
    else:
        return None, None, None 
    
    
start = -2.8
stop = -0.05
step = 0.05

precision_scores = []
recall_scores = []
f1_scores = []
for threshold in np.arange(start, stop, step):
    print("executing")
    precision, recall, f1 = eval_nel_threshold("../data/", "../entity_linking/results/mgenre_ed/", threshold)
    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)
    print(threshold, precision, f1)

#create precision recall curve
fig, ax = plt.subplots()
ax.plot(recall_scores, precision_scores, color='purple')

#add axis labels to plot
ax.set_title('Precision-Recall Curve')
ax.set_ylabel('Precision')
ax.set_xlabel('Recall')
plt.show()



# eval_nel(path_data="../vasari-kg.github.io/data/", path_results="results/mgenre_en/", lang="en")



