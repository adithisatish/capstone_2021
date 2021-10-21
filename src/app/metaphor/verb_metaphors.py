import spacy
import sys
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import numpy 
import pandas as pd
from sklearn.model_selection import train_test_split
import time

# ONLY works for <nsubj> <ROOT VERB> <prep> <dobj/pobj> patterns where <prep> may or may not be present

if __name__  not in ["__main__","verb_metaphors"]:
    sys.path.append("..")
    from app.metaphor.MetaphorUtil import MetaphorUtil
else:
    from MetaphorUtil import MetaphorUtil

nlp = spacy.load("en_core_web_sm")

class VerbMetaphor(MetaphorUtil):

    def __init__(self, text='', sp_w = 0.00, wp_w = 0.00, threshold = 0.00):
        self.text = text
        self.dependencies = {} # Overwritten for every sentence
        self.metaphors = [] # Overwritten for every sentence
        # self.paragraph = paragraph
        # Set all three to optimum by default so direct detection can be done
        self.spacy_weight = sp_w
        self.wupalmer_weight = wp_w
        self.threshold = threshold
        # self.paragraph = paragraph

    def compare_categories(self, verb, object, verb_syn, obj_syn):
        metaphor = False

        cat_verb = self.extract_lexical_categories(verb_syn)
        cat_obj = self.extract_lexical_categories(obj_syn)

        common_categories = cat_verb.intersection(cat_obj)
        if len(common_categories) == 0:
            message = "\nNo overlap => {0} and {1} could be metaphorical".format(verb, object)
            metaphor = True
        else:
            main_cat_verb = self.find_main_category(verb, cat_verb, key="verb")
            main_cat_object = self.find_main_category(object, cat_obj, key="noun")

            if main_cat_verb != main_cat_object: # Different main categories
                message = "\nMain categories are different => {0} and {1} could be metaphorical".format(verb, object)
                metaphor = True
            else:
                message = "The algorithm cannot determine whether a metaphor exists in this sentence."
                metaphor = False
        
        return (message, metaphor)
    
    def verb_metaphor_util(self, doc, code=0):
        for token in doc:
            if token.dep_ == "ROOT":
                nltk_tokens = word_tokenize(self.text)
                pos_tags = pos_tag(nltk_tokens)
                self.dependencies['ROOT'] = token.text
        
        sentences = list(doc.sents)
        root_token = sentences[0].root

        obj_flag = 0
        for child in root_token.children:
            if child.dep_ == "nsubj":
                self.dependencies['nsubj'] = child.text
            else:
                if child.dep_ in ["dobj", "pobj"]:
                    self.dependencies['obj'] = child.text
                    obj_flag = 1
                elif child.dep_ == "prep" and 'obj' not in self.dependencies.keys():
                    prep = child
                    for prep_child in prep.children:
                        if prep_child.dep_ in ["dobj", "pobj"]:
                            self.dependencies['obj'] = prep_child.text
                            obj_flag = 1
        
        if obj_flag == 0:
            self.metaphors.append(("No object found in the sentence => Verb metaphors cannot be found!"))
            return
        
        # print(self.dependencies)
        verb = self.dependencies['ROOT']
        obj = self.dependencies['obj']

        if code == 1: # FINDING OPTIMAL WEIGHTS
                final_score = self.return_similarity_score(verb, obj, code) 
                if final_score > self.threshold:
                    return ("N", final_score)
                else:
                    return ("Y", final_score)
            
        elif code == 2: # ADD SIM TO CSV
            return self.return_similarity_score(verb, obj, code = 2)

        else:
            similarity = self.return_similarity_score(verb, obj)

            if similarity < self.threshold:
                self.metaphors.append(("{0} and {1} could be metaphorical as similarity score is low".format(verb, obj),"Y"))
            else:
                self.metaphors.append(("{0} and {1} are probably not metaphorical as similarity score is high".format(verb, obj),"N"))

        # msg, is_metaphor = self.is_verb_metaphor()        
        # if is_metaphor == True:
        #     self.metaphors.append(("{0} and {1} could be metaphorical".format(self.dependencies['ROOT'], self.dependencies['obj']),msg))

    
    def add_individual_scores(self):
        spacy_scores = []
        wup_scores = []
       
        with open("vm_data/VM_data.txt","r") as file:
            data = list(map(lambda x: x.strip("\n"),file.readlines()))
        
        for text in data:
          doc = nlp(text)
          spac, wup = self.verb_metaphor_util(doc, code = 2)

        spacy_scores.append(spac)
        wup_scores.append(wup)

        # print(spacy_scores)
        data = {"Text": data, "Spacy":spacy_scores, "WUP": wup_scores}
        df = pd.DataFrame(data)

        df.to_csv("vm_data/VM_similarities.csv")

    
    def train(self,data, true_values):

        # train, test = train_test_split()
        # print(data)
        max_acc = 0.00
        best_threshold = 0.00
        optimal_weights = (0.00,0.00)

        new_threshold = 0.00

        for spw in numpy.arange(0,1,0.001):
            wpw = 1 - spw
            self.threshold = new_threshold, 
            self.spacy_weight =spw
            self.wupalmer_weight =wpw

            predictions = []
            scores = []

            for text in data:
                # print()
                # print("---------------------------------------------------")
                # print(text)
                # self.text = text
                doc = nlp(text)
                self.dependencies = {}
                pred,score = self.verb_metaphor_util(doc, code=1)

                predictions.append(pred)
                scores.append(score)

            new_threshold = sum(scores)/len(scores)
            
            acc = self.find_accuracy(predictions, true_values)
            if acc > max_acc:
                max_acc = acc
                best_threshold = new_threshold
                optimal_weights = (spw, wpw)
        
        print("Maximum Accuracy:", max_acc)
        print("Optimal Threshold:", best_threshold)
        print("Optimal Weights:", optimal_weights)

        self.threshold = best_threshold
        self.spacy_weight, self.wupalmer_weight = optimal_weights

    def test(self, data, true_values):
        scores = []
        predictions = []

        for text in data:
                # print()
                # print("---------------------------------------------------")
                # print(text)
                # self.text = text
                doc = nlp(text)
                self.dependencies = {}
                pred,score = self.verb_metaphor_util(doc, code=1)

                predictions.append(pred)
                scores.append(score)

        print("Weights - Spacy: {0} and Wu-Palmer: {1}".format(self.spacy_weight, self.wupalmer_weight))
        print("Threshold:",self.threshold)
        print("Test Accuracy:", self.find_accuracy(predictions, true_values))
    
    def detect_verb_metaphor(self):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []
        self.verb_metaphor_util(doc, code = 0)
        return self.metaphors


if __name__ == "__main__":
    start = time.time()
    print("Start Time:", start)
    print()

    with open("vm_data/VM_data.txt","r") as file:
        data = list(map(lambda x: x.strip("\n"),file.readlines()))

    
    VM_Trial = VerbMetaphor()
    VM_Trial.add_individual_scores()
    
    # df = pd.read_csv("vm_data/VM_similarities.csv")
    # # print(df['Metaphor'])

    # train_X, test_X, train_Y, test_Y = train_test_split(df["Text"],df['Metaphor'], stratify=df["Metaphor"], shuffle=True, test_size=0.10, random_state=42)

    # # print(train_X, train_Y)

    # VM_Trial = VerbMetaphor()
    # VM_Trial.train(train_X, train_Y)
    # print("\n\n")
    # VM_Trial.test(test_X, test_Y)
    # # find_optimal_weights()

    # print()
    # end = time.time()
    # print("End Time:", end)
    # print("Time taken:{0} minutes", (end - start)/60)

    # print(sum(VM_Trial.sim_scores)/len(VM_Trial.sim_scores))