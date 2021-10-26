from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.util import pr
import requests
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score
import spacy

nlp = spacy.load("en_core_web_md")

class MetaphorUtil:
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
        # print("Return Synsets")
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

    def find_main_category(self, noun, categories, key="noun"):
        # Finding main category of the word using ConceptNet
        main_cat = ''
        max_rel = -99999
        for cat in categories:
            if key in cat:
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

    def spacy_similarity(self, word1, word2):
        words = " ".join([word1, word2])
        tokens = nlp(words)
        token1, token2 = tokens[0], tokens[1]

        if token1.is_oov == False and token2.is_oov == False:
            return token1.similarity(token2)
    
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

    def return_similarities(self, word1, word2):
        # w1_syn = self.return_synsets(word1)
        # w2_syn = self.return_synsets(word2)
        # # print(attr_syn)
        # index_w1 = self.index_synset(w1_syn, word1)
        # index_w2 = self.index_synset(w2_syn, word2)

        # print(index_subj, index_obj)
        sim_result = self.spacy_similarity(word1, word2)
        return sim_result

        if index_w1 == -1 or index_w2 == -1:
            return (sim_result, 0.00)
        else:
            wup_result = self.wu_palmer_similarity(w1_syn, index_w1, w2_syn, index_w2)[0]
            sim_result = self.spacy_similarity(word1, word2)

            return (sim_result, wup_result)
        
    def return_similarity_score(self, word1, word2, code = 1):
        # Driver function to check if two nouns form a noun metaphor

        # sim_result = self.return_similarities(word1, word2)
        sim_result = self.spacy_similarity(word1, word2)

        # if code == 2:
        #     return (sim_result, wup_result)

        weighted_score = self.spacy_weight*sim_result #+ self.wupalmer_weight*wup_result

        return weighted_score

        '''
        if wup_result == None:

            if sim_result > 0.4:
                message = "Similarity score found to be high at {0}".format(sim_result)
                metaphor = "Maybe"
            else:
                message = "Metaphor due to low similarity score of {0}".format(sim_result)
                metaphor = True

            # Can't proceed further because comparison of categories needs synsets again :( => can only check with Spacy)
        else:
            sim_score = max(wup_result, sim_result)
            self.sim_scores.append(sim_score)
            # print("WUP",self.sim_scores)

            if sim_result >= 0.24:
                message, metaphor = self.compare_categories(subj, obj, subj_syn, attr_syn)
            else:
                message = "Metaphor due to low similarity score of {0}".format(sim_result)
                metaphor = True

        return (message,metaphor)'''
    
    def find_accuracy(self, predictions, true_values):
        return accuracy_score(true_values, predictions)

if __name__ == "__main__":
    obj = MetaphorUtil()
    obj.word2vec_similarity("king","queen")
    # syn = obj.return_synsets("woman")
    # print(obj.index_synset(syn))