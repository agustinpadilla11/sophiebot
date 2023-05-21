import speech_recognition as sr
import openai
from gtts import gTTS
from pygame import mixer
import os
import time as ti
import random
from flask import Flask, render_template, request

openai.api_key = "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"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index9.html')

# definimos cómo vamos a tomar el audio del mic y pasarlo a texto
def transformar_audio_a_texto():
    r = sr.Recognizer()

    with sr.Microphone() as origen:
        r.pause_threshold = 0.5
        print("Let Go!")
        audio = r.listen(origen)
        try:
            pedido = r.recognize_google(audio, language="en-GB")
            print("You: " + pedido)
            return pedido

        except sr.UnknownValueError:
            print("Ups, No entendi!")
            return "Ups, No entendi!"

        except sr.RequestError:
            print("Ups, no hay servicio!")
            return "Ups, no hay servicio!"

        except:
            print("Ups, algo salio mal!")
            return "Ups, algo salio mal!"


# Definimos cómo dado un texto (mensaje) lo pasamos a audio
def hablar_en(mensaje):
    volume = 0.7
    tts = gTTS(mensaje, lang="en", slow=False)
    ran = random.randint(0, 9999)
    filename = 'TempEn' + format(ran) + '.mp3'
    tts.save(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.set_volume(volume)
    mixer.music.play()

    while mixer.music.get_busy():
        ti.sleep(0.3)

    mixer.quit()
    os.remove(filename)


# definimos la comunicacion con OpenAI
# Conversation es el preseteo que le damos a chatgpt para que tome el rol que queremos
def traer_respuesta(question):
    conversation = "Sophie es más que una profesora de inglés, ella es una gran amiga." \
                    "No tengas miedo ni vergüenza alguna, Sophie está aquí para ayudarte a practicar tanto tu inglés escrito como hablado." \
                    "Además de brindarte correcciones gramaticales, Sophie te proporcionará ejercicios, formas de aprendizaje, consejos para conjugar verbos y todo lo necesario para que puedas mejorar tus habilidades en el idioma." \
                    "Pero lo más importante, Sophie quiere que te diviertas mientras charlas con ella de manera divertida y amigable." \
                    "¡Aprovecha esta oportunidad para aprender y pasar un buen rato con tu amiga Sophie!"

    conversation += "\nYou: " + question + "\nSophie:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation,
        temperature=0.5,
        max_tokens=2000,
        top_p=0.8,
        frequency_penalty=0.2,
        presence_penalty=0.0,
        stop=["\n", " You:", " Sophie:"]
    )
    answer = response.choices[0].text.strip()
    return answer


@app.route('/talk', methods=['POST'])
def talk():
    question = transformar_audio_a_texto().lower()
    answer = traer_respuesta(question)
    hablar_en(answer)
    return answer

@app.route('/send', methods=['POST'])
def send():
    question = request.form['question'].lower()
    answer = traer_respuesta(question)
    hablar_en(answer)
    return answer
    #return render_template('index5.html', answer=answer)

if __name__ == '__main__':
    app.run()