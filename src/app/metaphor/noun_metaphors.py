from nltk import text
import numpy
import spacy
import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import time
# print(__name__)

if __name__  not in ["__main__","noun_metaphors"]:
    sys.path.append("..")
    from app.metaphor.MetaphorUtil import MetaphorUtil
else:
    from MetaphorUtil import MetaphorUtil

# Possible grey areas
# 1. What to do when synsets can't be found?
# 2. Check for false positives 
# 3. "You dog!" not equated to "you are a dog" => results in error

# ONLY works with <nsubj> <aux> <det> <attr> pattern

nlp = spacy.load("en_core_web_sm")

class NounMetaphor(MetaphorUtil):

    # Code 0 => Check if sentence is metaphor, Code 1 => Find individual similarity and add to CSV, Code 2 => Find Optimal weights

    def __init__(self, text = "", sp_w = 0.977, wp_w = 0.023, threshold = 0.31047393):
        self.text = text
        self.dependencies = {} # Overwritten for every sentence
        self.metaphors = [] # Overwritten for every sentence
        self.sim_scores =[]

        # Set all three to optimum by default so direct detection can be done
        self.spacy_weight = sp_w
        self.wupalmer_weight = wp_w
        self.threshold = threshold
        # self.paragraph = paragraph

    def compare_categories(self, subj, obj, subj_syn, attr_syn):
        metaphor = False

        cat_subj = self.extract_lexical_categories(subj_syn) # Categories of subject
        cat_attr = self.extract_lexical_categories(attr_syn) # Categories of object
        
        common_categories = cat_subj.intersection(cat_attr)
        if len(common_categories) == 0: # No common categories
            message = "\nNo overlap => {0} and {1} could be metaphorical".format(subj, obj)
            metaphor = True
        else:
            main_cat_subj = self.find_main_category(subj, cat_subj)
            main_cat_attr = self.find_main_category(obj, cat_attr)

            if main_cat_attr != main_cat_subj: # Different main categories
                message = "\nMain categories are different => {0} and {1} could be metaphorical".format(subj, obj)
                metaphor = True
            else:
                message = "The algorithm cannot determine whether a metaphor exists in this sentence."
                metaphor = False
        
        return (message, metaphor)

    def noun_metaphor_util(self, doc, code=0):
        # Utility funtion that extracts pos dependencies for the sentence and extracts the 2 nouns
        # print("Noun Metaphor Util")
        for token in doc:
            if token.dep_ in self.dependencies:
                self.dependencies[token.dep_] += [token]
            else:
                self.dependencies[token.dep_] = [token]

        # print(self.dependencies)
        try:
            sentences = list(doc.sents)
            aux_verb = sentences[0].root

            for child in aux_verb.children:
                if child.dep_ == "nsubj":
                    subj = child.text
                    # subj_syn = self.return_synsets(subj)      

            obj_flag = 0
            for child in aux_verb.children:    
                if child.dep_ == "attr":
                    dependency = "attr"
                    dep = child.text
                    obj_flag = 1
                elif child.dep_ == "acomp":
                    dependency = "acomp"
                    dep = child.text
                    obj_flag = 1
            
            if obj_flag == 0:
                if code == 1:
                    return 0.00
                elif code == 2:
                    return (0.00, 0.00)
                
                return ("No noun metaphors found!",None)
            
            if code == 1: # FINDING OPTIMAL WEIGHTS
                final_score = self.return_similarity_score(subj, dep) 
                if final_score > self.threshold:
                    return ("N", final_score)
                else:
                    return ("Y", final_score)
            
            elif code == 2: # ADD SIM TO CSV
                return self.return_similarity_score(subj, dep, code = 2)

            else:
                similarity = self.return_similarity_score(subj, dep)

                if similarity < self.threshold:
                    self.metaphors.append(((subj, dep),"Y", similarity))
                else:
                    self.metaphors.append(((subj, dep),"N", similarity))



            # msg, is_metaphor = self.is_noun_metaphor(dep, subj_syn, subj)
            
            # if is_metaphor == True:
            #     self.metaphors.append(("{0} and {1} could be metaphorical".format(subj, dep),msg))
            # elif is_metaphor == "Maybe":
            #     self.metaphors.append(("{0} and {1} seem to be similar so they might not be metaphorical".format(subj, dep), msg))

        except Exception as e:
            print("Error:",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return None

        # return self.metaphors
    
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
                pred,score = self.noun_metaphor_util(doc, code=1)

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
                pred,score = self.noun_metaphor_util(doc, code=1)

                predictions.append(pred)
                scores.append(score)

        print("Weights - Spacy: {0} and Wu-Palmer: {1}".format(self.spacy_weight, self.wupalmer_weight))
        print("Threshold:",self.threshold)
        print("Test Accuracy:", self.find_accuracy(predictions, true_values))

    def detect_noun_metaphor(self):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []
        
        self.noun_metaphor_util(doc, code = 0)
        return self.metaphors

if __name__ == "__main__":

    NM = NounMetaphor(text="She was a lion in the battlefield")
    print(NM.detect_noun_metaphor())


    # REFER TO NM_STATS FOR PERFORMANCE METRICS
    # start = time.time()
    # print("Start Time:", start)
    # print()
    # df = pd.read_csv("nm_data/nounmetaphors.csv")
    # # print(df['Metaphor'])

    # train_X, test_X, train_Y, test_Y = train_test_split(df["Text"],df['Metaphor'], stratify=df["Metaphor"], shuffle=True, test_size=0.10, random_state=42)

    # # print(train_X, train_Y)

    # NM_Trial = NounMetaphor()
    # NM_Trial.train(train_X, train_Y)
    # print("\n\n")
    # NM_Trial.test(test_X, test_Y)
    # # find_optimal_weights()

    # print()
    # end = time.time()
    # print("End Time:", end)
    # print("Time taken:{0} minutes".format((end - start)/60))