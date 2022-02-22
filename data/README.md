# Evaluation data for Entity Linking on Art History literature

This evaluation dataset provides a set of sentences in English and Italian taken from two different editions of *Lives of the Most Excellent Painters, Sculptors and Architects* by Giorgio Vasari. This evaluation dataset was created for evaluating different Entity Linking tools on Art History literature.<br/>

The editions referred to are:

* 
* 

## Norms for the annotation
We annotated Named Entities mentioned in a text by using [Doccano](https://github.com/doccano/doccano). Entity spans are annotated with 5 types: **PER**, **LOC**, **ORG**, **MISC**, and **WORK**. The last type, introduced in this dataset, serves the purpose of annotating *Creative Works* explicitly mentioned in a text.<br/>
A specific named entity is considered in our annotation if:
* It's a Person (either fictional or real), a natural or geographical space, a human-made facility, an organization, an artistic subject (either a character or an event), or a creative work.
* It has a related Wikipedia page.<br/>

In this evaluation dataset, we do not consider overlapping entities. However, many artworks are mentioned in the text by using a surface form which denotes also their subject. For this specific case, we considered multiple entities, i.e. the subject and the artwork, to be the correct entity to link.<br/>
```
Leonardo painted an \[ Adoration of the Magi \] \(Adoration of the Magi - painting | Adoration of the Magi - subject \)
```


