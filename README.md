# iREAD: Interpretable REcognition and Automated Deconstruction of Semantics in Written English

iREAD is a learning aid that uses Machine Learning and Natural Language Processing techniques to deconstruct passages and identify literary devices and grammatical rules pertaining to Tense, Tone, Rhyme Schemes, and Metaphors, amongst others. The techniques used provide an insight to the rationale behind the deconstruction using: (1) an intuitive explanation through explication of the rules that underlie the grammatical constructs and (2) identifying the most relevant features for machine classification as a way to explain the outcome of models. We validate the algorithms that underlie the learning aid on manually annotated datasets from high school textbooks on English Grammar that are widely prescribed and referred to. The various components are delineated to three learning levels: easy (recognition of subject-predicate-object, tense and tone), intermediate (recognition of simile, alliteration and rhyme scheme) and advanced (recognition of metaphor and voice).

Published in the EDULEARN23 conference proceedings. 

### Required Libraries
To run the AllenNLP module, [PyTorch](https://pytorch.org/) is required (follow the installation steps on the website).

Run ```pip install -r requirements.txt``` once all the prerequisites are satisfied.

### Execution
1. To start the authserver, navigate to ```webapp``` and run ```npm run dev``` on the terminal.
2. To start the client, navigate to ```webapp/client``` and run ```npm start``` on a new terminal.
3. To start the Flask server, navigate to ```src``` and run ```python server.py``` on another terminal.

Note: Refer to the Instructions file for detailed directions on how to execute the individual components.

### Tech Specifications
- Frontend: React
- Backend: Python (Flask Server)
- Database for authentication: Firebase

### Components Implemented
- Subject-Predicate-Object
- Tense
- Tone
- Alliterations
- Rhyme Scheme
- Simile
- Metaphor
- Voice

### Citation
If you use this repository, please cite the following paper: 
```
@InProceedings{SATISH2023IRE,
author    = {Satish, A. and Bhamare, A. and Hoskote, D. and Raj, V. and Srinivasa, G.},
title     = {IREAD: INTERPRETABLE RECOGNITION AND AUTOMATED DECONSTRUCTION OF SEMANTICS IN WRITTEN ENGLISH},
series    = {15th International Conference on Education and New Learning Technologies},
booktitle = {EDULEARN23 Proceedings},
isbn      = {978-84-09-52151-7},
issn      = {2340-1117},
doi       = {10.21125/edulearn.2023.0668},
url       = {https://doi.org/10.21125/edulearn.2023.0668},
publisher = {IATED},
location  = {Palma, Spain},
month     = {3-5 July, 2023},
year      = {2023},
pages     = {2266-2275}}
```
