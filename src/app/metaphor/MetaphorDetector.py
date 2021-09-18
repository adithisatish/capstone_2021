from nltk import text
import sys 

if __name__ == "deconstructor":
    sys.path.append("..")
    from app.metaphor.noun_metaphors import NounMetaphor

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
        # YET TO BE DONE
        return None

    def find_adj_metaphors(self, text):
        # YET TO BE DONE
        return None

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
    from noun_metaphors import NounMetaphor
    
    texts = ["My eyes are an ocean of blue",\
            "Today is a prison and I am the inmate.",\
            "I am a prisoner","You are a dog!",\
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
            "His memories were cloudy."]

    
    met_obj = Metaphor(texts, 1)
    nmet = met_obj.execute()
    print(nmet)
