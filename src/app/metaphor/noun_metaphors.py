import spacy
import sys
import os
import pandas as pd

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

    def __init__(self, text):
        self.text = text
        self.dependencies = {} # Overwritten for every sentence
        self.metaphors = [] # Overwritten for every sentence
        self.sim_scores =[]
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
    
    def return_similarities(self, obj, subj_syn, subj):
        attr_syn = self.return_synsets(obj)
        # print(attr_syn)
        index_subj = self.index_synset(subj_syn, subj)
        index_obj = self.index_synset(attr_syn, obj)

        # print(index_subj, index_obj)

        if index_obj == -1 or index_subj == -1:
            sim_result = self.spacy_similarity(subj, obj)
            return (sim_result, None)
        else:
            wup_result = self.wu_palmer_similarity(subj_syn, index_subj, attr_syn, index_obj)[0]
            sim_result = self.spacy_similarity(subj, obj)

            return (sim_result, wup_result)
        
    def is_noun_metaphor(self, obj, subj_syn, subj):
        # Driver function to check if two nouns form a noun metaphor
        # print("Is Noun Metaphor")
        attr_syn = self.return_synsets(obj)
        # print(attr_syn)
        index_subj = self.index_synset(subj_syn, subj)
        index_obj = self.index_synset(attr_syn, obj)

        # print(index_subj, index_obj)

        sim_result, wup_result = self.return_similarities(self, obj, subj_syn, subj)

        if wup_result == None:

            if sim_result > 0.4:
                message = "Similarity score found to be high at {0}".format(sim_result)
                metaphor = "Maybe"
            else:
                message = "Metaphor due to low similarity score of {0}".format(sim_result)
                metaphor = True

            # Can't proceed further because comparison of categories needs synsets again :( => can only check with Spacy)
        else:
            sim_score = max(wup_result, sim_result)
            self.sim_scores.append(sim_score)
            # print("WUP",self.sim_scores)

            if sim_result >= 0.24:
                message, metaphor = self.compare_categories(subj, obj, subj_syn, attr_syn)
            else:
                message = "Metaphor due to low similarity score of {0}".format(sim_result)
                metaphor = True

        return (message,metaphor)

    def noun_metaphor_util(self, doc, test=0):
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
                    subj_syn = self.return_synsets(subj)      

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
                if test == 1:
                    return (None, None)
                
                return ("No noun metaphors found!",None)
            
            if test == 1:
                return self.return_similarities(dep, subj_syn, subj)

            msg, is_metaphor = self.is_noun_metaphor(dep, subj_syn, subj)
            
            if is_metaphor == True:
                self.metaphors.append(("{0} and {1} could be metaphorical".format(subj, dep),msg))
            elif is_metaphor == "Maybe":
                self.metaphors.append(("{0} and {1} seem to be similar so they might not be metaphorical".format(subj, dep), msg))

        except Exception as e:
            print("Error:",e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return None

        # return self.metaphors

    def detect_noun_metaphor(self, test = 0):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []

        if test == 1:
            return self.noun_metaphor_util(doc, test)
        
        self.noun_metaphor_util(doc)
        return self.metaphors

if __name__ == "__main__":
    # text = "Today is a prison and I am the inmate => figure out a logical split
    
    with open("nm_data/NM_data.txt","r") as file:
        data = list(map(lambda x: x.strip("\n"),file.readlines()))

    # print(data)

    NM_Trial = NounMetaphor(None)

    spacy_scores = []
    wup_scores = []

    for text in data:
        # print()
        # print("---------------------------------------------------")
        # print(text)
        NM_Trial.text = text
        spac, wup = NM_Trial.detect_noun_metaphor(test=1)
        spacy_scores.append(spac)
        wup_scores.append(wup)

    # # print(spacy_scores)
    data = {"Text": data, "Spacy":spacy_scores, "WUP": wup_scores}
    df = pd.DataFrame(data)

    df.to_csv("nm_data/NM_similarities.csv")