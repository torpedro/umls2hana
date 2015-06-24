# umls2hana

![UMLS Logo](http://www.nlm.nih.gov/research/umls/images/UMLS_header_newtree.gif)

This repository contains software to convert the [Metathesaurus of UMLS](http://www.nlm.nih.gov/research/umls/) into a dictionary that can be used by [SAP HANA](https://en.wikipedia.org/wiki/SAP_HANA). UMLS is the *Unified Medical Language System* and provides mappings of vocabularies from the biomedical domain. The *Metathersaurus* is the unified vocabulary of over 100 incorporated controlled vocabularies and classification systems.

### Convert the Metathesaurus to XML-Dictionaries
```
# Tested with Python 2.7
python convert.py /umls/path/
```

