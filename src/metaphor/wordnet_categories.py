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

    processed_text = convert(text).lower()
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

def find_main_category(noun, categories):
    main_cat = ''
    max_rel = -99999
    for cat in categories:
        if "noun" in cat:
            current_category = cat[5:]
            path = 'http://api.conceptnet.io//relatedness?node1=/c/en/'+noun+'&node2=/c/en/'+current_category
            result = requests.get(path).json()
            # print(current_category, result['value'])
            if result['value'] > max_rel:
                max_rel = result['value']
                main_cat = current_category
    
    return main_cat


text = "chocolate is a pizza"
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
            main_cat_subj = find_main_category(subj, cat_subj)
            main_cat_attr = find_main_category(attr, cat_attr)

            if main_cat_attr != main_cat_subj:
                print("\nNo overlap => {0} and {1} are METAPHORICAL".format(subj, attr))
            else:
                print("ugh I cry")
            
            # print("MCA:", main_cat_attr)
            # print("MCS:",main_cat_subj)
                    
            # pass

