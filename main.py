from urllib import *
from NLP import NatLang

if __name__ == '__main__':

	content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read())
	nlp = NatLang(content)
	# generate a paragraph using markov model
	print nlp.mkvModel(80)
	#summerize the speach in 5 points
	print nlp.summarize(5)