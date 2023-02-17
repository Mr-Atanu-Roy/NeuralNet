import threading

import pyttsx3


class Speak(threading.Thread):
    
    def __init__(self, gender, answer):
        self.gender = gender
        self.answer = answer
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            if self.gender == "female":
                engine.setProperty('voice', voices[1].id)
                engine.setProperty('rate', 189)
            else:
                engine.setProperty('voice', voices[0].id)
                engine.setProperty('rate', 191)
                
            engine.say(self.answer)
            engine.runAndWait()
        except Exception as e:
            print(e) 