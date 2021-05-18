from src.SPODetector import detect_svo
from src.AlliterationDetector import detect_alliteration
from src.ToneAnalyzer import display_tones, detect_tone
from src.TenseDetector import tenseDetection
from src.SimileDetector import detect_similes
import os
import pandas as pd 
import numpy as np 
import sys
import nltk
import time
# from ToneAnalyzer import 

if __name__ == "__main__":

    # nltk.download("stopwords")
    # time.sleep(5)
    
    os.system("CLS")
    print("Welcome to the Sentence Deconstructor!")
    print("----------------------------------------")
    print()
    text = input("Enter your sentence: ")
    
    while True:
        os.system("CLS")
        print("Welcome to the Sentence Deconstructor!")
        print("----------------------------------------")
        print("\nSentence:", text)
        print()
        print("Menu")
        print("1.\t Detect SPO")
        print("2.\t Detect Alliterations")
        print("3.\t Detect Tense")
        print("4.\t Detect Tone")
        print("5.\t Detect Similes")
        print("6.\t Change Input")
        print("7.\t Exit")
        print()
        
        try:
            choice = int(input("Enter your choice: "))
        except:
            print("Invalid choice. Please enter again.")
            time.sleep(1)
            continue

        if choice == 1:
            detect_svo(text)
            print("\n")
            moveon  = input("Press any key to return to Menu")
            time.sleep(1)
        elif choice == 2:
            print("\nSentence:", text)
            # print()
            alliteration = detect_alliteration(text)
            if alliteration != '':
                print("Words in the alliteration:", alliteration)
                print()
            else:
                print("No alliterations found!")
            print("\n")
            
            moveon = input("Press any key to return to Menu")
            time.sleep(1)
        elif choice == 3:
            print("\nSentence:", text)
            # print()
            tense = tenseDetection(text)
            print("Tense:", tense)
            print("\n")
            
            moveon  = input("Press any key to return to Menu")
            time.sleep(1)
        elif choice == 4:
            tone = detect_tone(text)
            # print(tone)
            display_tones(text, tone)
            print("\n")

            moveon  = input("Press any key to return to Menu")
            time.sleep(1)
        elif choice == 5:
            text = text.rstrip()
            detect_similes(text)

            print()
            moveon  = input("Press any key to return to Menu")
            time.sleep(1)
        elif choice == 6:
            print()
            text = input("Enter new sentence: ")
            time.sleep(1)
        elif choice == 7:
            exit(0)
        else:
            print("Invalid Choice. Please enter again.")
            time.sleep(1)


