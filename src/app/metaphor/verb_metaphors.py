import spacy
import sys
import os
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# ONLY works for <nsubj> <ROOT VERB> <prep> <dobj/pobj> patterns where <prep> may or may not be present

if __name__  not in ["__main__","verb_metaphors"]:
    sys.path.append("..")
    from app.metaphor.MetaphorUtil import MetaphorUtil
else:
    from MetaphorUtil import MetaphorUtil

nlp = spacy.load("en_core_web_sm")

class VerbMetaphor(MetaphorUtil):

    def __init__(self, text):
        self.text = text
        self.dependencies = {} # Overwritten for every sentence
        self.metaphors = [] # Overwritten for every sentence
        # self.paragraph = paragraph
        self.sim_scores = []

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
    
    def is_verb_metaphor(self):
        # try:
        verb_syn = self.return_synsets(self.dependencies['ROOT'])
        obj_syn = self.return_synsets(self.dependencies['obj'])

        verb = self.dependencies['ROOT']
        obj = self.dependencies['obj']
        
        index_verb = self.index_synset(verb_syn, self.dependencies['ROOT'])
        index_obj = self.index_synset(obj_syn, self.dependencies['obj'])

        if index_obj == -1 or index_verb == -1:
            sim_result = self.spacy_similarity(verb, obj)

            if sim_result > 0.4:
                message = "Similarity score found to be high at {0}".format(sim_result)
                metaphor = "Maybe"
            else:
                message = "Metaphor due to low similarity score of {0}".format(sim_result)
                metaphor = True

            # Can't proceed further because comparison of categories needs synsets again :( => can only check with Spacy)

            # if index_obj == -1:
            #     synset_err = obj
            # else:
            #     synset_err = subj
            # print("Error: Synsets not found for {0}".format(synset_err))
            # return ("The algorithm could not detect any metaphors in this sentence!", None)
        else:
        
            wup_result = self.wu_palmer_similarity(verb_syn, index_verb, obj_syn, index_obj)
            sim_result = self.spacy_similarity(verb, obj)

            sim_score = max(wup_result, sim_result)
            self.sim_scores.append(sim_score)

            if sim_score < 0.21177: 
                metaphor = True
                message = "Metaphor due to low similarity score of {0}".format(sim_score)
            else:
                message, metaphor = self.compare_categories(verb, obj, verb_syn, obj_syn)

        return (message, metaphor)
    
    def verb_metaphor_util(self, doc):
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

        msg, is_metaphor = self.is_verb_metaphor()        
        if is_metaphor == True:
            self.metaphors.append(("{0} and {1} could be metaphorical".format(self.dependencies['ROOT'], self.dependencies['obj']),msg))

    
    def detect_verb_metaphor(self):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []
        self.verb_metaphor_util(doc)
        return self.metaphors


if __name__ == "__main__":
    texts = ["She ate her feelings.",\
            "Broken in flight, the bird scythed down to the waiting moor.", \
            "He cut his friend off mid sentence.","I carried his name.",\
            "Inflation ate all my savings",\
            "He shot down all of my arguments.",\
            "My heart fills with pleasure",\
            "My heart dances with daffodils.",\
            "The breaking news stirred my excitement",\
            "The views she held were downright disgusting.",\
            "She held views that were downright disgusting.",\
            "His head was spinning with ideas",\
            "It's raining cats and dogs",\
            "She melted into his arms when he apologized.",\
            "She watched in horror as the dead bird floated down from the sky."\
            ] # Inflation has EATEN => error, no synsets for 'eaten'
    VM_Trial = VerbMetaphor(None)

    for text in texts:
        VM_Trial.text = text
        VM_Trial.detect_verb_metaphor()
        print(VM_Trial.metaphors)

    # print(sum(VM_Trial.sim_scores)/len(VM_Trial.sim_scores))