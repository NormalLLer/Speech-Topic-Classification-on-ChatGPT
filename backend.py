import speech_recognition as sr

import openai

init_prompt = ''
init_message = ''


def ask_chatgpt(message=None):
    global init_prompt, init_message
    if message is not None:
        message = {"role": "user", "content": message}
        messages = [init_message, message]
    else:  # message = None, init ChatGPT
        messages = [init_message]
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=1)
    print(response)
    response = response['choices'][0]['message']['content']
    return response


def speech_file_to_text(speech_file):
    recognizer = sr.Recognizer()
    audioFile = sr.AudioFile(speech_file)
    with audioFile as source:
        data = recognizer.record(source)
    transcript = recognizer.recognize_google(audio_data=data)
    filename = speech_file.filename
    return transcript, filename


def init_audio_categories(api_key, categories):
    global init_prompt, init_message

    openai.api_key = api_key
    init_prompt = f"There are {categories} types of subject categories that define text. " \
                  f"Next, I will enter the text to you, and please return and only " \
                  f"return the topic category that this text is most likely to belong to." \
                  f"e.g.: I input \"President Joe Biden and Republican leaders have expressed " \
                  f"cautious optimism that a deal to raise the US debt ceiling is within reach, " \
                  f"following emergency talks at the White House.\"You should only answer \"News " \
                  f"and current events\" or \"Politics and government\" which is " \
                  f"the exact category of the text. (Note: just an example, which does not " \
                  f"mean that the category of content is actually \"News and current events\" or " \
                  f"\"Politics and government\")"
    init_message = {"role": "user", "content": init_prompt}

    try:
        response = ask_chatgpt()
    except Exception as e:
        return False
    return True


if __name__ == '__main__':  # Test
    init_audio_categories('wrong api', ['a', 'b', 'c'])
    ask_chatgpt('aaaaaaaaabc')
