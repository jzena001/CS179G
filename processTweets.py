from __future__ import print_function
from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
import sys
import string
import json

path = "/bherr006/rddTweets/tweets20181104-131500/*"

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

lines = sc.textFile(path).map(lambda x: json.loads(x))\
          .map(lambda x: x['text'])\
          .flatMap(lambda line: line.split(" "))\
          .filter(lambda x: x.startswith( '#' ))\
          .map(lambda x: (x, 1))\
          .reduceByKey(lambda x, y: x + y)\


output = lines.collect()
print(output)

sc.stop()
