#!/usr/bin/env python

# python dummy file for tests:

import sys
import re
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer

posFeatures = []
posTag = []
words = []
sentiment = sentinel = position = 0

# needed for stemming and for lemmatizing: 
lancaster_stemmer = LancasterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

with open("positive_words.txt", 'r') as posDict:
#   remove line breaks
    posWords = [word.strip() for word in posDict]
#   create a list of positive words
    posFeatures.append(posWords)
#    posTag = [",".join(item) for item in posFeatures ]
#    print posTag
#    print posWords

#for word in posWords:
#    for word, pos in nltk.pos_tag(nltk.word_tokenize(word)):
#        # pos in scope: JJ, JJR, JJS, RB, RBR, RBS
#        if word in posWords and len(word) > 2 and pos in ['RB', 'JJ']:
#            # tag ordinal and comperative adjectives for positive words
#            print word + "\t" + str(sentiment) + "\t" + pos
#    if word in negWords and len(word) > 2 and pos in ['JJ', 'JJR', 'JJS']:
#        print productId + "\t" + noun + " --> " + word + "\t" + str(sentiment) + "\t" + pos

# defined grammer for the structure of the product reviews!
#grammar = "NP: {<NN>*<VBZ><RB>*<JJ>?}"

#grammar = """
#	NP:   {<PRP>?<JJ.*>*<NN.*>*<JJ.*>+}
#	CP:   {<JJR|JJS>}
#   ADVERB: {<RB.*>}
#	VERB: {<VB.*>}
#	THAN: {<IN>}
#	COMP: {<DT>?<NP><RB>?<VERB><DT>?<CP><THAN><DT>?<NP>}
#	"""

grammar = r"""
        NP: {<.*>*}             # start by chunking everything
        }<[\.VI].*>+{           # chink any verbs, prepositions or periods
        <.*>}{<DT>              # separate on determiners
        PP: {<IN><NP>}          # PP = preposition + noun phrase
        VP: {<VB.*><NP|PP>*}    # VP = verb words + NPs and PPs
        """

cp = nltk.RegexpParser(grammar)

for line in sys.stdin:
    line.rstrip('\n')
    data = re.split('\t', line)
    
    if len(data) == 8:
        memberId, productId, date, numberHelpfulFeedbacks, numbeFeedbacks, rating, title, textBody = data
        
        # split text into sentences
        print "1. Phase segmentation of the text into sentences:"
        sentences = nltk.sent_tokenize(textBody)

        # loop through for each sentence: 
        for sentence in sentences:
            print sentence
            tokens = nltk.word_tokenize(sentence)
            print "2. Phase tokenize the sentences:"
            print tokens
            
            print "3. Phase part of speech tagging:"
            tagged = nltk.pos_tag(tokens)
            print tagged
                       
            print "4. Phase chunking:"
            tree = cp.parse(tagged)
            print tree
            tree.draw()
 
            # entities not needed in the example when using chunks
#            entities = nltk.chunk.ne_chunk(tagged)
#            print entities

            for subtree in tree.subtrees(filter=lambda t: t.node == 'NP'):
                for attributes in subtree.leaves():
                    (expression, tag) = attributes
                    if tag == 'NN':
                        # lemmatizing
                        print wordnet_lemmatizer.lemmatize(expression) + " is a noun"
                    elif tag == 'RB' or tag == 'JJ':
                        # stemming
                        print lancaster_stemmer.stem(expression) + " is an adverb"

                
                    
