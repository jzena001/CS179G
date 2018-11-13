# For printing
from __future__ import print_function

# For creating a DataFrame in spark
from pyspark.ml import Pipeline

# For Naive Bayes classifier to generate model
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# For generating tf-idf for use with Naive Bayes classifier
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StringIndexer

# For getting pyspark context
from pyspark import SparkContext
from pyspark.sql import SparkSession

import shutil
import sys
import string


sc = SparkSession.builder.appName("ModelTraining").getOrCreate()

# Set the log level        
sc.sparkContext.setLogLevel("Error") # spark context

# Get the data to train the model
training_tweets = sc.read.csv("/mzero001/test_ml/training.1600000.processed.noemoticon.csv", header = False, inferSchema = True)

#test_tweets =sc.read.csv("/mzero001/test_ml/testdata.manual.2009.06.14.csv", header = False, inferSchema = True)

# Split the data into sets for training, validation, and test
(training_set, validation_set, test_set) = training_tweets.randomSplit([0.98, 0.01, 0.01], seed = 2000)

tokenizer = Tokenizer(inputCol="_c5", outputCol="words")

# Get the tf-idf
hashing_tf = HashingTF(numFeatures=2**16, inputCol = "words", outputCol = "tf")
idf = IDF(inputCol = "tf", outputCol = "features", minDocFreq=5)
labels = StringIndexer(inputCol = "_c0", outputCol = "label")
lines = Pipeline(stages=[tokenizer, hashing_tf, idf, labels])

# For creating the training, validation, and test models
line_fit = lines.fit(training_set)
train_model = line_fit.transform(training_set)
validation_model = line_fit.transform(validation_set)
test_model = line_fit.transform(test_set)
    
# Train and check the model
nb = NaiveBayes(smoothing=1.0, modelType = "multinomial")
model = nb.fit(train_model)
predictions = model.transform(test_model) 
predictions.show()

evaluator = MulticlassClassificationEvaluator(labelCol="label", 
                                             predictionCol = "prediction",
                                             metricName = "accuracy")

accuracy = evaluator.evaluate(predictions)

print('model accuracy []', format(accuracy))

# Save the model. We can load later with the NaiveBayesModel.load function
output_directory = 'mzero001/test_ml/naive_bayes'
shutil.rmtree(output_directory, ignore_errors=True)
model.save(output_directory)

# Exit stage right
sc.stop()
    
