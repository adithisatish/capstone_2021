from app.alliteration.AlliterationDetector import Alliteration
from app.simile.SimileDetector import Similes
from app.spo.SPODetector import SPO 
from app.metaphor.MetaphorDetector import Metaphor
from app.tense.TenseDetector import Tenses
from app.voice.voice_spo import Voice_Spo
from app.rhyme_scheme.RhymeSchemeDetector import RhymeScheme

mapComponent = {"SPO": SPO, "Alliteration": Alliteration, "Simile": Similes, "Metaphor": Metaphor, "Tense":Tenses, "Voice": Voice_Spo, "Rhyme Scheme":RhymeScheme} # Others yet to be mapped