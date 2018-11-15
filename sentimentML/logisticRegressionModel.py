# For printing
from __future__ import print_function

# For creating a DataFrame in spark
from pyspark.ml import Pipeline

# For Naive Bayes classifier to generate model
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel, LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

# For generating tf-idf for use with Naive Bayes classifier
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StringIndexer, IndexToString

# For getting pyspark context
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.sql.functions import *
import shutil
import sys
import string


sc = SparkSession.builder.appName("ModelTraining").getOrCreate()

# Set the log level        
sc.sparkContext.setLogLevel("Error") # spark context

dataset = sc.read.csv('/bherr006/datasetTraining/training.1600000.processed.noemoticon.csv', header=False, inferSchema=True)

#dataset.drop("_c1","_c2","_c3","_c4")
dataset = dataset.select(col("_c0").alias("original"), col("_c5").alias("text"))
dataset.show(30)

(trainSet, valSet, testSet) = dataset.randomSplit([0.98, 0.01, 0.01], seed = 2000)

# Get the tf-idf
tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol="tf")
idf = IDF(inputCol="tf", outputCol="features", minDocFreq=5)
labels = StringIndexer(inputCol="original", outputCol = "label")
lines = Pipeline(stages=[tokenizer,hashtf,idf,labels])

# For creating the training, validation, and test models
linesFit = lines.fit(trainSet)
trainModel = linesFit.transform(trainSet)
validationModel = linesFit.transform(valSet)

# Train and check the model
lr = LogisticRegression(maxIter=100)
model = lr.fit(trainModel)
predictions = model.transform(validationModel)
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
predictions.show(30)

#show the label of the indexed labels
converter = IndexToString(inputCol="label", outputCol="label meaning")
converted = converter.transform(predictions.select("label").distinct())
converted.select("label", "label meaning").distinct().show()

#calculate the precision and recall
truePositive = predictions[(predictions.label == 0) & (predictions.prediction == 0)].count()
trueNegative = predictions[(predictions.label == 1) & (predictions.prediction == 1)].count()
falsePositive = predictions[(predictions.label == 1) & (predictions.prediction == 0)].count()
falseNegative = predictions[(predictions.label == 0) & (predictions.prediction == 1)].count()
recall = float(truePositive) / (truePositive + falseNegative)
precision = float(truePositive) / (truePositive + falsePositive)

print("True Positive", truePositive)
print("True Negative", trueNegative)
print("False Positive", falsePositive)
print("False Negative", falseNegative)
print("recall", recall)
print("precision", precision)
print("accuracy", evaluator.evaluate(predictions))


# Save the model. We can load later with the NaiveBayesModel.load function
output_directory = "/bherr006/datasetTraining/logisticRegression"
shutil.rmtree(output_directory, ignore_errors=True)
model.save(output_directory)

# Exit stage right
sc.stop()
