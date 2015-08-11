#!/usr/bin/env python

#------------------------------------------#
#------------ GJA February 2015 -----------#
#-------- Mapper sentiment analysis -------#
#------------- customer reviews -----------#
#------- for reviewsNew.txt dataset -------#
#------------------------------------------#

import sys
import re
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer

# necessary to import the NLTK module to the HDFS cluster!
import zipimport

importer = zipimport.zipimporter('nltkandyaml.mod')
yaml = importer.load_module('yaml')
nltk = importer.load_module('nltk')

# get the existing POS tags from nltk help: 
# nltk.help.upenn_tagset()

# initialize variables
sentiment = 0.0

# needed for stemming and for lemmatizing: 
lancaster_stemmer = LancasterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

with open("positive_words.txt", 'r') as posDict:
#   create a list of positive words and remove line breaks
    posWords = [word.strip() for word in posDict]

with open("negative_words.txt", 'r') as negDict:
#   create a list of negative words and remove line breaks
    negWords = [word.strip() for word in negDict]

# define a context free grammer for detection of chunks within a sentence    
#grammar = r"""
#        NP: {<.*>*}             # start by chunking everything
#        }<[\.VI].*>+{           # chink any verbs, prepositions or periods
#        CP: {<JJ|JJR|JJS>}      # forms of adjectives (GJA)
#        AV: {<RB.*>}            # forms of adverbs (GJA)
#        PP: {<IN><NP>}          # PP = preposition + noun phrase
#        VP: {<AB.*><NP|CP>*}    # VP = verb words + NPs and PPs
#        """

grammar = r"""
        NP: {<.*>*}             # start by chunking everything
        }<[\.IDC],*.*>+{          # chink any verbs, prepositions, determiners, conjunctions or periods
        """
        
cp = nltk.RegexpParser(grammar)

# read from stdin: 
for line in sys.stdin:
    line.rstrip('\n')
    data = re.split('\t', line)
    
    if len(data) == 8:
        memberId, productId, date, numberHelpfulFeedbacks, numbeFeedbacks, rating, title, textBody = data

        # 1. phase: split text into sentences
        sentences = nltk.sent_tokenize(textBody)
        
        for sentence in sentences:
            # 2. phase tokenize the sentences:
            tokens = nltk.word_tokenize(sentence)
            
            # 3. phase part of speech tagging:
            tagged = nltk.pos_tag(tokens)
                       
            # 4. Phase chunking:
            tree = cp.parse(tagged)
            # uncomment the next lines to display the tree
#            print tree
#            tree.draw()
 
            # initialize variables:
            noun = posExpression = negExpression = posSuperlative = negSuperlative = ""
            
            for subtree in tree.subtrees(filter=lambda t: t.node == 'NP'):
                for attributes in subtree.leaves():
                    (expression, tag) = attributes
#                    print expression + "\t" + tag
                    if tag in ['NN', 'NNS', 'NNP']:
                        # lemmatizing not used for prformance reasons
                        # noun = wordnet_lemmatizer.lemmatize(expression)
                        noun += " " + expression
                    elif tag in ['JJ', 'JJR', 'RB', 'RBR',] and len(expression) > 2 and expression in posWords:
                        # tag ordinal and comperative adjectives for positive words
                        sentiment = 1
                        # lemmatizing not used for prformance reasons
                        # posExpression = wordnet_lemmatizer.lemmatize(expression)  
                        posExpression = expression                      
                    elif tag in ['JJ', 'JJR', 'RB', 'RBR'] and len(word) > 2 and expression in negWords:
                        # tag ordinal and comperative adjectives for negative words
                        sentiment = -1
                        # lemmatizing not used for prformance reasons
                        # negExpression = wordnet_lemmatizer.lemmatize(expression)
                        negExpression = expression
                    elif tag in ['JJS', 'RBS'] and expression in posWords and len(word) > 2:
                        # tag ordinal and comperative adjectives for positive words
                        sentiment = 2
                        # posSuperlative = wordnet_lemmatizer.lemmatize(expression)
                        posSuperlative = expression
                    elif tag in ['JJS', 'RBS'] and expression in negWords and len(word) > 2:
                        sentiment = -2
                        # negSuperlative = wordnet_lemmatizer.lemmatize(expression)
                        negSuperlative = expression
                    
                if (noun != "" and (posExpression != "" or negExpression != "" or posSuperlative != "" or negSuperlative != "")):
                    # using \t as separator for composite key in the reducer!!!
                    # print productId + "\t" + noun + "\t" + posExpression + " " + negExpression + "\t"+ str(sentiment)
                    print productId + "\t" + noun + "\t" + str(sentiment)
                # reset the content of the variables to ""
                noun = expression = posExpression = negExpression = posSuperlative = negSuperlative = ""
                            
    else: 
        continue
