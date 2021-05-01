import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('rWrVkP4wgEwBAj0E84j70OA1mOfRcaGWWaEu6MdW0SXB')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/e772457c-fdc1-473e-b300-f5f4dc57c6f5')

text = 'Team, I know that times are tough! Product '\
    'sales have been disappointing for the past three '\
    'quarters. We have a competitive product, but we '\
    'need to do a better job of selling it!'

def detect_tone(text):
    tone_analysis = tone_analyzer.tone({'text': text}, content_type='application/json').get_result()
    # print(tone_analysis)
    return tone_analysis
    # for key, value in tone_analysis.items():
    #     print(key, value)
    # return json.dumps(tone_analysis, indent=2)

def display_tones(text, tone):
    print("---------------------------\n")
    print("Text:", text)
    print("\nOverall Tone(s):")

    for i in tone['document_tone']['tones']:
        print("\t",i['tone_name'])

    try:
        print()
        print("Individual Tones:\n")
       
        for sentence in tone['sentences_tone']:
            print("\tSentence:",sentence['text'])
            print("\tTone(s):")
            for tones in sentence['tones']:
                print("\t\t",tones['tone_name'])
            print()
    except Exception as e:
        print("\tA single sentence was passed. Thus, the individual tone is the same as overall tone.")

if __name__ == "__main__":
    result = detect_tone("This has been a very bad day")
    # print(type(result))
    display_tones(text,result)
