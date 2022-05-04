from flask import Flask,render_template,flash,request,url_for,redirect,session
import numpy as np
import pandas as pd
import tensorflow as tf
from numpy import array
import time
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
import os
from flask import jsonify 
import urllib.request 
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import requests,json ,uuid,pathlib
from newspaper import Article
import sentiment
from flask import send_file
import nltk

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
     page="home.html"
     
######################

@app.route("/")
def home():
    #return jsonify(get.main())
    fake=0
    real=0
    return render_template("home.html")
@app.route('/prediction',methods = ['POST','GET'])
def prediction():
      if request.method == 'POST':
        rname=request.form.get('text')
        rlimit=request.form.get('limit')
        return redirect(url_for('getFromSubs',subreddits=rname,limit=rlimit))
#fetch memes from default list of subreddits
@app.route("/<int:limit>")
def getMore(limit):
    return jsonify(get.main(limit=limit, subs = config.subreddits))

#fetch using subreddits and limit
@app.route("/<subreddits>/<int:limit>")
def getFromSubs(subreddits, limit):
    post_json_array=get.main(limit=limit, subs = subreddits)['objects']
    #print(post_json_array)
    reply=[]
    url_array=[]
    title_array=[]
    sen_array=[]
    prob_array=[]
    text_array=[]
    fake=0
    real=0
    #nlp=English()
    for news_url in post_json_array:
        #html_document = requests.get(news_url['url_to_scrape']).content
        try:
            article = Article(news_url['url_to_scrape'])
            article.download()
            time.sleep(2)
            article.parse()
        #article.nlp()
            data=article.text
            reply.append({
                "data":news_url['url_to_scrape']
            })
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
            
            
            if(data):
                text_array.append(data)
            else:
                text_array.append('Not able to load data ')
            if(ans_array['res'][0]['sentiment']=='fake'):
                fake+=1
            else:
                real+=1
        except:
            url_array.append(news_url['url_to_scrape'])
            title_array.append(news_url['title'])
            sen_array.append('XX')
            prob_array.append(-1)
            text_array.append('site access Blocked, Forbidden  url')
    #pdf = pd.read_excel("NewsReport.xlsx")
    #pdf = pd.read_excel("NewsReport.xlsx", sheetname='Sheet1', header=2, skiprows=2, usecols=['url','title','prediction','probability','text'])#new
    pdf={'url':url_array,'title':title_array,'prediction':sen_array,'probability':prob_array,'text':text_array}
    pdf=pd.DataFrame(pdf)
    writer = pd.ExcelWriter('NewsReport.xlsx',engine="xlsxwriter")
    pdf.to_excel(writer, sheet_name="Sheet 1")
  
# write DataFrame to excel
    #pdf.to_excel(writer)
  
# save the excel
    #writer.save() 
    fake_count=[x for x in sen_array if x=='Fake']
    real_count=[x for x in sen_array if x=='Real']
    Low_50=[x for x in prob_array if x<=50]
    Low_80=[x for x in prob_array if (x>50.0 and x<=80.0)]
    Low_100=[x for x in prob_array if x>80.0]
    print(Low_100,Low_80,Low_100)

    data = [
    ['Fake', 'Real','XX'],[len(fake_count),len(real_count),limit-len(real_count)-len(fake_count)],['Below 50','Below 80','Above 80'],[len(Low_50),len(Low_50),len(Low_100)] ]

   
    workbook = writer.book
    
    worksheet = writer.sheets['Sheet 1']
    worksheet.write_column('A20', data[0])
    worksheet.write_column('B20', data[1])
    worksheet.write_column('A30', data[2])
    worksheet.write_column('B30', data[3])

    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
    'categories':['Sheet 1',29,0,31,0],
    'values': ['Sheet 1',29,1,31,1], 
    "name": "Predictions"})
    print(chart)
    worksheet.insert_chart('H10', chart)
    #writer.save()
    chart2=workbook.add_chart({'type': 'pie'})
    chart2.add_series({
    'categories':['Sheet 1',19,0,21,0],
    'values': ['Sheet 1',19,1,21,1], 
    "name": "Fake/Real"})
    worksheet.insert_chart('P10', chart2)
    writer.save()

    print(chart2)




    try:
        #page="graph.html"
        return send_file("NewsReport.xlsx",
                         mimetype='text/xlsx',
                        attachment_filename="output.xlsx",
                         as_attachment=True,
                         cache_timeout=-1) 
        #return render_template("graph.html",file_name:"NewsReport.xlsx")
    #return jsonify(reply)
    except:
        return j('Not able to send file to client ! :( ')
    

#fetch memes using subreddit, minimum upvotes and limit
@app.route("/<subreddits>/<int:upvotes>/<int:limit>")
def getWithUpvotes(subreddits, limit, upvotes):
    return jsonify(get.main(limit=limit, subs = subreddits, upvotes = upvotes))

if __name__ == "__main__":
    init()
    #app.run(debug=config.debug)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
