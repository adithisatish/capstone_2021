import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag

def determine_tense_input(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)
    print(tagged)
    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)

sentence = "I was reading Edgar Allan Poe last night."
tense_dict = determine_tense_input(sentence)
max = 0
tense = ''
for i in tense_dict:
    if tense_dict[i] > max:
        tense = i
        max = tense_dict[i]
print(tense_dict)
print(tense + ' tense')
