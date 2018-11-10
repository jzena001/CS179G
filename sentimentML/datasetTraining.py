from __future__ import print_function
from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

import sys
import string

spark = SparkSession.builder\
        .appName("datasetTraining")\
        .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

dataset = spark.read.csv('/bherr006/datasetTraining/training.1600000.processed.noemoticon.csv', header=False, inferSchema=True)

(trainSet, valSet, testSet) = dataset.randomSplit([0.98, 0.01, 0.01], seed = 2000)

tokenizer = Tokenizer(inputCol="_c5", outputCol="words")
hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol="tf")
idf = IDF(inputCol="tf", outputCol="features", minDocFreq=5)
labelStringIndex = StringIndexer(inputCol="_c0", outputCol = "label")
pipeline = Pipeline(stages=[tokenizer,hashtf,idf,labelStringIndex])

pipelineFit = pipeline.fit(trainSet)
trainDf = pipelineFit.transform(trainSet)
valDf = pipelineFit.transform(valSet)

lr = LogisticRegression(maxIter=100)
lrModel = lr.fit(trainDf)
predictions = lrModel.transform(valDf)
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
print(evaluator.evaluate(predictions))

