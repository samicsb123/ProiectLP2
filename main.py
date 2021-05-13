"""
Resurse folosite:
https://realpython.com/python-speech-recognition/
https://pypi.org/project/SpeechRecognition/
https://www.youtube.com/watch?v=K_WbsFrPUCk
https://pypi.org/project/pyttsx3/
https://docs.python.org/3/library/re.html
https://docs.python.org/3/library/webbrowser.html
"""

#Dam import la libariile de mai jos
import speech_recognition as sr
import os
import pyttsx3
import urllib.request
import re
import webbrowser


#Am creat o functie care urmareste pattern-ul de la youtube ca sa dea play la o melodie.
#Nu am gasit functia in vreo librarie care sa imi mearga, asa ca am facut-o de la 0.
def playyt(text):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + text.replace("play",'').replace(" ",''))
    video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
    video_url = "https://www.youtube.com/watch?v=" + video_ids[0]
    talk("Playing" + text.replace('play',''))
    webbrowser.open(video_url)

#Am creat o functie care foloseste ne ofera un output vocal, un feedback.
def talk(text):
    engine.say(text)
    engine.runAndWait()


dict = {
    "play + (song)": "Da play la o melodie",
    "Shutdown computer": "O sa inchida calculatorul",
    "Restart computer": "O sa dea restart la calculator"
}
engine = pyttsx3.init()
#Urmatoarele 2 linii de cod am schimbat vocea de baiat in cea de femeie
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


talk('What can i do for you?')
print(dict)


#Folosim microfonul ca si sursa, si afisam "Say Anything".
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak anything:")
    #Folosim functia listen ca microfonul nostru (source) sa fie ascultat
    #si stocat intr-o variabila (audio).
    audio = r.listen(source)

    try:
        #Folosim functia recognize_google ca sa recunoasca vocea noastra cu ajutorul lui google, si am schimbat limba
        #in romana.
        #Dupa am stocat asta intr-o variabila numita "text"
        text = r.recognize_google(audio)

        #Am folosit un if ca sa vada scriptul pe ce comanda de sistem sa mearga.
        if "play" in text:
            playyt(text)

        elif "Shut down computer" == text:
            os.system("shutdown /s")
            talk("I will shutdown the computer in less than a minute")
        elif "Restart computer" == text:
            os.system("shutdown /r")
            talk("I will restart the computer in less than a minute")


    #In cazul in care functia recognize nu recunoaste o voce se trece pe "expect"
    #si printeaza ca nu putem sa recunoastem vocea.
    except:
        talk("Sorry I could not recognize")


