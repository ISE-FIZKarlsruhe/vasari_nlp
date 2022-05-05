# Evaluation data for Entity Linking on Art History literature

This evaluation dataset provides a set of sentences in English and Italian taken from two different editions of *Lives of the Most Excellent Painters, Sculptors and Architects* by Giorgio Vasari. This evaluation dataset was created for evaluating different Entity Linking tools on Art History literature.<br/>

The editions referred to are:

* **IT**: Giorgio Vasari. Le Vite de' Piu Eccellenti Pittori, Scultori, et Architettori (1. ed. 1550). Einaudi (2000). [archive.org](https://archive.org/details/vitedepiueccellentipittoriscultoriedarchitettilegiorgiovasari) \[OCR transcribed\]
* **EN**: Lives of the Most Eminent Painters, Sculptors and Architects. Translated by Gaston du C. De Vere from the 1568 edition. Macmillan and the Medici Society (1912-1915). [Project Gutenberg](https://onlinebooks.library.upenn.edu/webbin/metabook?id=livespainters) \[Digital transcription\]


## Norms for the annotation
We annotated Named Entities mentioned in a text by using [Doccano](https://github.com/doccano/doccano). Entity spans are annotated with 5 types: **PER**, **LOC**, **ORG**, **MISC**. 

In this evaluation dataset, we do not consider overlapping entities. We solved the problems of nested entities by considering only the longest surface form.


GUIDELINES TO BE UPDATED

## Details

In order to remove errors derived from OCR transcriptions from the Italian text, we preliminarily applied regular expression to the sampled sentences. More specifically, 1) we automatically removed whitespaces between First Name initials and the rest of the name, and 2) we added whitespaces between two merged nouns which were both capitalized. In the first step, we do not remove whitespace if the uppercase letter is at the beginning of the sentence or at a word-boundary.




