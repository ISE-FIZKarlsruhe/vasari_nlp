# Entity Extraction for the Historical Biographies of Giorgio Vasari

This repository contains data and source code used for the Entity Extraction experiments of Entity Recognition and Entity Linking on Giorgio Vasari's *Lives of The Artists*.

The `data` directory contains 7 csv files:

1. `sentences.csv`: containing 54 sentences extracted from 27 paragraphs extracted from *Lives of The Artists* ([Project Gutenberg Edition](https://www.gutenberg.org/ebooks/25326))
2. `entities.csv`: containing named entities linked to Wikidata and labelled with the 4 entity types from CONLL-2003 (PER, ORG, LOC, MISC)
3. `works.csv`: containing artwork references (visual works) linked to Wikidata
4. `terms.csv`: containing generic artistic concepts linked to [Getty's AAT](https://www.getty.edu/research/tools/vocabularies/aat/)
5. `dates.csv`: containing annotated dates (1463) or time intervals (*after the Death of Julius II*)
6. `motifs.csv`: containing iconographic subjects annotated with [ICONCLASS](www.iconclass.org)
7. `spans.csv`: containing links between the annotation of subjects (`SUBJ`) and the annotation of further predicated states (`STATE`) in `motifs.csv`


For further information related to the annotation, Guidelines are available on \[1\]. All the data was annotated using [Inception](https://inception-project.github.io/).

The `results` directory contains the results obtained by testing several general-purpose Entity Recognition and Entity Linking models on the Named Entities in `entities.csv`. 
Moreover, it contains the results of a [domain-specific Spacy NER model for artworks](https://github.com/HPI-Information-Systems/art-ner-dataset) on the artwork references annotated in `works.csv`.

Source code for Entity Recognition is available as Jupyter notebooks in the `notebook` directory.

Source code used to test the pre-trained Entity Linking model mGENRE, as well as the scripts used for evaluation, are available in the `src` directory.

\[1\] Santini, Cristian, Tan, Mary Ann, Bruns, Oleksandra, Tietz, Tabea, Posthumus, Etienne, & Sack, Harald. (2023). Guidelines for the Annotation of ExtrART: Evaluation Dataset for Entity Extraction from The Lives Of The Artists (1550). Zenodo. [https://doi.org/10.5281/zenodo.7991340](https://doi.org/10.5281/zenodo.7991340)
