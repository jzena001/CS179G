from __future__ import print_function
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row

# For creating a data frame in spark
from pyspark.ml import Pipeline

# For Naive Bayes classifier
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel, LogisticRegression, LogisticRegressionModel

# For extracting features 
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StringIndexer
from pyspark.ml.feature import IndexToString


import shutil
import sys
import string
import json
import re

tweetsDate = "tweets20181104"
path = "/bherr006/rddTweets/" + tweetsDate + "*/*"


sc = SparkSession.builder.appName("ProcessData").getOrCreate()

# Set the log level        
sc.sparkContext.setLogLevel("Error") # spark context

def checkEmpty(x):
    if (x == ""):
        return False
    return True

def checkHashEmpty(x):
    if (x == "#" or x == ""):
        return False
    return True

def getText(x):
   coorList = []
   tempList = []
   hashtagList = []
   mentionList = []
   jsonTweet = json.loads(x)

   tweetText = jsonTweet['text'].encode('utf-8')
   tweetText = re.sub(r'[^\x00-\x7F]+','', tweetText)
   tweetText = re.sub(r'[\n\t\r,"|\\]', "", tweetText)
   if (not(checkEmpty(tweetText))):
      return tempList.append("")
  
   tweetText = tweetText.lower()
    
   tweetID = jsonTweet['id']
  
   tweetUser = jsonTweet['user']['screen_name'].encode('utf-8')
   tweetUser = re.sub(r'[^\x20-\x7E]+','', tweetUser)
   tweetUser = re.sub(r'[\n\t\r]', '', tweetUser)
   tweetUser = tweetUser.lower()

   hashtagTempList = tweetText.split(" ")   
   for i in range(len(hashtagTempList)):
      if (hashtagTempList[i].startswith('#') and not(hashtagTempList[i] == "#")):
         hashtagList.append(re.sub(r'[^a-zA-z0-9_]', '', hashtagTempList[i]))
  
   if (len(hashtagList) == 0):
      tweetHashtag = ""
   else:
      tweetHashtag = hashtagList[0]
      tweetHashtag = tweetHashtag.lower()

   mentionTempList = tweetText.split(" ")
   for i in range(len(mentionTempList)):
      if (mentionTempList[i].startswith('@') and not(mentionTempList[i] == "@")):
         mentionList.append(re.sub(r'[^a-zA-z0-9_]', '', mentionTempList[i]))

   if (len(mentionList) == 0):
      tweetMention = ""
   else:
      tweetMention = mentionList[0]
      tweetMention = tweetMention.lower()


   
   tweetTimeStamp = jsonTweet['created_at'].encode('utf-8')

   if (not(jsonTweet['coordinates'] == None)):
      tweetGeo = True
      tweetLongitude = jsonTweet['coordinates']['coordinates'][0]
      tweetLatitude = jsonTweet['coordinates']['coordinates'][1]
   else:
      tweetGeo = False
      tweetLongitude = 0.0
      tweetLatitude = 0.0
   
   tweetUrl = "https://twitter.com/" + tweetUser + "/status/" + str(tweetID)
   

   tempList.append(tweetID)
   tempList.append(tweetUser)
   tempList.append(tweetTimeStamp)
   tempList.append(tweetGeo)
   tempList.append(tweetLongitude)
   tempList.append(tweetLatitude)
   tempList.append(tweetText)
   tempList.append(tweetHashtag)
   tempList.append(tweetMention)
   tempList.append(tweetUrl)
   return tempList


lines = sc.read.text(path).rdd.map(lambda x: x[0])\
          .map(lambda x: getText(x))\
          .filter(lambda x: not(x == None))\
          .filter(lambda x: checkEmpty(x[0]))\
          .map(lambda x: Row(id=x[0], user=x[1], timeStamp=x[2], geo=x[3], longitude=x[4], latitude=x[5], text=x[6], hashtag=x[7], mention=x[8], url=x[9]))


df = sc.createDataFrame(lines)


tokenizer = Tokenizer(inputCol = "text", outputCol = "words")
# Extract the features
hashing_tf = HashingTF(numFeatures = 2**16, inputCol = "words", outputCol = "tf")
idf = IDF(inputCol = "tf", outputCol = "features", minDocFreq = 5)
lines = Pipeline(stages = [tokenizer, hashing_tf, idf])

# Get the data to test
line_fit = lines.fit(df)
test_model = line_fit.transform(df)

# Load the trained model
nb = LogisticRegressionModel.load("/bherr006/datasetTraining/logisticRegression")


# Reindex back to original labels
converter = IndexToString(inputCol="prediction", outputCol="sentiment")

# Classify the tweets by sentiment
result = nb.transform(test_model)

result= result.drop("words", "tf", "features", "rawPrediction", "probability")
result.show(10)


result.write.csv("/bherr006/csvTweets/" + tweetsDate)


sc.stop()
