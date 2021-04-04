import pandas as pd 
import numpy as np 
from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import warnings
warnings.filterwarnings("ignore")

# Tags:
# 
# - ARGx: Argument (The lowest is usually the subject)
# - V: Verb
# - ARGM-XXX: Modifiers
#     - ARGM-LOC: Modifier-Location
#     - ARGM-TMP: Modifier-Temporal
#     - ARGM-ADV: Modifier-Adverbial
#     - ARGM-DIS: Modifier-Discourse

predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz")

text = "A two-seater aircraft crashed in Odisha's Dhenkanal district on Monday, killing a trainee pilot and her instructor, officials said"
    
def get_oie_triplets(text):
    print("\n-------------------------------------------\n")
    print("Text:", text, "\n")

    openie = predictor.predict(sentence = text)

    triplet_list = []

    print("Total Number of Extractions Found:",len(openie['verbs']))
    print("------------------------------------\n")
    for count, i in enumerate(openie['verbs']):
        desc = i['description']
        oie_triplets = desc.split(",")
        triplet_dict = {}
        for triplet in oie_triplets:
            tags = triplet.replace("[","")
            tags = tags.split('] ')
            if tags[-1] == '':
                tags = tags[:-1]
            # print(l1)
            for tag in tags:
                trip = tag.split(": ")
                try:
                    triplet_dict[trip[1]] = trip[0]
                except Exception as e:
                    triplet_dict[trip[0]] = None

        print("Extraction",count+1,":")
        print(triplet_dict)
        print("\n")

        triplet_list.append(triplet_dict)
    
    return triplet_list

if __name__=='__main__':
    get_oie_triplets(text)
# triplet_list = get_oie_triplets(text)
# print("List of triplets:")
# print(triplet_list)