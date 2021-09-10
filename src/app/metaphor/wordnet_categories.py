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

def return_synsets(word):
    synsets = wn.synsets(word)
    return synsets

def extract_lexical_categories(synsets):
    # synsets = wn.synsets(word)
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

def wu_palmer_similarity(syn1, syn2):
    wu_palmer_score = syn1[0].wup_similarity(syn2[0])
    shortest_path_distance = syn1[0].shortest_path_distance(syn2[0])

    return (wu_palmer_score, shortest_path_distance)

def is_noun_metaphor(obj, subj_syn, subj, dependencies):
    attr_syn = return_synsets(obj)
    wup_result = wu_palmer_similarity(subj_syn, attr_syn)
    print()
    print(subj, ",", obj)
    print("WU-Palmer Score:",wup_result)

    if wup_result[0] >= 0.3:
        cat_subj = extract_lexical_categories(subj_syn) # Categories of subject
        for attr in dependencies['attr']:
            cat_attr = extract_lexical_categories(attr_syn) # Categories of object
            # print(cat_subj, cat_attr)

            common_categories = cat_subj.intersection(cat_attr)
            if len(common_categories) == 0: # No common categories
                print("\nNo overlap => {0} and {1} are METAPHORICAL".format(subj, attr))
            else:
                main_cat_subj = find_main_category(subj, cat_subj)
                main_cat_attr = find_main_category(attr, cat_attr)

                if main_cat_attr != main_cat_subj: # Different main categories
                    print("\nMain categories are different => {0} and {1} are METAPHORICAL".format(subj, attr))
                else:
                    print("The algorithm cannot determine whether a metaphor exists in this sentence.")
    else:
        print("Metaphor due to low Wu-Palmer score")


# text = "Today is a prison and I am the inmate => figure out a logical split
# texts = ["My eyes are an ocean of blue",\
#         "Today is a prison and I am the inmate.",\
#         "I am a prisoner","You dog!",\
#         "The snow is a white blanket.",\
#         "Her long hair was a flowing golden river.",\
#         "Tom's eyes were ice as he stared at her.",\
#         "The children were flowers grown in concrete gardens.",\
#         "The falling snowflakes are dancers.",\
#         "The calm lake was a mirror.",\
#         "John's suggestion was just a Band-Aid for the problem.",\
#         "Chaos is a friend of mine.",\
#         "His eyes are saucers.",\
#         "She was an early bird.",\
#         "His memories were cloudy."]

texts = ["She was an early bird"]
doc = nlp(texts[0])

for token in doc:
    print(token.text, token.dep_)
'''
for text in texts:
    doc = nlp(text)

    dependencies = {}
    for token in doc:
        if token.dep_ in dependencies:
            dependencies[token.dep_] += [token.text]
        else:
            dependencies[token.dep_] = [token.text]

    # print(dependencies)
    try:
        for subj in dependencies['nsubj']:
            subj_syn = return_synsets(subj)
            # print(subj_syn)
            if "attr" in dependencies:
                dependency = "attr"
            elif "acomp" in dependencies:
                dependency = "acomp"
            for dep in dependencies[dependency]:
                is_noun_metaphor(dep, subj_syn, subj, dependencies)
    except Exception as e:
        print("Error")                 

#     except Exception as e:
#         print("\n")
#         print(text)
#         print(e)
#         print("----------------")
'''


# COCA Collocation Dataset required

# print("MCA:", main_cat_attr)
# print("MCS:",main_cat_subj)
    
# pass

