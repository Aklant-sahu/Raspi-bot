from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from copyreg import pickle
from enum import EnumMeta
import random
from pprint import pprint
import pickle
import json
import numpy as np
import json
import pandas as pd
import re
import nltk
# nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD
import pyttsx3  

engine = pyttsx3.init()  
voices = engine. getProperty('voices')
engine.setProperty("rate", 140)
engine.setProperty('voice', voices[1].id)  

lemmatizer = WordNetLemmatizer()
df=pd.read_csv("prof1.csv")

app = Flask(__name__)

intents = json.loads(open('intents.json').read())
list_of_prof = ['Kavita', 'Naveeta', 'Rajani', 'Abhay', 'Asawari', 'Jaymala', 'Abhijit', 'Parmeshwar', 'Yogesh', 'Sarika', 'Rakhi', 'Gauri', 'Vijay', 'Amrita', 'Abhishek', 'Dipti', 'Anushree']
# print(intents['intents'])
lemmatizer = WordNetLemmatizer() # It is a technique use in nlp, basically convert a word to lemma i.e. the simmplest meaningful form of that word
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('aibotmodelprof2.h5')


def PROF_CSV(msg,df):
    lab_no =[int(s) for s in msg.split() if s.isdigit()][0]
    sentence=f"The professors sitting in lab no {lab_no} is {df[df['Room No']==lab_no]['Professors'].tolist()}"
    return sentence

def room_func(msg,df):
    sentence_words = re.split(',|\s+|\.',msg)
    sentence_words = [i.lower() for i in sentence_words]
    list_of_prof = ['Kavita', 'Naveeta', 'Rajani', 'Abhay', 'Asawari', 'Jaymala', 'Abhijit', 'Parmeshwar', 'Yogesh', 'Sarika', 'Rakhi', 'Gauri', 'Vijay', 'Amrita', 'Abhishek', 'Dipti', 'Anushree']
    list_of_prof =  [i.lower() for i in list_of_prof]
    room_name = str()
    flag = False
    for i,prof in enumerate(list_of_prof):
        if prof in sentence_words:    
            room_name = f'Prof.{prof.capitalize()} is present in room no. {df.iloc[i][-2]} which is on {df.iloc[i][-1]} .'
            flag = True
        # else:
        #     room_name = "Oops !!This professor name is not present in this department\nBelow is the list of Professors:"            
    return room_name,flag

def cleaning_sentence(sent):
    sentence_words = word_tokenize(sent)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sent):
    sentence_words = cleaning_sentence(sent)
    bag = [0]*len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i]= 1
    return np.array(bag)

def predict_class(sent):
    bow = bag_of_words(sent)
    # print(bow.shape)
    res = model.predict(np.array([bow]))[0]
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    # print(results)
    results.sort(key=lambda x: x[1],reverse = True)
    # print(results)
    return_list = []
    for r in results:
        return_list.append({'intents':classes[r[0]],'probability':str(r[1])})
    # print(return_list)
    return return_list

def get_response(intents_list,intents_json):
    tag = intents_list[0]['intents']
    print(tag)
    list_of_intents = intents_json['intents'] 
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            # result = random.choice(i['response'])
            # result = i['respones']
            break
    return result

def get_div(msg_lst,msg):
    for i in msg_lst:
        if i[0]== 'd':            
            return i.upper()
    

def timetable(div):
    div = div.upper()
   
    print(f"TimeTable of DIV {div}")
    return f"static/timetable/{div}.jpg"
    # img = ImageTk.PhotoImage(Image.open(f'Timetable/{div}.jpg'))
    # Label(win,image = img).pack()
    # print("TimeTable")
    # win.mainloop()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST","GET"])

def chatbot_response():
    msg = request.form["msg"]
    msg_lst=word_tokenize(msg)
    msg_lst = [i.lower() for i in msg_lst]
    
   
   
    if "Timetable".lower() in msg_lst:
        print("in timetable")
        res1=timetable(get_div(msg_lst,msg))
        # engine.say("Timetable is as follows")   
        # engine.runAndWait()
        return res1
    
       
    else:
        
        ints = predict_class(msg)
        res = get_response(ints, intents)
        
        print(res)
        if res=="Room_func":

            room,flag = room_func(msg,df)
            if flag==0:
                message=f"Oops !! This professor name is not present in this department.\n Below is the list of Professors {[i for i in list_of_prof]}"
                # engine.say(message)   
                # engine.runAndWait()
                return message
           
            else:
                # engine.say(room)   
                # engine.runAndWait()

                return room
        elif res == "PROF_CSV":
            ans=PROF_CSV(msg,df)
            # engine.say(ans)   
            # engine.runAndWait()
            return ans
        elif res=="clear":
            return "static/images/white.jpg"

        else:
            # engine.say(res)   
            # engine.runAndWait()

            return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)