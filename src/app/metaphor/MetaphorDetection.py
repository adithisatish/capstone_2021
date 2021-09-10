from nltk import text
from noun_metaphors import NounMetaphor

class Metaphor:
    
    def __init__(self, text, paragraph = 0) -> None:
        self.text = text
        self.paragraph = paragraph
        self.noun_metaphors = None
        self.verb_metaphors = None
        self.adj_metaphors = None

    def noun_metaphors(self):
        if self.paragraph == 0:
            NM = NounMetaphor(self.text)
        else:
            NM = NounMetaphor(None)
            for text in self.text:
                NM.text = text