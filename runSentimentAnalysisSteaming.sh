#!/bin/bash

# script for SentimentAnalysisMapper and Reducer: 

# change to the hadoop-directory: 
cd /Users/hadoop/hadoop-1.2.1

# create directory in HDFS for input:
if bin/hadoop fs -mkdir SentimentAnalysis/input; then
	echo "create the directory in HDFS for input:"
	bin/hadoop fs -ls SentimentAnalysis/input
else
	echo "directory already exists:"
	bin/hadoop fs -ls SentimentAnalysis/input
fi


# load some sample data:
if bin/hadoop fs -copyFromLocal /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/customer_reviews/reviewsNewsSample.txt SentimentAnalysis/input; then
	echo "load the data to HDFS:"
else
	echo "data already exists"
fi

# check if output directory exists: 
if bin/hadoop fs -rmr SentimentAnalysis/output; then
	echo "delete output directory:"
else
	echo "output directory doesnt exist"
fi

bin/hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar -D mapred.job.name='Sentiment Analysis Sample run' -D mapreduce.map.output.key.field.separator='\t' -D mapreduce.partition.keypartitioner.options=-k1,2 -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -input SentimentAnalysis/input/reviewsNewsSample.txt -output SentimentAnalysis/output/ -mapper /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -reducer /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.0.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.0.py

bin/hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar -input SentimentAnalysis/input/reviewsNewsSample.txt -output SentimentAnalysis/output/ -mapper /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -reducer /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.0.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.0.py

bin/hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar -input SentimentAnalysis/input/reviewsNewsSample.txt -output SentimentAnalysis/output/ -mapper /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -reducer /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.2.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.2.py


# bin/hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar -input SentimentAnalysis/input/reviewsNewsSample.txt -output SentimentAnalysis/output -mapper /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisMapper_V1.2.py -reducer /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.0.py -file /Users/hadoop/Documents/programs/hadoop_streaming/sentiment_analysis/SentimentAnalysisReducer_V1.0.py