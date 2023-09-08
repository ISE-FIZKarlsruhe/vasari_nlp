# Entity Extraction for the Historical Biographies of Giorgio Vasari

This repository contains data and source code used for the Entity Extraction experiments of Entity Recognition and Entity Disambiguation on Giorgio Vasari's *Lives of The Artists*.

## Requirements

This code has been tested with **Python 3.9** and the following [requirements](requirements.txt).

The code to run different Entity Recognition models is available in the Jupyter notebooks in the `notebooks_ner` directory.

The Entity Linking scripts in `scripts_disambiguation` rely on the [mGENRE](https://github.com/facebookresearch/GENRE) model from facebook. To run these scripts, you should install the **GENRE** library from source.

```
git clone https://github.com/facebookresearch/GENRE.git 
cd GENRE
pip install --editable ./
```

Moreover, for running the mGENRE model you need to download [fairseq_multilingual_entity_disambiguation](https://dl.fbaipublicfiles.com/GENRE/fairseq_multilingual_entity_disambiguation.tar.gz), [titles_lang_all105_trie_with_redirect.pkl](http://dl.fbaipublicfiles.com/GENRE/titles_lang_all105_trie_with_redirect.pkl) and [lang_title2wikidataID-normalized_with_redirect](https://dl.fbaipublicfiles.com/GENRE/lang_title2wikidataID-normalized_with_redirect.pkl).


## Results 

Scripts for the evaluation are available in `scripts_eval`. 

### Named Entity Recognition

|                 | Precision | Recall | F1 |
| --------------- | --------- | ------ | ----- |
| `flair/ner-english-large` | 0.847     | 0.811  | 0.829 |
| `flair/ner-english-ontonotes-large` | **0.917**     | 0.692  | 0.789 |
| `Babelscape/wikineural-multilingual-ner` | 0.855     | **0.836**  | **0.846** |
