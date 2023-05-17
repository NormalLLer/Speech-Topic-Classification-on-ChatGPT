import speech_recognition

recognizer = speech_recognition.Recognizer()
print("开始识别!")

has_next = True
while has_next:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio_data=audio, language='zh-CN')
            print(f"识别到的文字: \033[1;35m{text}\033[0m")
    except Exception:
        print("未检测到语音!")
        break
    has_next = eval(input("是否继续? (输入 'True' 或 'False'): "))
print("停止识别!")
