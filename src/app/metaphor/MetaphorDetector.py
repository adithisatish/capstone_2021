from nltk import text
from noun_metaphors import NounMetaphor

class Metaphor:
    
    def __init__(self, text, paragraph = 0) -> None:
        self.text = text
        self.paragraph = paragraph
        self.noun_metaphors = []
        self.verb_metaphors = []
        self.adj_metaphors = []

    def find_noun_metaphors(self):
        if self.paragraph == 0:
            NM = NounMetaphor(self.text)
        else:
            NM = NounMetaphor(None)
            for text in self.text:
                NM.text = text
                nm_result = {"sentence":text, "noun_metaphors": NM.detect_noun_metaphor()}
                self.noun_metaphors.append(nm_result)
        
        return self.noun_metaphors


if __name__ == "__main__":
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
    nmet = met_obj.find_noun_metaphors()
    print(nmet)
