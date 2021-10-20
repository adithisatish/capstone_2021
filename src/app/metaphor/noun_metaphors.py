import spacy
import sys
import os

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
        self.wup_scores =[]
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
    
    def is_noun_metaphor(self, obj, subj_syn, subj):
        # Driver function to check if two nouns form a noun metaphor
        # print("Is Noun Metaphor")
        attr_syn = self.return_synsets(obj)
        # print(attr_syn)
        index_subj = self.index_synset(subj_syn, subj)
        index_obj = self.index_synset(attr_syn, obj)

        # print(index_subj, index_obj)

        if index_obj == -1 or index_subj == -1:
            sim_result = self.spacy_similarity(subj, obj)

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
            sim_result = self.wu_palmer_similarity(subj_syn, index_subj, attr_syn, index_obj)[0]

            # print()
            # print(subj, ",", obj)
            # print("WU-Palmer Score:",wup_result)

            self.wup_scores.append(sim_result)
            # print("WUP",self.wup_scores)

            if sim_result >= 0.24:
                message, metaphor = self.compare_categories(subj, obj, subj_syn, attr_syn)
            else:
                message = "Metaphor due to low Wu-Palmer score of {0}".format(sim_result)
                metaphor = True

        return (message,metaphor)

    def noun_metaphor_util(self, doc):
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
                return ("No noun metaphors found!",None)

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

    def detect_noun_metaphor(self):
        # Driver function
        doc = nlp(self.text)
        self.dependencies = {}
        self.metaphors = []
        self.noun_metaphor_util(doc)
        return self.metaphors

if __name__ == "__main__":
    # text = "Today is a prison and I am the inmate => figure out a logical split
    texts = ["My eyes are an ocean of blue",\
            "Today is a prison and I am the inmate.",\
            "I am a prisoner","You dog!",\
            "The snow is a white blanket.",\
            "Her long hair was a flowing golden river.",\
            "Tom's eyes were ice as he stared at her.",\
            "The children were flowers grown in concrete gardens.",\
            "The falling snowflakes are dancers.",\
            "The calm lake was a mirror.",\
            "John's suggestion was just a Band-Aid for the problem.",\
            "Chaos is a friend of mine.",\
            "His eyes are saucers.",\
            "She is an early bird.",\
            "His memories were cloudy.", "All the world is a stage"]

    NM_Trial = NounMetaphor(None)

    for text in texts:
        print()
        print("---------------------------------------------------")
        print(text)
        NM_Trial.text = text
        NM_Trial.detect_noun_metaphor()
        print(NM_Trial.metaphors)
    
    # print("WUP SCORE AVERAGE:", sum(NM_Trial.wup_scores)/len(NM_Trial.wup_scores)) = 0.2308
    # doc = nlp(texts[0])

    # for token in doc:
    #     print(token.text, token.dep_)

    #     except Exception as e:
    #         print("\n")
    #         print(text)
    #         print(e)
    #         print("----------------")
    # COCA Collocation Dataset required

    # print("MCA:", main_cat_attr)
    # print("MCS:",main_cat_subj)
        
    # pass

