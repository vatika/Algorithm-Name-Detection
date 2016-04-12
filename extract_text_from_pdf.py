from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import pycountry
from sets import Set
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
from nltk.tag.perceptron import PerceptronTagger
import csv
TAGGER = PerceptronTagger()

from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger()

import json
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#set some globals
rsrcmgr = PDFResourceManager()
#retstr = StringIO()
codec = 'utf-8'
laparams = LAParams()
#device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
REFERENCES ="(References.*)"
CITATIONS = "(\[[^\]]*)([0-9])(?=[^\]]*\])"
REFERENCES_RE = re.compile(REFERENCES)
CITATIONS_RE = re.compile(CITATIONS)
LOCATIONS = []
for x in pycountry.countries:
    LOCATIONS.append(x.name.lower())
    LOCATIONS.append(x.alpha3.lower())
for x in pycountry.subdivisions:
    LOCATIONS.append(x.name.lower())

def citation(sentence):
	tokenized_sentences = [nltk.word_tokenize(sentence)]
	tagged_sentences = [pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
	entity_names = []
	for tree in chunked_sentences:
		entity_names.extend(extract_entity_names(tree))
	resp = []
	named_ents = []
	for name in entity_names:
		try:
			name = name.decode('ascii')
			if name.lower() not in LOCATIONS and name not in named_ents and len(name) > 2 and 'university' not in name.lower() and 'school' not in name.lower() and name not in authors:
					
					named_ents.append(name.lower())
			
		except Exception as e:
			print e
#        print named_ents
	return named_ents


def remove_noise(en):
#	re.compile('')
	pass
def author_names():
	with open('unique_authors.txt.part','rb') as fp:
		name = word_tokenize(fp.read().decode('utf-8'))
	return name


def convert_pdf_to_text(path):
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = False
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()

    retstr.close()
    device.close()
    return text



def extract_entity_names(t):
    entity_names = []
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
    pdf_id = 0 
    for pdf in listdir('small_dataset'):
        filename='file'+str(pdf_id)
        f=open(filename,'w')
		
        pdf_id += 1
        text = convert_pdf_to_text('small_dataset/'+pdf)
        ind=text.index('References')
        text=text[1:ind]
        sentences = sent_tokenize(text.decode('utf-8'))
        new_sents = []
	new_ents = []
        for sent in sentences:
            if len(CITATIONS_RE.findall(sent)) > 0:
                new_sents.append(sent)
        sentences = new_sents
        for sent in sentences:
            new_ents.extend(citation(sent))
        p = set(new_ents)
	print pdf
	print p
        for item in p:
            f.write(item+'\n')
        f.close()
