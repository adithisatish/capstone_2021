# Subject-Predicate-Object Detection

# Importing libraries
import pandas as pd 
import numpy as np
import re
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # to ignore tensorflow warnings and information logs

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import warnings
warnings.filterwarnings("ignore") # ignore any other warnings

# Tags:
# 
# - ARGx: Argument (The lowest ARGx is usually the subject)
# - V: Verb
# - ARGM-XXX: Modifiers
#     - ARGM-LOC: Modifier-Location
#     - ARGM-TMP: Modifier-Temporal
#     - ARGM-ADV: Modifier-Adverbial
#     - ARGM-DIS: Modifier-Discourse

modifiers = {'ARGM-LOC': 'Location', 'ARGM-TMP': 'Temporal', 'ARGM-ADV': 'Adverbial', 'ARGM-DIS': 'Discourse', 'ARGM-MNR':'Manner/Behaviour'}
argmatch = lambda x: re.search('ARG[0-9]:',x)
# print(argmatch('ARG1: what'))

text = sys.argv[1]
    

# Function to take text as input and return a list of all the different OpenInformationExtraction dictionaries found
def get_oie_triplets(text):
    
    # Initializing the AllenNLP-OIE predictor
    predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz")
    openie = predictor.predict(sentence = text)

    triplet_list = []

    # print("\nTotal Number of Extractions Found:",len(openie['verbs']))
    for count, i in enumerate(openie['verbs']): # contains the ARGx, V and ARGM-XXX
        desc = i['description']
        oie_triplets = desc.split(",")
        triplet_dict = {}

        # print(oie_triplets)

        for triplet in oie_triplets:
            tags = triplet.replace("[","")
            tags = tags.split('] ')

            if tags[-1] == '':
                tags = tags[:-1]
            if tags[-1] == ']':
                tags = tags[:-1]

            # print(tags)
            
            for tag in tags:
                if "ARGM-ADV" not in tag and 'V:' in tag and tag.find('V:') !=0:
                    tag = tag[tag.find('V:'):]
                    # print(tag)
                elif argmatch(tag)!= None and argmatch(tag).span()[0]!=0:
                    tag = tag[argmatch(tag).span()[0]:]
                trip = tag.split(": ")
                
                try:
                    if trip[1][-1]==']':
                        trip[1] = trip[1][:-1]
                    triplet_dict[trip[0].strip()] = trip[1].strip()
                
                except Exception as e:
                    if trip[0][-1]==']':
                        trip[0] = trip[1][:-1]
                    triplet_dict["NONE"] = trip[0]

        triplet_list.append(triplet_dict) # List of parsed OIE triplets
    
    return triplet_list

# Function to take dictionary containing OIE triplet as input and extract SVO + modifiers from it
def get_svo_from_triplet(triplet):
    
    try:
        argmin = min(triplet.keys())
        subject = triplet[argmin]
    except Exception as e:
        subject = "None"
    try:
        connecting_verb = triplet['V']
    except Exception as e:
        connecting_verb = 'None'

    object_clauses = []
    arg_modifiers = {}
    
    for key, value in triplet.items():
        # key = key.strip()
        try:
            if 'ARGM' in key:
                arg_modifiers[modifiers[key]] = value
        except Exception as e:
            arg_modifiers[key] = "!!New Arg Modifer!!"
        
        if 'ARG' in key and key != argmin and 'ARGM' not in key:
            object_clauses.append(value)

    return (subject,connecting_verb,object_clauses,arg_modifiers)
            

def detect_svo(text):
    list_of_triplets = get_oie_triplets(text)

    print("\nSentence:", text)
    
    for triplet in list_of_triplets:
        print("\n-----------------------------------------------------------")
        print()
        # print(triplet)
        
        print("Deconstruction:")
        subject, verb, obj_clauses, arg_modifiers = get_svo_from_triplet(triplet)
        
        print("\nSubject Clause:",subject)
        print("\nConnecting Verb:", verb)

        if len(obj_clauses) == 0:
            print("\nObject Clause(s): None")
        else:
            print("\nObject Clause(s):")
            for obj_clause in obj_clauses:
                print(obj_clause)
        
        if arg_modifiers == {}:
            print("\nSentence Modifiers: None")
        else:
            print("\nSentence Modifiers (as key-value pairs):")
            for modifier_key, modifier in arg_modifiers.items():
                print("{0}: {1}".format(modifier_key, modifier))

if __name__=='__main__':
    detect_svo(text)