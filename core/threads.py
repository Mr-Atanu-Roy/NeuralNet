import threading

import pyttsx3


class Speak(threading.Thread):
    
    def __init__(self, answer):
        self.answer = answer
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 193)
            engine.say(self.answer)
            engine.runAndWait()
        except Exception as e:
            print(e) 