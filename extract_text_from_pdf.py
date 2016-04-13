import numpy

from gensim.models import Word2Vec

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
#CITATIONS = "(\([^\)]*)(?=[\d{4}+])(?=[^\)]*\))"
REFERENCES_RE = re.compile(REFERENCES)
CITATIONS_RE = re.compile(CITATIONS)
LOCATIONS = []
for x in pycountry.countries:
    LOCATIONS.append(x.name.lower())
    LOCATIONS.append(x.alpha3.lower())
for x in pycountry.subdivisions:
    LOCATIONS.append(x.name.lower())

true_positives = []
false_positives = []

with open('true_positives', 'r') as f:
	for word in f.readlines():
		true_positives.append(word.strip())

with open('false_positives', 'r') as f:
	for word in f.readlines():
		false_positives.append(word.strip())

MODEL = Word2Vec.load("model3.dat")

TRUES = []
FALSES = []

for word in true_positives:
	try:
		TRUES.append(MODEL[word])
	except:
		pass

for word in false_positives:
	try:
		FALSES.append(MODEL[word])
	except:
		pass

print true_positives
print false_positives

TESTING = {
    'Analyzing The Role Of Dimension Arrangement For Data Visualization in Radviz\t.pdf': [],
    'A Coupled Clustering Approach for Items Recommendation.pdf': ['cf', 'cbf' ,'clustknn'],
    'An Approach to Identifying False Traces\nin Process Event Logs.pdf': [],
    'A Generic Classifier-Ensemble Approach for Biomedical\nNamed Entity Recognition.pdf': ['svm', 'crf', 'memm', 'hmm'],
    'A New Evaluation Function for Entropy-based Feature Selection from Incomplete Data.pdf': ['efs','lfs','pfs'],
    "A Framework for Large-Scale Train Trip Record Analysis and Its Application to Passengers' Flow Prediction after Train Accidents.pdf": [],
    'Topic Segmentation with an Aspect Hidden Markov Model\t.pdf': ['hmm'],
    'Large Scale Topic Assignment on Multiple Social Networks\t.pdf': [],
    'A Fast Secure Dot Product Protocol with Application to\nPrivacy Preserving Association Rule Mining.pdf': [],
    'An aggressive margin-based algorithm for incremental learning\t.pdf': ['svm'],
    'Analyzing Location Predictability on\nLocation-Based Social Networks.pdf': [],
    'Topic Modeling Using Collapsed Typed\nDependency Relations.pdf': ['lda'],
    'A Framework for SQL-based Mining of Large Graphs on Relational Databases.pdf': [],
    'Efficiently Depth-First Minimal Pattern Mining.pdf': ['acminer','ndi'],
    'A Graphical Model for Collective Behavior Learning Using Minority Games.pdf': [],
    'A Concept-drifting Detection Algorithm for Categorical Evolving Data\t.pdf': [],
    'MultiTask Metric Learning on Network Data.pdf': [],
    'A New Framework for Dissimilarity and Similarity Learning\t.pdf': ['nca','mcml','lmnn'],
    'A Double-Ensemble Approach for Classifying Skewed Data Streams.pdf': ['SDM07','SEA'],
    'An Efficient GA-Based Algorithm for Mining Negative Sequential Patterns.pdf': ['pnsp','gsp'],
    'An Associative Classifier For Uncertain Datasets.pdf': ['DTU','uRule','uHARMONY','UCBA'],
    'An Approach for Fast Hierarchical Agglomerative Clustering using Graphics Processors with CUDA\t.pdf': [],
    'A Graph Matching Method for Historical\nCensus Household Linkage.pdf': [],
    'A Novel Framework to Improve siRNA Efficacy Prediction.pdf': ['BIOPREDsi','DSIR','Thermocomposition21','SVM'],
    

}

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
    mainfile = open("mainfile", "w")
    for pdf in listdir('small_dataset'):
        print "%s: []," % repr(pdf)
    for pdf in listdir('small_dataset'):
        filename='file'+str(pdf_id)
        f=open(filename,'w')
        print pdf
		
        pdf_id += 1
        try:
            text = convert_pdf_to_text('small_dataset/'+pdf)
#            print text
        except:
            continue
        try:
            ind=text.index('References')
            text=text[1:ind]
        except:
            pass
        sentences = sent_tokenize(text.decode('utf-8'))
        new_sents = []
        new_ents = []
#        for sent in sentences:
#            if len(CITATIONS_RE.findall(sent)) > 0:
#                new_sents.append(sent)
#        sentences = new_sents
#        print "*"*30
        for sent in sentences:
            temp_ents = citation(sent)
#            print temp_sent, type(temp_sent)
            if len(CITATIONS_RE.findall(sent)) > 0:
#                print CITATIONS_RE.findall(sent)
                new_ents.extend(temp_ents)
#                print temp_ents
#        print "*"*30
        p = set(new_ents)
#        print pdf
#        print p
        precision = 0
        for item in p:
            min_true = 10000000000000
            min_false = 10000000000000
            sum_true = 0
            sum_false = 0
            WORD1 = item
            try:
                word1 = MODEL[item]
                for word2 in TRUES:
                    dist = numpy.linalg.norm(word1 - word2)
		    sum_true+=dist
                    min_true = min(min_true, dist)
                for word2 in FALSES:
                    dist = numpy.linalg.norm(word1 - word2)
                    min_false = min(min_false, dist)
		    sum_false+=dist
#                print WORD1, min_true, min_false
#                if min_true < min_false:
#                    print "first"
#                    print WORD1, min_true, min_false
                sum_true = sum_true / len(TRUES)
                sum_false = sum_false / len(FALSES)
                if min_true < min_false or sum_true < sum_false:
                    if WORD1 in TESTING[pdf]:
                        precision += 1
#                    print WORD1
            except Exception as e:
#                print "-"*30
#                print e
#                print "-"*30
                pass

            mainfile.write(item + "\n")
            f.write(item+'\n')
        f.close()
        if len(TESTING[pdf]) == 0:
            recall = 1
        else:
            recall = precision / float(len(TESTING[pdf]))
        if len(p) == 0:
            precision = 1
        else:
            precision = precision / float(len(p))
        print pdf
        print "RECALL: " + str(recall)
        print "PRECISION: " + str(precision)
    mainfile.close()
