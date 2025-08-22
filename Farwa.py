import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "f1216fba065a4f93aec018abd5c987a4"


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(api_key="sk-proj-")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Farwa. Give short responses."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:  # only first 5 headlines
                speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Siri....")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # reduce background noise
        while True:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                word = recognizer.recognize_google(audio)
                print("Heard:", word)

                # Wake words
                wake_words = ["siri", "ok siri", "siri"]

                if any(w in word.lower() for w in wake_words):
                    speak("Yes Farwa?")
                    print("Assistant activated. Listening for command...")

                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    processCommand(command)

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("API unavailable; {0}".format(e))
            except sr.WaitTimeoutError:
                print("Listening timed out")
            except Exception as e:
                print("Unexpected error:", e)
