import csv
import re

with open("sentences.csv", "r") as f1:
    sentences = list(csv.DictReader(f1, delimiter=","))
with open("entities.csv", "r") as f2:
    entities = list(csv.DictReader(f2, delimiter=","))
with open("dates.csv", "r") as f3:
    dates = list(csv.DictReader(f3, delimiter=","))
with open("works.csv", "r") as f4:
    works = list(csv.DictReader(f4, delimiter=","))
with open("motifs.csv", "r") as f5:
    motifs = list(csv.DictReader(f5, delimiter=","))
with open("coref.csv", "r") as f6:
    coref = list(csv.DictReader(f6, delimiter=","))

max_length = (None, 0)
min_length = (None, 1000)
max_annotations = (None, 0)
min_annotations = (None, 1000)
max_entities = (None, 0)
min_entities = (None, 1000)
max_coref = (None, 0)
min_coref = (None, 1000)
max_dates = (None, 0)
min_dates = (None, 1000)
max_works = (None, 0)
min_works = (None, 1000)
max_motifs = (None, 0)
min_motifs = (None, 1000)
max_work = (None, 0)
max_motif = (None, 0)

id = "agnolo"
max_work = (None, 0)
max_motif = (None, 0)

length_chapters = []
length_chapter = 0
for row in sentences:
    chapter = row["id"].split(":")[0]
    if id != chapter:
        length_chapters.append(length_chapter)
        if length_chapter >= max_length[1]:
            max_length = (id, length_chapter)
        if length_chapter <= min_length[1]:
            min_length = (id, length_chapter)
        id = chapter
        length_chapter = 0
    length_chapter += len(re.findall(r"\w+", row["sentence"]))
length_chapters.append(length_chapter)
if length_chapter >= max_length[1]:
    max_length = (id, length_chapter)
if length_chapter <= min_length[1]:
    min_length = (id, length_chapter)

id = "agnolo"
entities_chapters = []
entities_chapter = 0
for row in entities:
    chapter = row["id"].split(":")[0]
    if id != chapter:
        entities_chapters.append(entities_chapter)
        if entities_chapter >= max_entities[1]:
            max_entities = (id, entities_chapter)
        if entities_chapter <= min_entities[1]:
            min_entities = (id, entities_chapter)
        id = chapter
        entities_chapter = 0
    entities_chapter += 1
entities_chapters.append(entities_chapter)
if entities_chapter >= max_entities[1]:
    max_entities = (id, entities_chapter)
if entities_chapter <= min_entities[1]:
    min_entities = (id, entities_chapter)

id = "agnolo"
coref_chapters = []
coref_chapter = 0
for row in coref:
    chapter = row["id"].split(":")[0]
    if id != chapter:
        coref_chapters.append(coref_chapter)
        if coref_chapter >= max_coref[1]:
            max_coref = (id, coref_chapter)
        if coref_chapter <= min_coref[1]:
            min_coref = (id, coref_chapter)
        id = chapter
        coref_chapter = 0
    coref_chapter += 1
coref_chapters.append(coref_chapter)
if coref_chapter >= max_coref[1]:
    max_coref = (chapter, coref_chapter)
if coref_chapter <= min_coref[1]:
    min_coref = (chapter, coref_chapter)

id = "agnolo"
dates_chapters = []
dates_chapter = 0
for row in dates:
    chapter = row["id"].split(":")[0]
    if id != chapter:
        dates_chapters.append(dates_chapter)
        if dates_chapter >= max_dates[1]:
            max_dates = (id, dates_chapter)
        if dates_chapter <= min_dates[1]:
            min_dates = (id, dates_chapter)
        id = chapter
        dates_chapter = 0
    dates_chapter += 1
dates_chapters.append(dates_chapter)
if dates_chapter >= max_dates[1]:
    max_dates = (chapter, dates_chapter)
if dates_chapter <= min_dates[1]:
    min_dates = (chapter, dates_chapter)


