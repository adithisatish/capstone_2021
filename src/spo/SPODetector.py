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

class SPO:
    # Tags:
    # 
    # - ARGx: Argument (The lowest ARGx is usually the subject)
    # - V: Verb
    # - ARGM-XXX: Modifiers
    def __init__(self, text, paragraph = 0):
        self.modifiers = {'ARGM-LOC': 'Location', 'ARGM-TMP': 'Temporal', 'ARGM-ADV': 'Adverbial - General Purpose', 
                    'ARGM-DIS': 'Discourse', 'ARGM-MNR':'Manner/Behaviour', 'ARGM-DIR': 'Directional',
                    'ARGM-EXT':'Extent', 'ARGM-PNC': 'Purpose', 'ARGM-CAU': 'Causal', 
                    'ARGM-NEG': 'Negation','ARGM-MOD': 'Modal Verb'}
        self.argmatch = lambda x: re.search('ARG[0-9]:',x)
        self.text = text
        self.paragraph = paragraph
        self.svo_list = []
    # print(argmatch('ARG1: what'))
        

    # Function to take text as input and return a list of all the different OpenInformationExtraction dictionaries found
    def get_oie_triplets(self, text):
        
        # Initializing the AllenNLP-OIE predictor
        predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz")
        openie = predictor.predict(sentence = text)

        triplet_list = []

        # print("\nTotal Number of Extractions Found:",len(openie['verbs']))
        for count, i in enumerate(openie['verbs']): # contains the ARGx, V and ARGM-XXX
            desc = i['description']
            # print(desc)
            if "V" in desc and "ARG" not in desc:
                continue
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
                    elif self.argmatch(tag)!= None and self.argmatch(tag).span()[0]!=0:
                        tag = tag[self.argmatch(tag).span()[0]:]

                    if "ARGM" in tag and tag.find("ARGM") !=0:
                        tag = tag[tag.find("ARGM"):]

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
    def get_svo_from_triplet(self, triplet):
        
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
                    arg_modifiers[self.modifiers[key]] = value
            except Exception as e:
                arg_modifiers[key] = "!!New Arg Modifer!!"
            
            if 'ARG' in key and key != argmin and 'ARGM' not in key:
                object_clauses.append(value)

        svo_result = {'Subject':subject,'Connecting Verb':connecting_verb,'Object Clauses':object_clauses,'Argument Modifiers':arg_modifiers}
        return svo_result
                

    def detect_svo_sentence(self, text):
        list_of_triplets = self.get_oie_triplets(text)
        new_svo = {'sentence':self.text,'triplets':[]}
        # print("\nSentence:", self.text)
        
        for triplet in list_of_triplets:
            svo = self.get_svo_from_triplet(triplet)
            new_svo['triplets'].append(svo)

        return new_svo
    
    def detect_svo(self):
        if self.paragraph == 0:
            self.svo_list.append(self.detect_svo_sentence(self.text))
        else:
            for i in text:
                self.svo_list.append(self.detect_svo_sentence(i))
    
    def display_spo(self):
        for svo_sent in self.svo_list:
            sentence = svo_sent['sentence']
            print("Sentence:", sentence)
            print("***********************************")
            svo_list = svo_sent['triplets']

            for svo in svo_list:
                print("\nSubject Clause:",svo['Subject'])
                print("\nConnecting Verb:", svo['Connecting Verb'])

                if len(svo['Object Clauses']) == 0:
                    print("\nObject Clause(s): None")
                else:
                    print("\nObject Clause(s):")
                    for obj_clause in svo['Object Clauses']:
                        print(obj_clause)
                
                if svo['Argument Modifiers'] == {}:
                    print("\nSentence Modifiers: None")
                else:
                    print("\nSentence Modifiers (as key-value pairs):")
                    for modifier_key, modifier in svo['Argument Modifiers'].items():
                        print("{0}: {1}".format(modifier_key, modifier))
            print("-------------------------------------")

if __name__=='__main__':
    text = "John bought a apple."
    spo = SPO(text)
    spo.detect_svo()
    spo.display_spo()
    # print(spo.svo_list)

    