import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag

def determine_tense_input(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)
    countPast = 0
    countPresent = 0
    countFuture = 0
    for word in tagged:
        if word[1] == "MD":
            countFuture += 1
        elif word[1] in ["VBP", "VBZ","VBG"]:
            countPresent += 1
        elif word[1] in ["VBD", "VBN"]:
            countPast +=1
    tense_dict = dict()
    tense_dict["Past"] = countPast
    tense_dict["Present"] = countPresent
    tense_dict["Future"] = countFuture
    max = 0
    tense = ''
    for i in tense_dict:
        if tense_dict[i] > max:
            tense = i
            max = tense_dict[i]
    return tense

if __name__ == "__main__":
    sentence = "This restaurant used to be good back in the day."
    tense = determine_tense_input(sentence)
    print(tense + ' tense')
