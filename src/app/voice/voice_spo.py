from app.spo.SPODetector import get_oie_triplets, get_svo_from_triplet

class Voice_Spo:
    def __init__(self, sentence): 
        self.text = sentence

    def voiceSpoDetection(self):
        text = "She returned the computer after noticing the damage."
        triplets = get_oie_triplets(text)
        for triplet in triplets:
            svo = get_svo_from_triplet(triplet)
        print(svo)

        subject = svo['Subject']
        print('subject index: ')
        sub_index = text.index(subject)
        print(sub_index)

        objectClause = svo['Object Clauses']
        obj = ''
        for i in objectClause:
            obj = obj + i
        print('object index: ')
        obj_index = text.index(obj)
        print(obj_index)

        voice = ""
        if sub_index < obj_index:
            voice = "Active"
        if obj_index < sub_index:
            voice = "Passive"
        
        output = dict()
        output['sentence'] = sentence
        output['voice'] = voice
    
    def execute(self):
    # Driver function
        return self.voiceDetection()

if __name__ == "__main__":
    sentence = "Jack attended the program"
    voice_obj = Voice_Spo(sentence)
    #s = sim_obj.detect_similes()
    s1=voice_obj.execute()
    print(s1)