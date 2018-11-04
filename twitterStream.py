from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
import sys
import string
import json
import time

#change the path to desired location (it will save to hadoop)
path = "/bherr006/rddTweets/tweets"

#check for langauge from the json
def checkLanguage(tweetJson):
    if tweetJson.has_key('lang'):
        if tweetJson['lang'] == "en":
            return True
    return False


# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from the above spark context with interval size 60 seconds
ssc = StreamingContext(sc, 50)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9008
dataStream = ssc.socketTextStream("localhost",9009)
#lines = dataStream.window(5000)  


#load the jsons and filter only english. Return json into string
jsonRDD = dataStream.map(lambda x: json.loads(x))\
               .filter(lambda x: checkLanguage(x))\
               .map(lambda x: json.dumps(x))               

#save the json strings into text files in a distriputed way
jsonRDD.foreachRDD(lambda rdd: rdd.saveAsTextFile(path + time.strftime("%Y%m%d-%H%M%S")))

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
