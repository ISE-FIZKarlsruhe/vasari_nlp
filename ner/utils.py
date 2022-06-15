import csv
import matplotlib.pyplot as plt

def get_dict_types(csv_file):
    dict_types = dict()
    with open(csv_file) as f:
        data = csv.DictReader(f=f, delimiter=",")
        data = list(data)
    for item in data:
        ner_type = item["type"]
        if ner_type in dict_types.keys():
            dict_types[ner_type]+=1
        else:
            dict_types[ner_type]=1
    return dict_types

dict_type = get_dict_types("results3/flair_multi_it/fp_ner.csv")
values = list(dict_type.values())
labels = list(dict_type.keys())

# Create bars
bars = plt.bar(labels, values)

# Create names on the x-axis
plt.xticks(labels, labels)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)

plt.show()