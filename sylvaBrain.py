import os, sys
import json
import openai
from enum import Enum
from google.cloud import texttospeech
from pygame import mixer as pym
import random


#Load all the APIs!
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.path.join(sys.path[0],'GoogleTTS.json')
f = open(os.path.join(sys.path[0],'api_data.json'))
data = json.load(f)
openai.api_key = data['openai_token']
f.close()

class Sentiment(Enum):
    neutral = "neutral"
    positive = "positive"
    sad = "sad"
    mad = "mad"
    surprised = "surprised"
    funny = "funny"


class Sylva:
    def __init__(self, model_engine="gpt-3.5-turbo"):
        self.model_engine = model_engine

    def respond(self, author, message):
        prompt = f"{author}: {message}\nSylva the vtuber:"
        print(prompt)
        response = openai.ChatCompletion.create(
            model=self.model_engine,
            messages=[
                {"role":"user","content":prompt},
                {"role":"system","content":"Your name is Sylva and you are a catgirl who attends high school in Tokyo.  You should act like a vtuber when you respond"}
            ],
        )
        return response['choices'][0]['message']['content']
    
    def sentimentAnalysis(self, answer):

        prompt = f"Please analyze the sentiment of the following text and provide a one word output selected from the following list: neutral, positive, sad, mad, surprised, funny.  Your answer be exactly one word long. \n\nText: {answer}"
        completions  = openai.Completion.create(
            engine='text-babbage-001',
            prompt=prompt,
            n=1,
            stop=None,
            temperature=0.7,
        )

        response=completions.choices[0].text.strip()

        for sentiment in Sentiment:
            if(response.find(sentiment.name)!= -1):
                return sentiment.name
        
        return random.choice([Sentiment.neutral.name,Sentiment.positive.name])
    
    def synthesize_text(self, message):
        """Synthesizes speech from the input string of text."""

        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=message)
        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )
        audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
        filename="voice.mp3"
        with open(filename, "wb") as out:
            out.write(response.audio_content)
        pym.init()
        pym.music.load(filename)
        pym.music.play()
        while pym.music.get_busy()==True:
            continue
        pym.music.unload()