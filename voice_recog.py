import speech_recognition as sr

def find_airpods_microphone():
    microphones = sr.Microphone.list_microphone_names()
    print("Mics found:")
    for i, mic in enumerate(microphones):
        print(f"{i}: {mic}")

    for i, mic in enumerate(microphones):
        if "AirPods" in mic:
            print("AirPods found")
            return i

    print("No AirPods")
    return None

def recognize_voice_with_airpods():
    mic_index = find_airpods_microphone()
    if mic_index is None:
        print("No mic")
        return

    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=mic_index) as source:
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Didn't get")
            return None
        except sr.RequestError:
            print("Error")
            return None
        except sr.WaitTimeoutError:
            print("No input")
            return None

if __name__ == "__main__":
    print("Starting...")
    recognize_voice_with_airpods()
