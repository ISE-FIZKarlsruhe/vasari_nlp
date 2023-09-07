# Entity Extraction for the Historical Biographies of Giorgio Vasari

This repository contains data and source code used for the Entity Extraction experiments of Entity Recognition and Entity Disambiguation on Giorgio Vasari's *Lives of The Artists*.

## Requirements

This code has been tested with **Python 3.9** and the following [requirements](requirements.txt).

The code to run different Entity Recognition models is available in the Jupyter notebooks in the `notebooks_ner` directory.

The Entity Linking scripts in `scripts_disambiguation` rely on the [mGENRE](https://github.com/facebookresearch/GENRE) model from facebook. To run these scripts, you should install both **fairseq** and the **GENRE** library from source.

```
git clone --branch fixing_prefix_allowed_tokens_fn https://github.com/nicola-decao/fairseq
git clone https://github.com/facebookresearch/GENRE.git 
cd fairseq
pip install --editable ./
cd ../
cd GENRE
pip install --editable ./
```

Moreover, for running the mGENRE model you need to download [fairseq_multilingual_entity_disambiguation](https://dl.fbaipublicfiles.com/GENRE/fairseq_multilingual_entity_disambiguation.tar.gz), [titles_lang_all105_trie_with_redirect.pkl](http://dl.fbaipublicfiles.com/GENRE/titles_lang_all105_trie_with_redirect.pkl) and [lang_title2wikidataID-normalized_with_redirect](https://dl.fbaipublicfiles.com/GENRE/lang_title2wikidataID-normalized_with_redirect.pkl)
