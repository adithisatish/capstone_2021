#split sentence if there is a conjugation as a child of the main verb
#if not, extract root verb and auxilary verb (if exists) from child

"""
Main clause: 
For a sentence to be complete, rather than a fragment, it must include 
a main clause. In English grammar, a main clause (also known as in independent 
clause, superordinate clause, or base clause) is a group of words made up of 
a subject and a predicate that together express a complete concept.

Predicate:
the part of a sentence or clause containing a verb and stating something about the subject
"""

import spacy
nlp = spacy.load("en_core_web_sm")
from nltk import word_tokenize, pos_tag
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd 
import numpy as np 

"""
piano_text = 'He will say that she is ill'
piano_doc = nlp(piano_text)
for token in piano_doc:
    print (token.text, token.dep_, token.pos_)
    if(token.dep_ == 'ROOT'):
        print(token.text)
    elif(token.dep_ == 'aux'):
        print(token.text)
"""

def findVerbs(text): #takes input as single sentence, does not split at conjunction
    text_doc = nlp(text)
    #print(text_doc)
    mainClause = {} #{verb, aux, sub}
    for i in text_doc:
        if(i.dep_ == 'ROOT'):
            mainClause['verb'] = i
            mainClause['aux'] = []
            for j in i.children:
                #print(j, j.dep_, j.tag_)
                if(j.dep_ == 'aux'):
                    mainClause['aux'].append(j.text)
                elif(j.dep_ == 'nsubj'):
                    mainClause['sub'] = j.text
    return mainClause

def tenseDetector(text):
    #print(text)
    #mainclause
    mainClause = findVerbs(text)
    #print(mainClause)
    mainVerb = [mainClause['verb'].text, mainClause['verb'].tag_] # [verb, postag]
    #print(mainVerb)
    auxVerb = mainClause['aux'] #list
    subject = mainClause['sub'] #word
    modals = ['can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must', 'ought']

    tense = ""

    if auxVerb == []: #no auxilary verb sentences: she went/ she came/ she cried etc
        #print("no aux")
        if(mainVerb[1] == 'VBD'):
            tense = "Past Simple"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the past tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(mainVerb[1] in ['VBP', 'VBZ']):
            tense = "Present Simple"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the present tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(mainVerb[1] == 'VBG'):
            tense = "Present Continuous"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the gerund/present participle form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(mainVerb[1] == 'MD'):
            tense = "Future Simple"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is a modal. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
    
    else:
        #future
        for i in modals:
            if i in auxVerb:
                if('be' in auxVerb and mainVerb[1] == 'VBG'):
                    tense = "Future Continuous"
                    explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'be'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                elif(('has' in auxVerb or 'have' in auxVerb) and 'been' in auxVerb and mainVerb[1] == 'VBG'):
                    tense = "Future Perfect Continuous"
                    explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle taking and appears after 'has/have been'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                elif(('have' in auxVerb) and 'been' in auxVerb and mainVerb[1] == 'VBN'):
                    tense = "Future Perfect"
                    explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a past participle and appears after 'have'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                else:
                    tense = "Future Simple"
                    explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the future tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
                return tense

        #past
        if(('was' in auxVerb or 'were' in auxVerb) and mainVerb[1] == 'VBG'):
            tense = "Past Continuous"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'was/were'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif('had' in auxVerb and 'been' in auxVerb and mainVerb[1] == 'VBG'):
            tense = "Past Perfect Continuous"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'had been'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif('had' in auxVerb and mainVerb[1] == 'VBN'):
            tense = "Past Perfect"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a past participle and appears after 'had'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(mainVerb[1] == 'VBD'):
            tense = "Past Simple"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the past tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        
        #present
        elif(('is' in auxVerb or 'am' in auxVerb or 'are' in auxVerb) and mainVerb[1] == 'VBG'):
            tense = "Present Continuous"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'is/am/are'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(('has' in auxVerb or 'have' in auxVerb) and 'been' in auxVerb and mainVerb[1] == 'VBG'):
            tense = "Present Perfect Continuous"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle and appears after 'has/have been'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(('has' in auxVerb or 'have' in auxVerb) and 'been' in auxVerb and mainVerb[1] == 'VBN'):
            tense = "Present Perfect"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a past participle and appears after 'has/have'. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(mainVerb[1] in ['VBP', 'VBZ']):
            tense = "Present Simple"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the present tense form. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        elif(mainVerb[1] == 'VBG'):
            tense = "Present Continuous"
            explanation = "The verb ***{0}*** that describes the action of the subject ***{1}*** is in the form of a gerund/present participle. The verb and the subject comprise the main clause - a group of words made up of a subject and a predicate that together express a complete concept".format(mainVerb[0], subject)
        
    return {'sentence': text, 'tense': tense, 'explanation': explanation}
        
sentence = "The crying child, with tears flowing like streams down both cheeks, managed to settle down only upon getting a chocolate."
print(tenseDetector(sentence))