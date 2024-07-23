from flask import Flask, request, redirect, url_for, flash, jsonify,render_template
import time
import wave
app=Flask(__name__)
import deepgram
import os
import dotenv
from dotenv import load_dotenv
import google.generativeai as genai
from deepgram import DeepgramClient,PrerecordedOptions,FileSource,SpeakOptions
import time
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model=genai.GenerativeModel("gemini-pro")
stt =DeepgramClient(os.getenv('DG_API_KEY'))
def get_gemini_response(question):
    response=model.generate_content(question)
    return str(response.text)
@app.route('/',methods=['GET','POST'])
def hello():
    text=''
    if request.method=='POST':
        text=str(request.form['transcript'])
        print(text)
        reponse=get_gemini_response(text)
        print(response)
        SPEAK_OPTIONS = {"text": response}
        filename ='static/output.wav'
        try:
            options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
            )
            res=stt.speak.v('1').save(filename, SPEAK_OPTIONS, options)
       except Exception as e:
            print(e)
        print(response)
        exp={
            'a': response 
        }
    else:
        exp={
                'a':''
            }
    current_time = int(time.time())
    return render_template('index.html',result=exp,time=current_time)










if __name__ == "__main__":
    app.run(debug=True)
