# Annotation Projection

This repo contains code for translating a conll-2012 formatted dataset, such as OntoNotes, and its annotations into another language. 


## Data
- A lot of large data files are used in this project, and therefore not included in this repo. 
The files used for word alignment when creating the Swedish version of OntoNotes can be found [here](https://drive.google.com/drive/folders/1NX9WPYHq0Gbd6b54gRXVRo4TtVorcrOp?usp=sharing).
- The OntoNotes corpus can not be shared due to licencing, but it can be obtained via [LDC](https://catalog.ldc.upenn.edu/LDC2013T19). After access, it can be compiled into train, dev, and test set using the script ```compile_coref_data.sh``` from AllenNLP.

## Word alignment
This code relies on a word aligner called [eflomal](https://github.com/robertostling/eflomal), and if you want to translate another dataset or to another language you need to use this tool. 
You would also need to get [fast_align](https://github.com/clab/fast_align) in order to use the ```atools``` program.
For OntoNotes in Swedish, you can rely on the files linked above. 


## Usage

The code is written in jupyter notebooks, so that the resulting dataframes can be inspected and created in steps. There are four notebooks: 
- ```conll-to-dataframe.ipynb``` is used to read a conll-2012 formatted file into a dataframe. 
- ```create-parallel.ipynb``` translates the texts in the dataframe and writes them to a parallel file on the format required by eflomal to create word alignments. 
The word alignments needs to be created separately, unless the existing files for Swedish are used.
- ```align-and-project.ipynb``` uses the word alignments by eflomal to project the coreference annotations from source to target language. 
- ```dataframe-to-conll.ipynb``` writes the data in the dataframe back to conll-2012 format.
 
 
 
## Create new word alignments
To create word alignments for a new dataset/language, you need ```eflomal``` and ```fast_align``` mentioned above. 
Below is an example on how to create word alignments for the dev set of the OntoNotes data. 
```parallel_ontonotes_dev.en-sv``` is created from ```create-parallel.ipynb```.
- ```./[path-to-eflomal]/align.py -i data/alignment/parallel_ontonotes_dev.en-sv --priors data/alignment/europarl.en-sv.priors --model 3 -f data/alignment/ontonotes_dev.fwd -r data/alignment/ontonotes_dev.rev```
- ```[path-to-fast-align]/build/atools -c grow-diag-final-and -i data/alignment/ontonotes_dev.fwd -j data/alignment/ontonotes_dev.rev >data/alignment/ontonotes_dev.sym``` 

