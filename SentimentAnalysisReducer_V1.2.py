#!/usr/bin/python

#------------------------------------------#
#------------- GJA March 2015 -------------#
#------- Sentiment Analysis Reducer -------#
#------- for customerReviews.txt data -----#
#------------------------------------------#

import sys

def reducer():
    sentimentTotal = sentiment = count = 0
    oldKey = None

    for line in sys.stdin:
        data = line.strip().split("\t")

        if len(data) != 3:
            continue

        thisProduct, thisAttribute, thisSentiment = data
        thisKey = thisProduct + "-" + thisAttribute
        
        if oldKey and oldKey != thisKey:
            sentiment = sentimentTotal / count
            print oldKey + "\t" + str(sentiment) 
            sentimentTotal = sentiment = count = 0
            
        oldKey = thisKey
        count += 1
        sentimentTotal += float(thisSentiment)

    if oldKey != None:
        sentiment = sentimentTotal / count
        print oldKey + "\t" + str(sentiment) 
            
def main():
	import StringIO
	reducer()
	sys.stdin = sys.__stdin__

main()