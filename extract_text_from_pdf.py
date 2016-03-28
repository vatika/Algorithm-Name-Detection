from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import pycountry

from os import listdir
from os.path import isfile, join
import nltk
import nltk.corpus
from nltk.corpus import brown
from nltk.corpus import treebank
import nltk.tag
from nltk import tokenize, ne_chunk_sents
from nltk import word_tokenize
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize

import csv

from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()

import json
import re
#import geograpy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#set some globals
rsrcmgr = PDFResourceManager()
retstr = StringIO()
codec = 'utf-8'
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
locations=[]
for x in pycountry.countries:
    locations.append(x.name.lower())
for x in pycountry.subdivisions:
    locations.append(x.name.lower())
print locations
def remove_noise(en):
#	re.compile('')
	pass
def author_names():
	with open('unique_authors.txt.part','rb') as fp:
		name = word_tokenize(fp.read().decode('utf-8'))
	return name

def convert_pdf_to_text(path):
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    
    return text



def extract_entity_names(t):
    entity_names = []
#    print t   
    if hasattr(t, 'label') and t.label:
#	print t.label()
        if t.label() == 'NE':
#	    print t

            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
                
    return entity_names

if __name__ == "__main__":
    authors = author_names()
    count = 0
    features = {}
    #extract features from pdf like word tokens and sentence tokens and save them to a csv file
    with open('features.csv','wb') as csv_file:
        pdf_id = 0
        csv = csv.writer(csv_file)
        for pdf in listdir('small_dataset'):
            
                pdf_id += 1
                text = convert_pdf_to_text('small_dataset/'+pdf)
	
                words = word_tokenize(text.decode('utf-8'))
		p=nltk.pos_tag(words)
#		print p
		x = 0
        
		entity_names = []

		sentences = sent_tokenize(text.decode('utf-8'))
		tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
#		print tokenized_sentences
		tagged_sentences = [tagger.tag(sentence) for sentence in tokenized_sentences]
		chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
#		print chunked_sentences
		for tree in chunked_sentences:
#			print tree
			entity_names.extend(extract_entity_names(tree))
		resp = []
		for name in entity_names:
			try:
				#name = name.decode('ascii')
				#places = geograpy.get_place_context(url=name)
				if name.lower() not in locations and name not in resp and len(name) > 2 and 'university' not in name.lower() and 'school' not in name.lower() and name not in authors:
					resp.append(name.lower())
			except:
				pass
		for name in resp:
			print name
		print len(resp)
		break
                #features[pdf_id] = [words, sentences]
		
                json.dump(features, open('data.json', 'wb'))
    print count
    device.close()
    retstr.close()
 
