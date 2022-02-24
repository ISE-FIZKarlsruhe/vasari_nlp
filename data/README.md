# Evaluation data for Entity Linking on Art History literature

This evaluation dataset provides a set of sentences in English and Italian taken from two different editions of *Lives of the Most Excellent Painters, Sculptors and Architects* by Giorgio Vasari. This evaluation dataset was created for evaluating different Entity Linking tools on Art History literature.<br/>

The editions referred to are:

* **IT**: Giorgio Vasari. Le Vite de' Piu Eccellenti Pittori, Scultori, et Architettori (1. ed. 1550). Einaudi (2000). [archive.org](https://archive.org/details/vitedepiueccellentipittoriscultoriedarchitettilegiorgiovasari) \[OCR transcribed\]
* **EN**: Lives of the Most Eminent Painters, Sculptors and Architects. Translated by Gaston du C. De Vere from the 1568 edition. Macmillan and the Medici Society (1912-1915). [Project Gutenberg](https://onlinebooks.library.upenn.edu/webbin/metabook?id=livespainters) \[Digital transcription\]


## Norms for the annotation
We annotated Named Entities mentioned in a text by using [Doccano](https://github.com/doccano/doccano). Entity spans are annotated with 5 types: **PER**, **LOC**, **ORG**, **MISC**, and **WORK**. The last type, introduced in this dataset, serves the purpose of annotating *Creative Works* explicitly mentioned in a text. Each entity span is subsequently disambiguated by linking it to the corresponding Wikidata entity.<br/>
A specific named entity is considered in our annotation if:
* It's a Person (either fictional or real), a natural or geographical space, a human-made facility, an organization, an artistic subject (either a character or an event), or a creative work.
* It has a related Wikipedia page.<br/>

In this evaluation dataset, we do not consider overlapping entities. We solved the problems of nested entities by considering only the longest surface form. However, many artworks are mentioned in the text by using a surface form which denotes also their subject. For this specific case, we adopt the following rules:<br/>
* if the surface form is preceeded by an undefinite article, we will link it to the subject entity, except when taking co-reference into account.
* if the surface form is preceeded by a definite article, we will link it to the creative work, except when taking co-reference into account

Co-reference resolution is important since these rules may not always be correct and depend on the information provided by the context.
```
Leonardo painted an [ Adoration of the Magi ] (Adoration of the Magi - subject )
```
```
Leonardo painted the [ Adoration of the Magi ] (Adoration of the Magi - painting)
```
```
Leonardo painted a [Last Supper] (Last Supper - painting), a most beautiful and marvellous thing.
```

## Details

In order to remove errors derived from OCR transcriptions from the Italian text, we preliminarily applied regular expression to the sampled sentences. More specifically, 1) we automatically removed whitespaces between First Name initials and the rest of the name, and 2) we added whitespaces between two merged nouns which were both capitalized. In the first step, we do not remove whitespace if the uppercase letter is at the beginning of the sentence or at a word-boundary.




