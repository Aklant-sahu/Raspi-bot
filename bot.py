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

intents = json.loads(open('intents.json').read())
# print(intents['intents'])
lemmatizer = WordNetLemmatizer() # It is a technique use in nlp, basically convert a word to lemma i.e. the simmplest meaningful form of that word
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('aibotmodelprof2.h5')

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
print("Go go bot")

def chatbot_response(msg):
    ints = predict_class(msg)
    res = get_response(ints, intents)
    return res
def displaycsv():
    df = pd.read_csv("prof1.csv")
    return df
df = pd.read_csv("prof1.csv")
if __name__ == "__main__":
    # print(predict_class('Hello'))
    while True:
        msg = input('You: ')
        sentence_words = word_tokenize(msg)
        sentence_words = [i.lower() for i in sentence_words]


        print(sentence_words)
        list_of_prof = ['Kavita', 'Naveeta', 'Rajani', 'Abhay', 'Asawari', 'Jaymala', 'Abhijit', 'Parmeshwar', 'Yogesh', 'Sarika', 'Rakhi', 'Gauri', 'Vijay', 'Amrita', 'Abhishek', 'Dipti', 'Anushree']
        list_of_prof =  [i.lower() for i in list_of_prof]
        # for i,prof in enumerate(list_of_prof):
        #     if prof in sentence_words:
        #         print(f'{prof.capitalize()} is in {df.iloc[i][-1]}')
        if 'goodbye' in [x.lower() for x in sentence_words ] :
            print('Bot: Bye')
        else:
            ints = predict_class(msg) 
            # print(ints)
            res = get_response(ints,intents)
            if res == "PROF_CSV":
                print(displaycsv())
            else:
                print('Bot: ',res)


# a = ['Hello','Hi'
# ,'Hello'
# ,'Greetings!','Hello'
# ,'Hello'
# ,'Good'
# ,'Fine'
# ,'Okay'
# ,'Great'
# ,'Could be better.'
# ,'Not so great.'
# ,'Good.'
# ,'Very well, thanks.'
# ,'How are you doing?','Fine and you?'
# ,'Nice to meet you.','Thank you.'
# ,'Im doing well.'
# ,'How do you do?',"I'm doing well. How are you?"
# , 'nice to meet you.','Thank you. You too.'
# ,'It is a pleasure to meet you.','Thank you. You too.'
# ,'Top of the morning to you!','Thank you kindly.'
# ,'Top of the morning to you!,And the rest of the day to you.'
# ,'Whats up?', 'What about you?']


# b = list(set(a))
# b = json.dumps(b)
# print(b)
