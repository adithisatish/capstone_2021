from nltk import stem
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.util import pr
import requests
from nltk.corpus import stopwords
import spacy

# Possible grey areas
# 1. What to do when synsets can't be found?
# 2. Check for false positives 
# 3. "You dog!" not equated to "you are a dog" => results in error

nlp = spacy.load("en_core_web_sm")

class NounMetaphor:

    def __init__(self, text):
        self.text = text
        self.dependencies = {} # Overwritten for every sentence
        self.metaphors = [] # Overwritten for every sentence
        # self.paragraph = paragraph

    def remove_stopwords(self, text):
        # Function that removes stopwords from a sentence
        words = stopwords.words("english")
        convert = lambda x: " ".join([i for i in x.split() if i not in words])

        processed_text = convert(text).lower()
        # return processed_text
        if len(processed_text) != 0:
            return processed_text
        else:
            return text

    def return_synsets(self, word):
        # Function that returns wordnet synsets for a particular word
        synsets = wn.synsets(word)
        return synsets

    def extract_lexical_categories(self, synsets):
        # Function to extract lexical categories given the synsets for a word
        # synsets = wn.synsets(word)
        categories = set()
        if len(synsets) != 0:
            for synset in synsets:
                name = str(synset.lexname())
                categories.add(name)
                # definition = str(synset.definition())
                # print(name, definition)
        return categories

    def find_main_category(self, noun, categories):
        # Finding main category of the word using ConceptNet
        main_cat = ''
        max_rel = -99999
        for cat in categories:
            if "noun" in cat:
                current_category = cat[5:]
                path = 'http://api.conceptnet.io//relatedness?node1=/c/en/'+noun+'&node2=/c/en/'+current_category
                result = requests.get(path).json()
                # print(current_category, result['value'])
                if result['value'] > max_rel:
                    max_rel = result['value']
                    main_cat = current_category
        
        return main_cat

    def wu_palmer_similarity(self, syn1, index1, syn2, index2):
        # Computes Wu-Palmer Similarity for two synsets and returns the score as well as the shortest path distance
        # print(syn1)
        # print(syn2)
        wu_palmer_score = syn1[index1].wup_similarity(syn2[index2])
        shortest_path_distance = syn1[index1].shortest_path_distance(syn2[index2])

        return (wu_palmer_score, shortest_path_distance)
    
    def index_synset(self, synset, name):
        # Returns the index of the right synset to use after comparing with stemmed and lemmatized forms
        ps = PorterStemmer()
        lem = WordNetLemmatizer()
        stemmed_name = ps.stem(name)
        lemmatized_name = lem.lemmatize(name)
        index = -1
        for i, syn in enumerate(synset):
            syn_name = syn.name().split(".")[0]
            stemmed_syn = ps.stem(syn_name)
            lemmatized_syn = lem.lemmatize(syn_name)
            # print("Stemming:",stemmed_name, stemmed_syn)
            # print("Lemmatized:", lemmatized_name, lemmatized_syn)
            if (name.lower() == syn_name.lower() or stemmed_name == stemmed_syn or lemmatized_name == lemmatized_syn) and index == -1:
                index = i 
        return index

    def compare_categories(self, subj, obj, subj_syn, attr_syn):
        # Extracts and compares the categories of the two noun 
        metaphor = False

        cat_subj = self.extract_lexical_categories(subj_syn) # Categories of subject
            # for attr in self.dependencies[dependency]:
        cat_attr = self.extract_lexical_categories(attr_syn) # Categories of object
        # print(cat_subj, cat_attr)

        common_categories = cat_subj.intersection(cat_attr)
        if len(common_categories) == 0: # No common categories
            message = "\nNo overlap => {0} and {1} are METAPHORICAL".format(subj, obj)
            metaphor = True
        else:
            main_cat_subj = self.find_main_category(subj, cat_subj)
            main_cat_attr = self.find_main_category(obj, cat_attr)

            if main_cat_attr != main_cat_subj: # Different main categories
                message = "\nMain categories are different => {0} and {1} are METAPHORICAL".format(subj, obj)
                metaphor = True
            else:
                # What to do here??

                message = "The algorithm cannot determine whether a metaphor exists in this sentence."
                metaphor = False
        
        return (message, metaphor)
    
    def is_noun_metaphor(self, obj, subj_syn, subj):
        # Driver function to check if two nouns form a noun metaphor
        attr_syn = self.return_synsets(obj)
        # print(attr_syn)
        index_subj = self.index_synset(subj_syn, subj)
        index_obj = self.index_synset(attr_syn, obj)

        # print(index_subj, index_obj)

        if index_obj == -1 or index_subj == -1:
            print("Error: Synsets not found")
            return (None, None)
        
        wup_result = self.wu_palmer_similarity(subj_syn, index_subj, attr_syn, index_obj)

        # print()
        # print(subj, ",", obj)
        # print("WU-Palmer Score:",wup_result)

        if wup_result[0] >= 0.3:
            message, metaphor = self.compare_categories(subj, obj, subj_syn, attr_syn)
        else:
            message = "Metaphor due to low Wu-Palmer score"
            metaphor = True

        return (message,metaphor)

    def noun_metaphor_util(self, doc):
        # Utility funtion that extracts pos dependencies for the sentence and extracts the 2 nouns
        for token in doc:
            if token.dep_ in self.dependencies:
                self.dependencies[token.dep_] += [token.text]
            else:
                self.dependencies[token.dep_] = [token.text]

        # print(self.dependencies)
        try:
            for subj in self.dependencies['nsubj']:
                subj_syn = self.return_synsets(subj)
                # print(subj_syn)

                if "attr" in self.dependencies:
                    dependency = "attr"
                elif "acomp" in self.dependencies:
                    dependency = "acomp"
                for dep in self.dependencies[dependency]:
                    # print(dep, subj_syn, subj, dependency)
                    msg, is_metaphor = self.is_noun_metaphor(dep, subj_syn, subj, dependency)
                    
                    if is_metaphor == True:
                        self.metaphors.append(("{0} and {1} are metaphorical".format(subj, dep),msg))

        except Exception as e:
            print("Error:",e)
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
            "His memories were cloudy."]

    NM_Trial = NounMetaphor(None)

    for text in texts:
        print()
        print("---------------------------------------------------")
        print(text)
        NM_Trial.text = text
        NM_Trial.detect_noun_metaphor()
        print(NM_Trial.metaphors)
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

