# Computational Algorithms for Explainable Deconstruction of Semantics in Written English

The framework implemented here intends to deconstruct English sentences and paragraphs to identify and highlight the different grammatical forms used. In addition to this, it also aims to provide interpretability by explaining the reasoning behind the identification. In doing this, we provide a tool that will help laymen understand and significantly improve their written English. 

This repository contains the datasets and source code files which accompany the paper "Computational Algorithms for Explainable Deconstruction of Semantics in Written English" submitted to the 31st International Joint Conference on Artificial Intelligence (IJCAI-ECAI 2022).

### Required Libraries
To run the AllenNLP module, [PyTorch](https://pytorch.org/) is required (follow the installation steps on the website).

Run ```pip install -r requirements.txt``` once all the prerequisites are satisfied.

### Execution
1. Navigate to ```client``` and run ```npm start``` on the terminal.
2. Navigate to ```src``` and run ```python server.py``` on another terminal.

Note: Refer to the Instructions file for detailed directions on how to execute the individual components.

### Tech Specifications
- Frontend: React
- Backend: Python (Flask Server)
- Database for authentication: Firebase

### Components Implemented
- Alliterations
- Metaphors
- Rhyme Scheme
- Similes
- Subject Predicate Object
- Tense
- Tone
- Voice
