from nltk.corpus import wordnet as wn
import requests
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("en_core_web_sm")

def remove_stopwords(text):
    words = stopwords.words("english")
    convert = lambda x: " ".join([i for i in x.split() if i not in words])

    processed_text = convert(text)
    # return processed_text
    if len(processed_text) != 0:
        return processed_text
    else:
        return text

def extract_lexical_categories(word):
    synsets = wn.synsets(word)
    categories = set()
    if len(synsets) != 0:
        for synset in synsets:
            name = str(synset.lexname())
            categories.add(name)
            # definition = str(synset.definition())
            # print(name, definition)
    return categories

text = "I am a prisoner"
doc = nlp(text)

dependencies = {}
for token in doc:
    if token.dep_ in dependencies:
        dependencies[token.dep_] += [token.text]
    else:
        dependencies[token.dep_] = [token.text]

# print(dependencies)

for subj in dependencies['nsubj']:
    cat_subj = extract_lexical_categories(subj)
    for attr in dependencies['attr']:
        cat_attr = extract_lexical_categories(attr)
        # print(cat_subj, cat_attr)

        common_categories = cat_subj.intersection(cat_attr)
        if len(common_categories) == 0:
            print("\nNo overlap => {0} and {1} are METAPHORICAL".format(subj, attr))
        else:
            # to be done
            pass

