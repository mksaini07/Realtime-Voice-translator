import assemblyai as aai
from googletrans import Translator
translator = Translator()
def translator_fun(text):
    return translator.translate(text, src='en', dest='hi')

aai.settings.api_key="85f8ebb86e224aac997250053cd32f0e"
transcriber=aai.Transcriber()
transcript=transcriber.transcribe("/Users/daksh/Desktop/New Recording.mp3")
hindi = translator_fun(transcript)
print(transcript.text)
print(hindi)      