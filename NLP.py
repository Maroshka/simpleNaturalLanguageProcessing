from urllib import *
from bs4 import BeautifulSoup
import string
import re
import operator
from nltk import PunktSentenceTokenizer
from random import randint

class NatLang(object):
	"""docstring for NatLang"""
	def __init__(self, text):
		super(NatLang, self).__init__()
		self.text = text

	@staticmethod
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

	@staticmethod
	def clean(inp):
		inp = inp.lower()
		inp = re.sub(r'((?![\w\s]).)*', '', inp)
		inp = re.sub(r'[0-9\n+]', ' ',inp)
		inp = re.sub(r' +', ' ', inp)
		inp = bytes(inp)
		inp = inp.split()

		return inp

	@staticmethod
	def buildWordDict(wdlist):
		wdDict = {}
		for i in range(0, len(wdlist)-2):
			if wdlist[i] not in wdDict:
				wdDict[wdlist[i]] = {}
			if wdlist[i+1] not in wdDict[wdlist[i]]:
				wdDict[wdlist[i]][wdlist[i+1]] = 1
			else:
				wdDict[wdlist[i]][wdlist[i+1]] += 1 

		return wdDict

	@staticmethod
	def ngrams(inp, n):
		inp = NatLang.clean(inp)
		out = []
		for i in range(0, len(inp)-n-1):
			s = ''
			for k in range(0, n):
				s = s+' '+inp[i+k]
			out.append(s)
		outset = set(out)
		grams = {item:sum([i==item for i in out]) for item in outset if not NatLang.isCommon(item)}

		return grams

	def mkvModel(self,n):
		wdlist = NatLang.clean(self.text)
		wdDict = NatLang.buildWordDict(wdlist)
		startwd = wdlist[randint(0, len(wdlist)-1)]
		chain = ''
		for i in range(0, n):
			chain = chain+' '+startwd
			tmpdict = wdDict[startwd]
			# print startwd
			startwd = tmpdict.keys()[randint(0, len(tmpdict.keys())-1)]
		chain = re.sub(r'^\s', '', chain)
		chain = chain[0].upper()+chain[1:]

		return chain

	def summarize(self,n):
		#n is the number of points you want the summary to consist of
		tokenizer = PunktSentenceTokenizer()
		tokens = tokenizer.sentences_from_text(self.text)
		summary = []
		# make a summary of William Henry's speach
		ngram = NatLang.ngrams(self.text, 2)
		sortedngms = sorted(ngram.items(), key = operator.itemgetter(1), reverse=True)
		topgrams = sortedngms[:n]
		for popgram in topgrams:
			for token in tokens:
				if popgram[0] in token.lower():
					summary.append(token)
					break

		return summary
		