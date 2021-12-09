"""
This file contains all the code necessary to scrape the comments of a youtube video or a list of youtube videos
and analyze the average sentiment of the comments. 
"""
import logging
import threading, queue

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('words')
from nltk.corpus import words


import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd   
from selenium import webdriver

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

"""
Creating a dataframe of comments from one youtube video url
parameter: url to a youtube video
returns: dataframe of all comments for video
"""
def create_comments_df(youtube_url):
  data=[]
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--mute-audio")

  with Chrome('chromedriver',chrome_options=chrome_options) as driver:
      wait = WebDriverWait(driver,15)
      driver.get(youtube_url)

      for item in range(40): # can change this range to get more/less comments
          wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)

      comments = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content")))
      for comment in comments:
          data.append(comment.text)

  df = pd.DataFrame(data, columns=['comment'])
  return df


"""
Function to clean the dataframe of comments, removes non-english comments 
parameter: dataframe to clean
returns: cleaned dataframe
"""
def clean_df(df):
  # remove first two rows
  df = df.drop([0, 1])
  
  # remove any comments that are a language other than English
  Word = list(set(words.words()))
  df = df[df['comment'].str.contains('|'.join(Word))]

  # remove duplicate comments
  df.drop_duplicates()
  return df


"""# Sentiment Analysis
**Using the Vader Sentiment Analysis package, here is how we will using the output to classify the output sentiment ([from the docs](https://github.com/cjhutto/vaderSentiment)):**
The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a 'normalized, weighted composite score' is accurate.
It is also useful for researchers who would like to set standardized thresholds for classifying sentences as either positive, neutral, or negative. Typical threshold values (used in the literature cited on this page) are:
positive sentiment: compound score >= 0.05
neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
negative sentiment: compound score <= -0.05
"""

"""
Function to compute a compound sentiment score for a single sentence
parameter: sentence to output sentiment for
returns: sentiment score of sentence
"""
def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
     
    compound = sentiment_dict["compound"]

    return compound
 
"""
Function that takes in a dataframe of comments and returns the average overall sentiment of all the comments
parameter: dataframe of comments
returns: averaged compound sentiment of all comments in the dataframe
"""
def avg_comment_sentiment(comment_df):
    # convert df to list
    comment_list = comment_df.values.tolist()

    comment_sentiments = [sentiment_scores(comment) for comment in comment_list]

    sentiment_score_total = 0
    count = 0
    for sentiment in comment_sentiments:
        count += 1
        sentiment_score_total = sentiment_score_total + sentiment


    overall_sentiment = sentiment_score_total/count

    # print("overall sentiment is: ", overall_sentiment) # USE THIS FOR DEBUGGING PURPOSES

    return  overall_sentiment

"""
Helper function for each thread to scrape comments, clean them, and find overall sentiment of comments
"""
def sentiment_analyze_one_url(url, queue):
    comments_df = create_comments_df(url)
    comments_df = clean_df(comments_df)
    queue.put(avg_comment_sentiment(comments_df))

"""
Overall function to analyze the sentiment of multiple videos given a list of urls
"""
def sentiment_analyze_urls(urls):
  # Using threads to start comment scraping and sentiment analysis on all urls at the same time
  threads = list()
  q = queue.Queue()
  final_sentiments = []
  for url in urls:
    x = threading.Thread(target=sentiment_analyze_one_url, args=(url, q))
    threads.append(x)
    x.start()
    

  # Get response from the threads and append them to the final sentiment list
  for index, t in enumerate(threads):
    response = q.get()
    final_sentiments.append(response)
    t.join()

  return final_sentiments



"""
Server Code
This code is largely inspired by the following tutorial: https://pythonbasics.org/webserver/ 
"""
hostName = "localhost"
serverPort = 8080
class MyServer(BaseHTTPRequestHandler):
    # This function accepts post requests from http://localhost:8080
    # Receives a list of video urls from the POST request
    # Responds back with a list of positivity/negativity percentages for each video
    def do_POST(self):
        # read and parse data(list of video urls) sent by client
        length = self.headers["Content-Length"]
        body = (self.rfile.read(int(length)).decode('utf-8'))[1:-1]
        body = body.replace('\"', '')
        urls = body.split(",")

        # Pass urls to sentiment analyzer above
        sentiments = sentiment_analyze_urls(urls)

        # Send 200 OK response
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Send list of positivity/negativity percentage data
        self.wfile.write(bytes(json.dumps(sentiments), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")