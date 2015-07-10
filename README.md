# umls2hana

![UMLS Logo](http://www.nlm.nih.gov/research/umls/images/UMLS_header_newtree.gif)

This repository contains software to convert the [Metathesaurus of UMLS](http://www.nlm.nih.gov/research/umls/) into a dictionary that can be used by [SAP HANA](https://en.wikipedia.org/wiki/SAP_HANA). UMLS is the *Unified Medical Language System* and provides mappings of vocabularies from the biomedical domain. The *Metathersaurus* is the unified vocabulary of over 100 incorporated controlled vocabularies and classification systems.

### UMLS Metathesaurus

To use the Metathesaurus you first have to download and extract it from [here](http://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html). To use the vocabulary in HANA you have to convert it into a XML-Dictionary. You need to point our converter to your downloaded version of the UMLS Metathesaurus. Right now the script only needs the files `META/MRCONSO.RRF` and `META/MRSTY.RRF` to build the dictionary. You can do this by using our converter:

```
python dict-convert.py /umls/path/
```


### UMLS Semantic Network

The [UMLS Semantic Network](http://semanticnetwork.nlm.nih.gov/) contains a list of the semantic types and a list of relations between these types. All related files can be downloaded [here](http://semanticnetwork.nlm.nih.gov/Download/index.html).

Using this script you can import the semantic types and relations into your HANA instance. For this you only need the *SRDEF.html* and *SRSTRE1.html* files.

```
Usage: semantic-network-parser.py [options] input_folder

Options:
  -h, --help            show this help message and exit
  -s SERVER, --server=SERVER
                       Address of the HANA server
  -p PORT, --port=PORT  
  -u USER, --user=USER 
```

```
python semantic-network-parser.py ~/umls-semantic-network/
```
