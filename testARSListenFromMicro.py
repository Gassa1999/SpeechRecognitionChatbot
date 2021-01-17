# -*- coding: utf-8 -*-
import speech_recognition as sr
import pyttsx3
import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account


DIALOGFLOW_PROJECT_ID = 'test-npeo'
DIALOGFLOW_LANGUAGE_CODE = 'de-DE'
credentials = service_account.Credentials.from_service_account_file("test-npeo-eed7aef6dc7c.json")
SESSION_ID = 'current-user-id'


engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(toSay):
    engine.say(toSay)
    engine.runAndWait()
#https://cloud.google.com/speech-to-text/docs/languages

def speechToText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # listen for 5 seconds and create the ambient noise energy level
        #engine.say('Sprich etwas!')
        print("listening...")
        r.adjust_for_ambient_noise(source)
        data = r.listen(source)
        print("end listen...")
        #, duration=3
    try:
        resultText = r.recognize_google(data, language='de-DE')
        print("-----> Du hast gesagt: ", resultText)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        resultText = "Ich konnte dich nicht verstehen"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        resultText = "Irgendetwas ist schief gelaufen"
    return resultText

def check(text):
    if text == "Ich konnte dich nicht verstehen" or text == "Irgendetwas ist schief gelaufen":
        speak(text + "probiers nochmal")
        return check(speechToText())
    else:
        return text

def detectIntent(queryText):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    # textInput = dialogflow.types.TextInput(text=queryText)
    textInput = dialogflow.types.TextInput(text=queryText, language_code=DIALOGFLOW_LANGUAGE_CODE)
    queryInput = dialogflow.types.QueryInput(text=textInput)
    # print(queryInput)
    try:
        response = session_client.detect_intent(session=session, query_input=queryInput)
    except InvalidArgument:
        raise
    # print("Query text:", response.query_result.query_text)
    # print("Detected intent:", response.query_result.intent.display_name)
    # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    # print("Fulfillment text:", response.query_result.fulfillment_text)
    return response.query_result.fulfillment_text

speak("wie kann ich dir helfen?")
while True:
    resultText = check(speechToText())
    if "exit" in resultText or "beenden" in resultText or "ende" in resultText or "tschüss" in resultText or "aufhören" in resultText  or "ciao" in resultText or "servus" in resultText:
        break
    response = detectIntent(resultText)
    print("-----> Antwort von Dialogflow: ", response)
    speak(response)