id = "agnolo"
works_chapters = []
works_chapter = 0
for row in works:
    if len(row["surface"])>=max_work[1]:
        max_work = (row["surface"], len(row["surface"]))
    chapter = str(row["id"].split(":")[0])
    if not id == chapter:
        works_chapters.append(works_chapter)
        if works_chapter >= max_works[1]:
            max_works = (id, works_chapter)
        if works_chapter <= min_works[1]:
            min_works = (id, works_chapter)
        id = chapter
        works_chapter = 0
    works_chapter += 1
works_chapters.append(works_chapter)
if works_chapter >= max_works[1]:
    max_works = (chapter, works_chapter)
if works_chapter <= min_works[1]:
    min_works = (chapter, works_chapter)


id = "agnolo"
motifs_chapters = []
motifs_chapter = 0
for row in motifs:
    if len(row["surface"])>=max_motif[1]:
        max_motif = (row["surface"], len(row["surface"]))
    chapter = row["id"].split(":")[0]
    if id != chapter:
        motifs_chapters.append(motifs_chapter)
        if motifs_chapter >= max_motifs[1]:
            max_motifs = (id, motifs_chapter)
        if motifs_chapter <= min_motifs[1]:
            min_motifs = (id, motifs_chapter)
        id = chapter
        motifs_chapter = 0
    motifs_chapter += 1
motifs_chapters.append(motifs_chapter)
if motifs_chapter >= max_motifs[1]:
    max_motifs = (chapter, motifs_chapter)
if motifs_chapter <= min_motifs[1]:
    min_motifs = (chapter, motifs_chapter)

annotations = entities_chapters + coref_chapters + dates_chapters + works_chapters + motifs_chapters
with open("stats.txt", "w") as f:
    f.write("Tokens in corpus: "+ str(sum(length_chapters))+"\n")
    f.write("Avg tokens per artist: "+ str(sum(length_chapters)/27)+"\n")
    f.write("Longest chapter is: "+ str(max_length[0])+" with "+ str(max_length[1])+ " tokens\n")
    f.write("Shortest chapter is: "+ str(min_length[0])+" with "+ str(min_length[1])+ " tokens\n")
    f.write("Annotations in corpus: "+ str(sum(annotations))+"\n")
    f.write("Avg. annotations per artist: "+ str(sum(annotations)/27)+"\n")
    f.write("Entities in corpus: "+ str(sum(entities_chapters))+"\n")
    f.write("coreferences in corpus: "+ str(sum(coref_chapters))+"\n")
    f.write("Dates in corpus: "+ str(sum(dates_chapters))+"\n")
    f.write("Works in corpus: "+ str(sum(works_chapters))+"\n")
    f.write("Motifs in corpus: "+ str(sum(motifs_chapters))+"\n")
    f.write("Chapter with most entities is: "+ str(max_entities[0])+" with "+ str(max_entities[1])+ " entities\n")
    f.write("Chapter with most coreferences is: "+ str(max_coref[0])+" with "+ str(max_coref[1])+ " coreferences\n")
    f.write("Chapter with most dates is: "+ str(max_dates[0])+" with "+ str(max_dates[1])+ " dates\n")
    f.write("Chapter with most works is: "+ str(max_works[0])+" with "+ str(max_works[1])+ " works\n")
    f.write("Chapter with most motifs is: "+ str(max_motifs[0])+" with "+ str(max_motifs[1])+ " motifs\n")
    f.write("Chapter with less entities is: "+ str(min_entities[0])+" with "+ str(min_entities[1])+ " entities\n")
    f.write("Chapter with less coreferences is: "+ str(min_coref[0])+" with "+ str(min_coref[1])+ " coreferences\n")
    # f.write("Chapter with less dates is: "+ str(min_dates[0])+" with "+ str(min_dates[1])+ " dates\n")
    # f.write("Chapter with less works is: "+ str(min_works[0])+" with "+ str(min_works[1])+ " works\n")
    # f.write("Chapter with less motifs is: "+ str(min_motifs[0])+" with "+ str(min_motifs[1])+ " motifs\n")
    f.write("longest artwork description is <"+ str(max_work[0])+"> with "+ str(max_work[1])+ " characters\n")
    f.write("longes motif description is <"+ str(max_motif[0])+"> with "+ str(max_motif[1])+ " characters\n")


