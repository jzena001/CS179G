from __future__ import print_function
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row

# For creating a data frame in spark
from pyspark.ml import Pipeline

# For Naive Bayes classifier
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel

# For extracting features 
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StringIndexer
from pyspark.ml.feature import IndexToString

from pyspark.sql.functions import monotonically_increasing_id

import shutil
import sys
import string
import json
import re

path = "/bherr006/rddTweets/tweets20181107-045910/*"

sc = SparkSession.builder.appName("ProcessData").getOrCreate()

# Set the log level        
sc.sparkContext.setLogLevel("Error") # spark context

def checkEmpty(x):
    if (x == ""):
        return False
    return True


def getText(x):
   tempList = []
   jsonTweet = json.loads(x)

   tweetID = jsonTweet['id']
  
   tweetUser = jsonTweet['user']['screen_name'].encode('utf-8')
   tweetUser = re.sub(r'[^\x00-\x7F]+','', tweetUser)
   tweetUser = re.sub(r'[\n\t\r,]', '', tweetUser)
   
   tweetText = jsonTweet['text'].encode('utf-8')
   tweetText = re.sub(r'[^\x00-\x7F]+','', tweetText)
   
   tweetTimeStamp = jsonTweet['created_at'].encode('utf-8')

  # if (not(jsonTweet['coordinates'] == None)):
  #    tweetGeo = True
  #    tweetLongitude = jsonTweet['coordinates'][0]
  #    tweetLatitude = jsonTweet['coordinates'][1]
  # else:
  #    tweetGeo = False
  #    tweetLongitude = 0
  #    tweetLatitude = 0
   
   tempList.append(tweetID)
   tempList.append(tweetUser)
   tempList.append(tweetTimeStamp)
   #tempList.append(tweetGeo)
   #tempList.append(tweetLongitude)
   #tempList.append(tweetLatitude)
   tempList.append(tweetText)
   return tempList

lines = sc.read.text(path).rdd.map(lambda x: x[0])

jsonText = lines.map(lambda x: getText(x))
rowRdd = jsonText.map(lambda w: Row(id=w[0], user=w[1], timeStamp=w[2], text=w[3]))

df = sc.createDataFrame(rowRdd)


#df.show()


tokenizer = Tokenizer(inputCol = "text", outputCol = "words")
# Extract the features
hashing_tf = HashingTF(numFeatures = 2**16, inputCol = "words", outputCol = "tf")
idf = IDF(inputCol = "tf", outputCol = "features", minDocFreq = 5)
#labels = StringIndexer(inputCol = "_c0", outputCol = "label")
lines = Pipeline(stages = [tokenizer, hashing_tf, idf])

# Get the data to test
line_fit = lines.fit(df)
test_model = line_fit.transform(df)

# Load the trained model
nb = NaiveBayesModel.load("/mzero001/test_ml/naive_bayes")

# Reindex back to original labels
converter = IndexToString(inputCol="prediction", outputCol="sentiment")

# Classify the tweets by sentiment
result = nb.transform(test_model)
#result.show()

df = df.withColumn("number", monotonically_increasing_id())
sentimentDf = result.select("prediction").withColumn("number", monotonically_increasing_id())
df = df.join(sentimentDf, "number", "right_outer").drop("number")
df.show(10)

df.write.csv("/bherr006/csvTweets/test")

sc.stop()
