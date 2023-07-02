# iREAD: Interpretable REcognition and Automated Deconstruction of Semantics in Written English

iREAD is a learning aid that uses Machine Learning and Natural Language Processing techniques to deconstruct passages and identify literary devices and rammatical rules pertaining to Tense, Tone, Rhyme Schemes, and Metaphors, amongst others. The techniques used provide an insight to the rationale behind the deconstruction using: (1) an intuitive explanation through explication of the rules that underlie the grammatical constructs and (2) identifying the most relevant features for machine classification as a way to explain the outcome of models. We validate the algorithms that underlie the learning aid on manually annotated datasets from high school textbooks on English Grammar that are widely prescribed and referred to. The various components are delineated to three learning levels: easy (recognition of subject-predicate-object, tense and tone), intermediate (recognition of simile, alliteration and rhyme scheme) and advanced (recognition of metaphor and voice).

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


