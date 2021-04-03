import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag

def determine_tense_input(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)

sentence = "This restaurant used to be good back in the day."
tense = determine_tense_input(sentence)
print(tense)
