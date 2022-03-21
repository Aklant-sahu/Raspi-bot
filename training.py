from copyreg import pickle
import random
from pprint import pprint
import pickle
import json
import numpy as np
from sklearn.model_selection import train_test_split
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
X_train, X_test, y_train, y_test = train_test_split(train_x, train_y, test_size=0.15, random_state=101)

# print(train_y)
# # Builing Model 
act = 'relu'
stop = callbacks.EarlyStopping(monitor='val_loss',patience=5)
model = Sequential()
model.add(Dense(100,input_shape = (len(train_x[0]),),activation=act)) # input_shape parameter adds a layer before current layer as a input layer
model.add(Dropout(0.15)) 
model.add(Dense(100,activation=act))
model.add(Dropout(0.15)) 
model.add(Dense(50,activation=act))
model.add(Dropout(0.15)) 
model.add(Dense(25,activation=act))
model.add(Dense(len(train_y[0]),activation='softmax')) # Output layer
# model.add(Dense(len(train_y[0]),activation='sigmoid'))
sgd = SGD(learning_rate=0.01,momentum=0.9,nesterov=True) # sgd optimiser is giving an error during predict operation ([nan nan])
adam = Adam(learning_rate=0.01)
model.compile(loss = 'categorical_crossentropy',optimizer=adam,metrics=['accuracy'])
# model.compile(loss = 'binary_crossentropy',optimizer=adam,metrics=['accuracy'])

model.fit(np.array(X_train), np.array(y_train), epochs= 200,batch_size=8,verbose=1,callbacks=[stop],validation_data=[np.array(X_test),np.array(y_test)])
# print(model.evaluate(np.array(train_x), np.array(train_y)))
# model.save('datazen1.h5')
# tf.saved_model.save(model, "aibotmodelprof2")
model.save('aibotmodelprof2.h5')
print('~~~~~ DONE ! ~~~~~~')