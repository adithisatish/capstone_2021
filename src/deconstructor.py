from app.alliteration.AlliterationDetector import Alliteration
from app.simile.SimileDetector import Simile
from app.spo.SPODetector import SPO 
from app.metaphor.MetaphorDetector import Metaphor
from app.tense.TenseDetector import Tenses
from app.voice.VoiceDetector import Voice
from app.rhyme_scheme.RhymeSchemeDetector import RhymeScheme
from app.tone.ToneDetector import Tone

mapComponent = {"SPO": SPO, "Alliteration": Alliteration, "Simile": Simile, "Metaphor": Metaphor, "Tense":Tenses, "Voice": Voice, "Rhyme Scheme":RhymeScheme, "Tone": Tone}