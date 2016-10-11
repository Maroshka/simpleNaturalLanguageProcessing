from urllib import *
from bs4 import BeautifulSoup
import string
import re
import operator
from nltk import PunktSentenceTokenizer

def isCommon(ngram):
	commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",\
	"i", "that", "for", "you", "he", "with", "on", "do", "say", "this",\
	"they", "is", "an", "at", "but","we", "his", "from", "that", "not",\
	"by", "she", "or", "as", "what", "go", "their","can", "who", "get",\
	"if", "would", "her", "all", "my", "make", "about", "know", "will",\
	"as", "up", "one", "time", "has", "been", "there", "year", "so",\
	"think", "when", "which", "them", "some", "me", "people", "take",\
	"out", "into", "just", "see", "him", "your", "come", "could", "now",\
	"than", "like", "other", "how", "then", "its", "our", "two", "more",\
	"these", "want", "way", "look", "first", "also", "new", "because",\
	"day", "more", "use", "no", "man", "find", "here", "thing", "give",\
	"many", "well"]
	for word in ngram.split():
		if word in commonWords:
			return True
	return False

def clean(inp):
	inp = inp.lower()
	inp = re.sub(r'((?![\w\s]).)*', '', inp)
	inp = re.sub(r'[0-9\n+]', ' ',inp)
	inp = re.sub(r' +', ' ', inp)
	inp = bytes(inp)
	inp = inp.split()
	return inp

def ngrams(inp, n):
	inp = clean(inp)
	out = []
	for i in range(0, len(inp)-n-1):
		s = ''
		for k in range(0, n):
			s = s+' '+inp[i+k]
		out.append(s)
	outset = set(out)
	grams = {item:sum([i==item for i in out]) for item in outset if not isCommon(item)}
	return grams


if __name__ == '__main__':
	content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read())
	ngram = ngrams(content, 2)
	sortedngms = sorted(ngram.items(), key = operator.itemgetter(1), reverse=True)
	topgrams = sortedngms[:5]
     
	tokenizer = PunktSentenceTokenizer()
	tokens = tokenizer.sentences_from_text(content)
	summary = []
	# make a summary of William Henry's speach
	for popgram in topgrams:
		for token in tokens:
			if popgram[0] in token.lower():
				summary.append(token)
				break
	print summary