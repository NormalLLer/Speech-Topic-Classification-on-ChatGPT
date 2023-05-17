import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
import speech_recognition as sr
import backend

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/config', methods=['GET', 'POST'])
def configuration():
    if request.method == 'POST':

        input_categories = request.form.get('input-text').strip()
        input_api_key = request.form.get('api-key').strip()

        if input_categories is not None and input_categories != '':

            if backend.init_audio_categories(input_api_key, input_categories):
                session['config'] = 1
                session['api-key'] = input_api_key
                session['categories'] = input_categories
                flash('Configuration of the audio theme is complete!', 'success')
                return redirect(url_for('index'))

            else:
                flash('ChatGPT API key error!', 'warning')
                return redirect(request.url)
        else:
            flash('Categories input format error! Please enter all audio topic categories, separated by spaces!',
                  'warning')
            return redirect(request.url)
    if not session.get('config'):
        return render_template('config.html', config=False)
    else:
        return render_template('config.html', config=True, api_key=session['api-key'],
                               categories=session['categories'])



@app.route('/recognition', methods=['GET', 'POST'])
def recognition():
    if not session.get('config'):
        flash('Please enter configuration first!', 'warning')
        return redirect(url_for('index'))

    transcript = ''
    filename = ''
    category = ''
    if request.method == 'POST':
        print("Speech file uploaded successfully!")

        if "file" not in request.files:
            flash("Please upload your audio file correctly!", 'warning')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash("Please upload your audio file correctly!", 'warning')
            return redirect(request.url)

        transcript, filename = backend.speech_file_to_text(file)
        category = backend.ask_chatgpt(transcript)

    return render_template(
        "recognition.html",
        transcript=transcript,
        filename=filename,
        category=category
    )


if __name__ == '__main__':
    app.run(host='localhost')
