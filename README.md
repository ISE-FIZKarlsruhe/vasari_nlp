# Knowledge Extraction for the Historical Biographies of Giorgio Vasari

This repository contains data and source code used for the Knowledge Extraction experiments of Entity Recognition and Entity Linking on Giorgio Vasari's *Lives of The Artists*.

The `data` directory contains 6 csv files:

1. `sentences.csv`: containing 54 sentences extracted from 27 paragraphs extracted from *Lives of The Artists* ([Project Gutenberg Edition](https://www.gutenberg.org/ebooks/25326))
2. `entities.csv`: containing named entities linked to Wikidata and labelled with the 4 entity types from CONLL (PER, ORG, LOC, MISC)
3. `works.csv`: containing direct references to artworks linked to Wikidata
4. `motifs.csv`: containing iconographic motifs manually labelled with Iconclass codes
5. `terms.csv`: containing a list of generic terms related to art and architecture and labelled with 4 entity types (OBJ, OBJarch, OBJsculpt, OBJpaint)
6. `dates.csv`: containing a list of calendar dates or intervals annotated with either 1 value if it is a specific calendar date or 4 (earliest begin, begin, end, latest end) if it is a time interval.

The `results` directory contains the results obtained by testing several general-purpose Entity Recognition and Entity Linking models on the Named Entities in `entities.csv`. 
Moreover, it contains the results of a [domain-specific Spacy NER model for artworks](https://github.com/HPI-Information-Systems/art-ner-dataset) on the artwork references annotated in `works.csv`.

Source code for Entity Recognition is available as Jupyter notebooks in the `notebook` directory.

Source code used to test the pre-trained Entity Linking models Blink and mGENRE, as well as the scripts used for evaluation, are available in the `src` directory.
