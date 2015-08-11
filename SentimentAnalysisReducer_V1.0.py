#!/usr/bin/python

#------------------------------------------#
#------------- GJA March 2015 -------------#
#------- Sentiment Analysis Reducer -------#
#------- for customerReviews.txt data -----#
#------------------------------------------#

import sys

def reducer():
    sentimentTotal = sentiment = count = 0
    thisKey = oldKey = ""

    for line in sys.stdin:
        data = line.strip().split("\t")

        if len(data) != 3:
            continue

        thisProduct, thisAttribute, thisSentiment = data
        thisKey = thisProduct + thisAttribute

        if oldKey and oldKey != thisKey:
            sentiment = sentimentTotal / count
#            print oldKey + "\t" + str(sentiment)
            print thisProduct + "\t" + thisAttribute + "\t" + str(sentiment)
            count = sentimentTotal = 0
        
        count += 1
        sentimentTotal += int(thisSentiment)
        oldKey = thisProduct + thisAttribute

#    if oldKey != "":
#        print thisProduct + "\t" + thisAttribute + "\t" + str(sentiment)

def main():
	import StringIO
	reducer()
	sys.stdin = sys.__stdin__

main()
	
