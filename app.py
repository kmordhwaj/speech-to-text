from flask import Flask, render_template, jsonify
import speech_recognition as sr

app = Flask(__name__)

# Function to recognize speech using SpeechRecognition library
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        # Using Google Web Speech API for speech recognition
        text = recognizer.recognize_google(audio)
        print(text)
        return text.lower()  # Convert to lowercase for easier comparison
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

# Function to check if the recognized text contains any of the keywords
def check_keyword(text, keywords):
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speech_recognition')
def speech_recognition():
    keywords = ["start", "stop"]
    text = recognize_speech()
    if text:
        keyword = check_keyword(text, keywords)
        if keyword:
            # Return JSON response containing the recognized text
            return jsonify(keyword=keyword, text=text)
        else:
            return jsonify(keyword=None, text="Keyword not recognized.")
    else:
        return jsonify(keyword=None, text="Speech not recognized.")

if __name__ == "__main__":
    app.run(debug=True)
