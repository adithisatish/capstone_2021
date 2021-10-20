import spacy
import sys
import os

if __name__  not in ["__main__","adjective_metaphors"]:
    sys.path.append("..")
    from app.metaphor.MetaphorUtil import MetaphorUtil
else:
    from MetaphorUtil import MetaphorUtil

nlp = spacy.load("en_core_web_sm")

class AdjectiveMetaphor(MetaphorUtil):

    def __init__(self, text):
        self.text = text
        self.dependencies = {} # Overwritten for every sentence
        self.metaphors = [] # Overwritten for every sentence
        # self.paragraph = paragraph

    def compare_categories(self, adj, object, adj_syn, obj_syn):
        metaphor = False

        cat_adj = self.extract_lexical_categories(adj_syn)
        cat_obj = self.extract_lexical_categories(obj_syn)

        common_categories = cat_adj.intersection(cat_obj)
        if len(common_categories) == 0:
            message = "\nNo overlap => {0} and {1} are METAPHORICAL".format(adj, object)
            metaphor = True
        else:
            main_cat_adj = self.find_main_category(adj, cat_adj, key="adj")
            main_cat_object = self.find_main_category(object, cat_obj, key="noun")

            if main_cat_adj != main_cat_object: # Different main categories
                message = "\nMain categories are different => {0} and {1} are METAPHORICAL".format(adj, object)
                metaphor = True
            else:
                message = "The algorithm cannot determine whether a metaphor exists in this sentence."
                metaphor = False
        
        return (message, metaphor)
    
    def is_adj_metaphor(self, noun, adjective):
        adj_syn = self.return_synsets(adjective)
        noun_syn = self.return_synsets(noun)
        
        index_adj = self.index_synset(adj_syn, adjective)
        index_noun = self.index_synset(noun_syn, noun)

        if index_noun == -1 or index_adj == -1:
            if index_noun == -1:
                synset_err = noun
            else:
                synset_err = adjective
            print("Error: Synsets not found for {0}".format(synset_err))
            return ("The algorithm could not detect any metaphors in this sentence!", None)
        
        wup_result = self.wu_palmer_similarity(adj_syn, index_adj, noun_syn, index_noun)
        # print(wup_result)

        if wup_result[0] < 0.3:
            metaphor = True
            message = "Metaphor due to low Wu-Palmer score of {0}".format(wup_result[0])
        else:
            message, metaphor = self.compare_categories(adjective, noun, adj_syn, noun_syn)

        return (message, metaphor)
    
    def adj_metaphor_util(self, doc):
        
        # Find all adj-noun pairs
        noun_adj_pairs = {}
        for chunk in doc.noun_chunks:
            adj = []
            noun = ""
            for tok in chunk:
                if tok.pos_ == "NOUN":
                    noun = tok.text
                if tok.pos_ == "ADJ" or tok.pos_ == "CCONJ":
                    adj.append(tok.text)
            if noun:
                noun_adj_pairs.update({noun:adj})
        
        for noun in noun_adj_pairs:
            for adjective in noun_adj_pairs[noun]:
                msg, is_metaphor = self.is_adj_metaphor(noun, adjective)
                if is_metaphor == True:
                    self.metaphors.append(("{0} and {1} are metaphorical".format(noun, adjective),msg))
    
    def detect_adj_metaphor(self):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []
        self.adj_metaphor_util(doc)
        return self.metaphors


if __name__ == "__main__":
    texts = ["The old woman had a cold heart."]
    AM_Trial = AdjectiveMetaphor(None)

    for text in texts:
        AM_Trial.text = text
        AM_Trial.detect_adj_metaphor()
        print(AM_Trial.metaphors)