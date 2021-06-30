import requests
from SPODetector import get_oie_triplets, get_svo_from_triplet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Noun-Noun metaphors: check for subj is/are/was/were/will obj => subj and obj should be dissimilar (eg: Her eyes were an ocean)
# Adj-Noun metaphors: check for dissimilarity between adj and noun (eg: she was a sweet child)
# Verb-Noun metaphor: relatedness of verb and noun (eg: The boss barked at his assistant)


def remove_stopwords(text):
    words = stopwords.words("english")
    convert = lambda x: " ".join([i for i in x.split() if i not in words])

    processed_text = convert(text)
    # return processed_text
    if len(processed_text) != 0:
        return processed_text
    else:
        return text


if __name__=="__main__":
    sentence = "My eyes are an ocean of blue"
    metaphor_found = 0
    tokens = word_tokenize(sentence)
    tags = {}
    
    for word, tag in pos_tag(tokens):
        tags[word] = tag
    print(tags)
    print("------------------------")

    OIETriplets = get_oie_triplets(sentence)

    for triplet in OIETriplets:
        svo = get_svo_from_triplet(triplet)
        
        # Noun-Noun Metaphor (comparing subject and object)
        subject = remove_stopwords(svo["Subject"])
        # print("S:", subject)
        objects = []
        for obj in svo["Object Clauses"]:
            objects.append(remove_stopwords(obj))

        for subj in subject.split():
            for objs in objects:
                obj = objs.split()
                for i in obj:
                    if tags[i] in ['JJ','JJS','JJR']:
                        continue
                    path = 'http://api.conceptnet.io//relatedness?node1=/c/en/'+subj+'&node2=/c/en/'+i
                    result = requests.get(path).json()
                    print("The relatedness of {0} and {1} is {2}".format(subj,i,result['value']))
                    if result['value'] <= 0.1:
                        print("Metaphor found")
                        metaphor_found = 1
    
    if metaphor_found==0:
        print("No metaphors")
    