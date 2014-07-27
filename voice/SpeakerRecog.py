from voiceid.db import GMMVoiceDB
from voiceid import fm
from os.path import splitext
from voiceid.sr import Voiceid
import sys

db = GMMVoiceDB('mydir')

def convertFile(file):
    """Returns the file in wav format. """
    w = fm.file2wav(file)
    basename, extension = splitext(w)
    return basename

def addVoices(samplevoice, speaker):
    """Adds model samplevoice: String and speaker: String to voice db. """
    db.add_model(convertFile(samplevoice), speaker)
    
def bestSpeaker(file):
    """Returns best matching speaker: String in voice db for file: String. """
    v = Voiceid(db, file, True)
    v.extract_speakers()
    clu = v.get_clusters().values()[0]
    if len(clu.get_best_five()) <= 0:
        return None;
    return clu.get_best_five()[0][0]

if __name__ == '__main__':
    if sys.argv[1] == "train":
        addVoices("HarrySample.mp3", "Harry")
        addVoices("RohanSample.mp3", "Rohan")
        addVoices("TomSample.mp3", "Tom")
        addVoices("HeathSample.mp3", "Heath")
    else:
        print bestSpeaker(sys.argv[1])
