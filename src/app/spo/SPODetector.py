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
        self.modifiers = {'ARGM-LOC': 'Location - relating to place', 'ARGM-TMP': 'Temporal - relating to time', 'ARGM-ADV': 'Adverbial - General Purpose', 
                    'ARGM-DIS': 'Discourse', 'ARGM-MNR':'Manner/Behaviour', 'ARGM-DIR': 'Directional',
                    'ARGM-EXT':'Extent', 'ARGM-PNC': 'Purpose', 'ARGM-CAU': 'Causal - relating to cause', 
                    'ARGM-NEG': 'Negation - a "not" has been seen in the sentence, negating it','ARGM-MOD': 'Modal Verb',
                    'ARGM-GOL':"Goal"}
        self.argmatch = lambda x: re.search('ARG[0-9]:',x)
        self.text = text
        self.paragraph = paragraph
        self.svo_list = []
        
        self.subj_explanation = lambda subj: 'Explanation: "{0}" is a subject/ subject phrase because the sentence is about it. The subject performs the action that is being described in the sentence.'.format(subj)
        self.verb_explanation = lambda verb: 'Explanation: "{0}" is the verb because it is the action or the state of being that is happening in the sentence. The verb functions as a connector between the subject and the object.'.format(verb)
        self.obj_explanation = lambda obj: 'Explanation: "{0}" is the object because it describes the \"whom\" or \"what\" the action is being done to. There can be multiple object clauses in a sentence.'.format(obj)
        self.reference_explanation = lambda ref: ' Additionally, the object clause refers to "{0}".'.format(ref)
    # print(argmatch('ARG1: what'))
        

    # Function to take text as input and return a list of all the different OpenInformationExtraction dictionaries found
    def get_oie_triplets(self, text):
        
        # Initializing the AllenNLP-OIE predictor
        predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz")
        openie = predictor.predict(sentence = text)
        # print(openie)

        triplet_list = []

        # print("\nTotal Number of Extractions Found:",len(openie['verbs']))
        for count, i in enumerate(openie['verbs']): # contains the ARGx, V and ARGM-XXX
            desc = i['description']
            pattern = "\[.*?\]"
            matches = re.findall(pattern=pattern, string=desc)
            print(matches)
            triplet_dict = {}
            for match in matches:
                key,value = match[1:-1].split(": ")
                triplet_dict[key] = value
            
            if triplet_dict != {}:
                triplet_list.append(triplet_dict)

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
        obj_explanations = []
        arg_modifiers = {}
        references = {}
        
        for key, value in triplet.items():
            # key = key.strip()
            try:
                if 'ARGM' in key:
                    arg_modifiers[self.modifiers[key]] = value
            except Exception as e:
                arg_modifiers[key] = "!!New Arg Modifer!!"
            if "R-ARG" in key:
                references["Obj"+key[5:]] = value
                # print("Reference found for object:",key[5:])
                # exit()
            elif 'ARG' in key and key != argmin and 'ARGM' not in key:
                obj_number = key[3:]
                # print(obj_number)
                if "Obj"+obj_number in references:
                    obj_explanation = self.obj_explanation(value) + self.reference_explanation(references["Obj"+obj_number])
                else:
                    obj_explanation = self.obj_explanation(value)
                object_clauses.append(value)
                obj_explanations.append(obj_explanation)

        svo_result = {'Subject':subject,\
                    "Connecting Verb":connecting_verb,\
                    "Object Clauses":object_clauses,\
                    "References":references, \
                    "Argument Modifiers":arg_modifiers, \
                    "Subject Explanation": self.subj_explanation(subject), \
                    "Verb Explanation": self.verb_explanation(connecting_verb),\
                    "Object Explanations": obj_explanations}
        return svo_result
                

    def detect_svo_sentence(self, text):
        list_of_triplets = self.get_oie_triplets(text)
        new_svo = {'sentence':text,'triplets':[]}
        # print("\nSentence:", self.text)

        if list_of_triplets == []:
            return None
        
        for triplet in list_of_triplets:
            svo = self.get_svo_from_triplet(triplet)
            new_svo['triplets'].append(svo)
        
        if new_svo['triplets'] != []:
            return new_svo
        else:
            return None
    
    def detect_spo(self):
        if self.paragraph == 0:
            sent_svo = self.detect_svo_sentence(self.text)
            if sent_svo != None:
                self.svo_list.append(sent_svo)
        else:
            for i in self.text:
                try:
                    sent_svo = self.detect_svo_sentence(i)
                    if sent_svo != None:
                        self.svo_list.append(sent_svo)
                except Exception as e:
                    # print(self.svo_list)
                    print("!! Text that caused error: {0}!!\n".format(i))
                    print(e)
        return self.svo_list
    
    def display_spo(self):
        for svo_sent in self.svo_list:
            sentence = svo_sent['sentence']
            print("Sentence:", sentence)
            print("***********************************")
            svo_list = svo_sent['triplets']

            for svo in svo_list:
                print("\nSubject Clause:",svo['Subject'])
                print(svo['Subject Explanation'])
                print("\nConnecting Verb:", svo['Connecting Verb'])
                print(svo['Verb Explanation'])

                if len(svo['Object Clauses']) == 0:
                    print("\nObject Clause(s): None")
                else:
                    print("\nObject Clause(s):")
                    for i, obj_clause in enumerate(svo['Object Clauses']):
                        print(obj_clause)
                        print(svo["Object Explanations"][i])
                        print()
                
                if svo['Argument Modifiers'] == {}:
                    print("\nSentence Modifiers: None")
                else:
                    print("\nSentence Modifiers (as key-value pairs):")
                    for modifier_key, modifier in svo['Argument Modifiers'].items():
                        print("{0}: {1}".format(modifier_key, modifier))
            print("-------------------------------------")
    
    def execute(self):
        return self.detect_spo()

if __name__=='__main__':
    # text = ['The silence spoke volumes, none of which he wanted to hear.']
    text = "My difficult daily schedule slips by wayside."
    spo = SPO(text)
    spo.detect_spo()
    # spo.display_spo()

    # spo.detect_svo_sentence(text)
    print(spo.svo_list)

    