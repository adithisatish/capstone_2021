import spacy
import sys
import os

if __name__ != "__main__":
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

    def compare_categories(self, verb, object, verb_syn, obj_syn):
        metaphor = False

        cat_verb = self.extract_lexical_categories(verb_syn)
        cat_obj = self.extract_lexical_categories(obj_syn)

        common_categories = cat_verb.intersection(cat_obj)
        if len(common_categories) == 0:
            message = "\nNo overlap => {0} and {1} are METAPHORICAL".format(verb, object)
            metaphor = True
        else:
            main_cat_verb = self.find_main_category(verb, cat_verb, key="verb")
            main_cat_object = self.find_main_category(object, cat_obj, key="noun")

            if main_cat_verb != main_cat_object: # Different main categories
                message = "\nMain categories are different => {0} and {1} are METAPHORICAL".format(verb, object)
                metaphor = True
            else:
                message = "The algorithm cannot determine whether a metaphor exists in this sentence."
                metaphor = False
        
        return (message, metaphor)
    
    def is_verb_metaphor(self):
        verb_syn = self.return_synsets(self.dependencies['ROOT'])
        obj_syn = self.return_synsets(self.dependencies['dobj'])

        verb = self.dependencies['ROOT']
        obj = self.dependencies['dobj']
        
        index_verb = self.index_synset(verb_syn, self.dependencies['ROOT'])
        index_obj = self.index_synset(obj_syn, self.dependencies['dobj'])

        if index_obj == -1 or index_verb == -1:
            if index_obj == -1:
                synset_err = self.dependencies['dobj']
            else:
                synset_err = self.dependencies['ROOT']
            print("Error: Synsets not found for {0}".format(synset_err))
            return ("The algorithm could not detect any metaphors in this sentence!", None)
        
        wup_result = self.wu_palmer_similarity(verb_syn, index_verb, obj_syn, index_obj)
        # print(wup_result)

        if wup_result[0] < 0.3: # Need to set threshold after checking
            metaphor = True
            message = "Metaphor due to low Wu-Palmer score of {0}".format(wup_result[0])
        else:
            message, metaphor = self.compare_categories(verb, obj, verb_syn, obj_syn)

        return (message, metaphor)
    
    def verb_metaphor_util(self, doc):
        for token in doc:
            if token.dep_ == "ROOT":
                self.dependencies['ROOT'] = token.text
        
        sentences = list(doc.sents)
        root_token = sentences[0].root

        for child in root_token.children:
            if child.dep_ == "nsubj":
                self.dependencies['nsubj'] = child.text
            elif child.dep_ == "dobj":
                self.dependencies['dobj'] = child.text
        
        # print(self.dependencies)

        msg, is_metaphor = self.is_verb_metaphor()        
        if is_metaphor == True:
            self.metaphors.append(("{0} and {1} are metaphorical".format(self.dependencies['ROOT'], self.dependencies['dobj']),msg))

    
    def detect_verb_metaphor(self):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []
        self.verb_metaphor_util(doc)
        return self.metaphors


if __name__ == "__main__":
    texts = ["She ate her feelings."]
    VM_Trial = VerbMetaphor(None)

    for text in texts:
        VM_Trial.text = text
        VM_Trial.detect_verb_metaphor()
        print(VM_Trial.metaphors)