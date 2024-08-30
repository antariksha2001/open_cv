import cv2
import pyttsx3
from django.http import StreamingHttpResponse
from django.shortcuts import render
import threading

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()
    
    # Run the TTS in a separate thread
    speech_thread = threading.Thread(target=run_speech)
    speech_thread.start()

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Error: Could not open camera.")
        return None
    
    speak("Hello")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Error: Failed to capture image.")
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def camera_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'stream/index.html')
