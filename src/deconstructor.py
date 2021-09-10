from app.alliteration.AlliterationDetector import Alliteration
from app.simile.SimileDetector import Similes
from app.spo.SPODetector import SPO 
from app.simile.SimileDetector import detect_similes
from app.tone.ToneAnalyzer import display_tones, detect_tone
from app.tense.TenseDetector import tenseDetection

mapComponent = {"SPO": SPO, "Alliteration": Alliteration, "Simile": Similes} # Others yet to be mapped