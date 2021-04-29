from src.SPODetector import detect_svo
from src.AlliterationDetector import detect_alliteration
from src.trial import determine_tense_input
import os
import pandas as pd 
import numpy as np 
import sys
import nltk
import time
# from ToneAnalyzer import 

if __name__ == "__main__":

    nltk.download("stopwords")
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
        print()
        print("Menu")
        print("1.\t Detect SPO")
        print("2.\t Detect Alliterations")
        print("3.\t Detect Tense")
        print("4.\t Change Input")
        print("5.\t Exit")
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
            tense = determine_tense_input(text)
            print("Tense:", tense)
            print("\n")
            
            moveon  = input("Press any key to return to Menu")
            time.sleep(1)
        elif choice == 4:
            print()
            text = input("Enter new sentence: ")
            time.sleep(1)
        elif choice == 5:
            exit(0)
        else:
            print("Invalid Choice. Please enter again.")
            time.sleep(1)


