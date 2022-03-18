
from flask import Flask,render_template,flash,request,url_for,redirect,session
import numpy as np
import pandas as pd
import re
import os
import tensorflow as tf
from numpy import array
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Embedding,LSTM,Conv1D ,MaxPool1D
import pickle
import sys

'''
#from tensorflow.python.ops.math_ops import reduce_prod

#IMAGE_FOLDER = os.path.join('static','img_pool')
app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

def init():
     global model,graph
     model = load_model('New_Model.h5',compile=False)
    # graph = tf.compat.get_default_graph()

@app.route('/',methods = ['GET','POST'])
def home():
       
       return render_template("home.html")
@app.route('/sentiment_analysis_prediction',methods = ['POST','GET'])
'''
def main(text_p):
    #if request.method='POST':
    if True:
        text = text_p
        
        Sentiment = ''
        max_review_length = 1000
        word_to_id = imdb.get_word_index()
        #strip_special_chars = re.compile("[A-Za-z0-9 ]+")
        #text = text.lower().replace("<br />"," ")
        #text = re.sub(strip_special_chars,"",text.lower())
        text=text.split()
        print(text, file=sys.stderr)
        tt=text[1:]
        #t=post.title
        text=''
        text+= " ".join(tt)
        #words = text.split()
        #tokenizer=Tokenizer()
        #with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(open('tokenizer.pickle', 'rb'))

        #x_test = [[word_to_id[word]if (word in word_to_id and word_to_id[word]<=20000)else 0 for word in words]]
        #x_test = tf.keras.preprocessing.sequence.pad_sequences(x_test,maxlen=1000)
        #vector = np.array([x_test.flatten()])
        #with graph.as_default():
        l=[text]
        l=tokenizer.texts_to_sequences(l)
        #print('tokeinsered text',l,file=sys.stderr)
        l=pad_sequences(l,maxlen=1000)
        model = load_model('New_Model.h5',compile=False)
        y=model.predict(l)
        probability=y

        if(y[0][0]>0.5):
            Sentiment='Real'
        else:
            Sentiment='fake '
        #return render_template('home.html',text=text,sentiment = Sentiment,probability = probability)
        json_list = []
        json_list.append({"sentiment":Sentiment})
        json_list.append({"probability":(float(y[0][0])*100)})

        return {"res":json_list}

if __name__ == "__main__":
    #init()
    app.run()