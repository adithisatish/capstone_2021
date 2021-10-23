# from nltk import text
import sys

from nltk.corpus.reader import verbnet 

if __name__ != "__main__":
    sys.path.append("..")
    from app.metaphor.noun_metaphors import NounMetaphor
    from app.metaphor.verb_metaphors import VerbMetaphor
    from app.metaphor.adjective_metaphors import AdjectiveMetaphor

class Metaphor:
    
    def __init__(self, text, paragraph = 0) -> None:
        self.text = text
        self.paragraph = paragraph
        self.metaphor_list = []
        self.noun_metaphors = []
        self.verb_metaphors = []
        self.adj_metaphors = []

    def find_noun_metaphors(self, text):
        NM = NounMetaphor(text)
        nm_result = NM.detect_noun_metaphor()
        noun_met = {"sentence":text, "noun metaphor": nm_result}
        self.noun_metaphors.append(noun_met)
        return nm_result
    
    def find_verb_metaphors(self, text):
        VM = VerbMetaphor(text)
        vm_result = VM.detect_verb_metaphor()
        verb_met = {"sentence":text, "verb metaphor": vm_result}
        self.verb_metaphors.append(verb_met)
        return vm_result
        # return None

    def find_adj_metaphors(self, text):
        AM = AdjectiveMetaphor(text)
        am_result = AM.detect_adj_metaphor()
        adj_met = {"sentence":text, "adj metaphor": am_result}
        self.adj_metaphors.append(adj_met)
        return am_result
        # return None

    def detect_metaphors(self):
        if self.paragraph == 1:
            for text in self.text:
                new_metaphor_list = {"sentence":text,\
                                     "noun_metaphors": self.find_noun_metaphors(text),\
                                     "verb_metaphors": self.find_verb_metaphors(text),\
                                     "adj_metaphors": self.find_adj_metaphors(text)}
                self.metaphor_list.append(new_metaphor_list)
        
        return self.metaphor_list

    def execute(self):
        return self.detect_metaphors()



if __name__ == "__main__":
    print(__name__)
    
    from noun_metaphors import NounMetaphor
    from verb_metaphors import VerbMetaphor
    from adjective_metaphors import AdjectiveMetaphor
    
    texts = ["My eyes are an ocean of blue",\
            "Today is a prison and I am the inmate.",\
            "The snow is a white blanket.",\
            "Her long hair was a flowing golden river.",\
            "Tom's eyes were ice as he stared at her.",\
            "The children were flowers grown in concrete gardens.",\
            "I am a prisoner.",\
            "She ate her feelings",\
            "My heart dances with daffodils",\
            "His head was spinning with ideas",\
            "It is raining cats and dogs",\
            "Andrew is playing basketball at the college tournament",\
            "They bleed from their sensitive souls.",\
            "The white voice spoke to me and whispered horrible things.",\
            "Forget the grey past and focus on the golden future.",\
            "I met a homeless person in the city.",\
            "His mind was a synthetic sky: blue, blank and cloudless.",\
            "The old woman had a cold heart."]

    
    met_obj = Metaphor(texts, 1)
    nmet = met_obj.execute()
    print(nmet)
    
