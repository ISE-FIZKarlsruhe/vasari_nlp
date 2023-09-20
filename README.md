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

## UniversalNER Results 

The model [Universal-NER](https://github.com/universal-ner/universal-ner) was used for Artwork and Subject Recognition. Scripts for inference are in `scripts_uniner` and the evaluation scripts are available in `scripts_eval`. 

|                 | Precision | Recall | F1 |
| --------------- | --------- | ------ | ----- |
| `Universal-NER/UniNER-7B-all` (Artworks)| 54.862 (±5.76)  | 56.532 (±4.79)  | 55.606 (±4.79) |
| `Universal-NER/UniNER-7B-all` (Artworks filtered) | 73.921 (±6)     | 54.055 (±3,6)  | 62.38 (±4) |
| `Universal-NER/UniNER-7B-all` (Subjects)` | 78.885 (±3,68)     | 48.748 (±2,63)  | 60.242 (±2,86) |


## Results 

Scripts for the evaluation are available in `scripts_eval`. 

### Named Entity Recognition

|                 | Precision | Recall | F1 |
| --------------- | --------- | ------ | ----- |
| `flair/ner-english-large` | 84.7     | 81.1  | 82.9 |
| `flair/ner-english-ontonotes-large` | **91.7**     | 69.2  | 78.9 |
| `Babelscape/wikineural-multilingual-ner` | 85.5     | **83.6**  | **84.6** |


### Entity Disambiguation

|          | Accuracy | 
| -------- | -------- | 
| `mGENRE` | 0.643    | 


### Entity Linking 

|                                                   | Precision | Recall | F1 |
| ------------------------------------------------- | --------- | ----- | ----- |
| `Babelscape/wikineural-multilingual-ner + mGENRE` | 0.579     | 0.55  | 0.565 |