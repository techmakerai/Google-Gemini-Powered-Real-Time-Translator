# Google Gemini-Powered Real-Time Language Translator with Audio
# Tested and working on Windows 11. 
# By TechMakerAI on YouTube
# 
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pygame import mixer
from datetime import date
 
mixer.init()
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# set Google Gemini API key as a system environment variable or add it here
# genai.configure(api_key="Your-Google-API-key")

today = str(date.today())
 
# Name of Google Generative AI Model
model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat()

# Set up the Gemini Pro model
gf = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 128,
    } 

safety_settings=[
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

# text to speech function
 
def speak_text(text):
    
    mp3audio = BytesIO() 
    
    tts = gTTS(text, lang='zh-CN', tld = 'us')     
    
    tts.write_to_fp(mp3audio)

    mp3audio.seek(0)

    mixer.music.load(mp3audio, "mp3")
    mixer.music.play()

    while mixer.music.get_busy():
        pass
    
    mp3audio.close()
    
# save conversation to a log file 
def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a", encoding='utf-8') as f:
        f.write(text + "\n")
        f.close 

# define default language to work with the AI model 
slang = "en-EN"

# Main function  
def main():
    global today, openaitts, model, chat, slang, gf, safety_settings 
    
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold=False
    rec.energy_threshold = 400 

    request = '''You are a real-time language translator. 
        Your task is to translate the speech from English to Chinese. 
        Please refrain from adding any words or sentences after you 
        finish the translation, your role is to translate only. '''
    response = chat.send_message(request)   
 
    # while loop for interaction with AI model  
 
    while True:     
        
        with mic as source1:            
            rec.adjust_for_ambient_noise(source1, duration= 0.5)

            print("Listening ...")
            
            audio = rec.listen(source1, timeout = 20, phrase_time_limit = 30)
            
            try:                 
               
                request = rec.recognize_google(audio, language=slang )
                #request = rec.recognize_wit(audio, key=wit_api_key )
                
                if len(request) < 2:
                    continue 
                    
                if "that's all" in request.lower():
                                               
                    append2log(f"You: {request}\n")
                        
                    speak_text("Bye now")
                        
                    append2log(f"AI: Bye now. \n")                        

                    print('Bye now')

                    continue
                                       
                # process user's request (question)
                
 
                request = f"Translate this to Chinese: {request}!"  
                
                append2log(f"You: {request}\n ")

                print(f"You: {request}\n AI: " )
                response = chat.send_message(request, generation_config=gf, 
                                             safety_settings=safety_settings #, stream=True,
                )

                print(response.text)
                speak_text(response.text.replace("*", ""))        

                append2log(f"AI: {response.text } \n")
 
            except Exception as e:
                #print(response)
                continue 
 
if __name__ == "__main__":
    main()



