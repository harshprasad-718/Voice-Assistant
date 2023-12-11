import speech_recognition as sr
from gtts import gTTS
import winsound
from pydub import AudioSegment
import pyaudio
import setuptools
import pyautogui
import webbrowser
import os

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

def respond(response_text):
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    winsound.PlaySound("response.wav", winsound.SND_FILENAME)

tasks = []
listeningToTask = False


def main():
    global tasks
    global listeningToTask
    respond("Hello, Harsh. I hope you're having a nice day today.")
    while True:
        command = listen_for_command()
        triggerKeyword = "bologna"
        if command:
            if listeningToTask:
                tasks.append(command)
                listeningToTask = False
                respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
            elif "add a task" in command:
                listeningToTask = True
                respond("Sure, what is the task?")
            elif "list task" in command:
                respond("Sure. Your tasks are:")
                for task in tasks:
                    respond(task)
            elif "take a screenshot" in command:
                pyautogui.screenshot("screenshot.png")
                respond("I took a screenshot for you.")
            elif "open browser" in command:
                respond("Opening Chrome.")
                webbrowser.open("http://www.google.com")
            elif "open youtube" in command:
                respond("Opening YouTube.")
                webbrowser.open("http://www.youtube.com")
            elif "how r u" in command:
                respond("I am Fine. What about You?")
            elif "i am also fine" in command:
                respond("Great. How can I help You.")
            elif "exit" in command:
                respond("Goodbye!")
                deleteResponse()
                break
            else:
                respond("Sorry, I'm not sure how to handle that command.")

def deleteResponse():
    wav_file = 'response.wav'
    mp3_file = 'response.mp3'
    try:
        os.remove(wav_file)
        os.remove(mp3_file)
    except OSError as e:
        print(f"Error deleting files: {e}")

if __name__ == "__main__":
    main()