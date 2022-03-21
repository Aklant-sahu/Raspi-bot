# Convert the model.
import os
from copyreg import pickle
import random
from pprint import pprint
import pickle
import json
import numpy as np

import nltk
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD,Adam
from tensorflow.keras import callbacks

intents = json.loads(open('intents.json').read())
# print(intents['intents'])

lemmatizer = WordNetLemmatizer() # It is a technique use in nlp, basically convert a word to lemma i.e. the simmplest meaningful form of that word

words = [] # list of list of different words
classes = []
documents = [] # list of words and there respective tag in a tuple
ignore_letters = ['?','.','!',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
    # for pattern in intent['pattern']:
        word_list = word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

print(classes)
# Convert to  pickle file
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))


###################################################################################################################################
# This entire process is there so that the neural network can have a array as an input because it will not take words as input
training = []
output_empty = [0]*len(classes) 
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    # print(bag)

    output_row = list(output_empty)# This method is used to copy the list
    # print('empty output list: ',output_empty)
    # print('copy of empty list',output_row)
    # print('index: ',classes.index(document[1]))
    output_row[classes.index(document[1])] = 1
 
    training.append([bag,output_row])
###################################################################################################################################
# print(training)
random.shuffle(training)
training= np.array(training)

train_x = list(training[ : , 0])
train_y = list(training[ : , 1])
model = tf.keras.models.load_model('aibotmodelprof2')
##  converting model
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()
# # Save the model.
# with open('model.tflite', 'wb') as f:
#   f.write(tflite_model)


def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size

def convert_bytes(size, unit=None):
    if unit == "KB":
        return print('File size: ' + str(round(size / 1024, 3)) + ' Kilobytes')
    elif unit == "MB":
        return print('File size: ' + str(round(size / (1024 * 1024), 3)) + ' Megabytes')
    else:
        return print('File size: ' + str(size) + ' bytes')


convert_bytes(get_file_size('aibotmodelprof.h5'), "KB")
# test_loss,test_acc=model.evaluate(np.array(train_x), np.array(train_y))
# print('/nTest accuracy:',test_acc)
convert_bytes(get_file_size('model.tflite'), "KB")

tflite_interpreter = tf.lite.Interpreter(model_path='model.tflite')

input_details = tflite_interpreter.get_input_details()
output_details = tflite_interpreter.get_output_details()

print("== Input details ==")
print("name:", input_details[0]['name'])
print("shape:", input_details[0]['shape'])
print("type:", input_details[0]['dtype'])

print("\n== Output details ==")
print("name:", output_details[0]['name'])
print("shape:", output_details[0]['shape'])
print("type:", output_details[0]['dtype'])
print(input_details)



print(np.array(train_x).shape)

tflite_interpreter.resize_tensor_input(input_details[0]['index'], (119,192))
tflite_interpreter.resize_tensor_input(output_details[0]['index'], (1,11))
tflite_interpreter.allocate_tensors()

input_details = tflite_interpreter.get_input_details()
output_details = tflite_interpreter.get_output_details()
tflite_interpreter.set_tensor(input_details[0]['index'],np.array(train_x,dtype=np.float32))

tflite_interpreter.invoke()

tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])
print("Prediction results shape:", tflite_model_predictions.shape)
## calculating tflite accuarcy 
# tflite_interpreter.allocate_tensors()
# tflite_interpreter.set_tensor(input_details[0]['index'],np.array(train_x,dtype=np.float32))
# tflite_interpreter.invoke()


# tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])
# print("Prediction results shape:", tflite_model_predictions.shape)
