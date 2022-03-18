from flask import Flask,render_template,flash,request,url_for,redirect,session
import numpy as np
import pandas as pd
import tensorflow as tf
from numpy import array

from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Embedding,LSTM,Conv1D ,MaxPool1D
import pickle
import sys
import get
import config
from flask import jsonify 
import urllib.request 
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import requests,json ,uuid,pathlib
from newspaper import Article
import sentiment
################################
app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

def init():
     global model,graph,url_array,title_array,sen_array,prob_array
     model = load_model('New_Model.h5',compile=False)
     url_array=[]
     title_array=[]
     sen_array=[]
     prob_array=[]
######################

@app.route("/")
def home():
    return jsonify(get.main())

#fetch memes from default list of subreddits
@app.route("/<int:limit>")
def getMore(limit):
    return jsonify(get.main(limit=limit, subs = config.subreddits))

#fetch using subreddits and limit
@app.route("/<subreddits>/<int:limit>")
def getFromSubs(subreddits, limit):
    post_json_array=get.main(limit=limit, subs = subreddits)['objects']
    print(post_json_array)
    reply=[]
    url_array=[]
    title_array=[]
    sen_array=[]
    prob_array=[]
    text_array=[]
    for news_url in post_json_array:
        html_document = requests.get(news_url['url_to_scrape']).content
        try:
            article = Article(news_url['url_to_scrape'])
            article.download()
            article.parse()
        #article.nlp()
            data=article.text
            reply.append({
                "data":news_url['url_to_scrape']
            })
            print(data)
        #soup = BeautifulSoup(html_document, 'html.parser')
        #x=soup.find('article')
        #if x==None:
            #continue
        #print(news_url['title'],news_url['url_to_scrape'],x)
        #print(source)
            ans_array=sentiment.main(data)
            reply.append(ans_array)
            url_array.append(news_url['url_to_scrape'])
            title_array.append(news_url['title'])
            sen_array.append(ans_array['res'][0]['sentiment'])
            prob_array.append(ans_array['res'][1]['probability'])
            text_array.append(data)
        except:
            url_array.append(news_url['url_to_scrape'])
            title_array.append(news_url['title'])
            sen_array.append('XX')
            prob_array.append(-1)
            text_array.append('site access Blocked, Forbidden  url')

    pdf={'url':url_array,'title':title_array,'sentiment':sen_array,'probability':prob_array,'text':text_array}
    pdf=pd.DataFrame(pdf)
    datatoexcel = pd.ExcelWriter('E:/flaskProjects-1/fake_news_1/NewsReport.xlsx')
  
# write DataFrame to excel
    pdf.to_excel(datatoexcel)
  
# save the excel
    datatoexcel.save()  
    return jsonify(reply)
    

#fetch memes using subreddit, minimum upvotes and limit
@app.route("/<subreddits>/<int:upvotes>/<int:limit>")
def getWithUpvotes(subreddits, limit, upvotes):
    return jsonify(get.main(limit=limit, subs = subreddits, upvotes = upvotes))

if __name__ == "__main__":
    init()
    app.run(debug=config.debug)
