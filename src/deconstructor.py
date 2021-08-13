from app.alliteration.AlliterationDetector import Alliteration
from app.spo.SPODetector import SPO 
from app.SimileDetector import detect_similes
from app.ToneAnalyzer import display_tones, detect_tone
from app.TenseDetector import tenseDetection

mapComponent = {"SPO": SPO, "Alliteration": Alliteration} # Others yet to be mapped