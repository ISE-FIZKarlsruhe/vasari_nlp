import matplotlib.pyplot as plt
import csv

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

def plt_per_type(items):
    output_dict = {}
    for item in items:
        label = item["type"]
        if label in output_dict.keys():
            output_dict[label] += 1
        else:
            output_dict[label] = 1

    
    plt.bar(output_dict.keys(), output_dict.values())
    addlabels(list(output_dict.keys()), list(output_dict.values()))
    plt.xlabel("Types")
    plt.ylabel("Number of false negatives")
    plt.show()

with open("../mgenre_babel_it/fn_ner.csv", "r") as f:
    dict_reader = csv.DictReader(f, delimiter=",")
    data = list(dict_reader)

plt_per_type(data)
