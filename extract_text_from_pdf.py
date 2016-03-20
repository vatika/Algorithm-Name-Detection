from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from os import listdir
from os.path import isfile, join

from nltk.tokenize import sent_tokenize, word_tokenize

import csv
import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#set some globals
rsrcmgr = PDFResourceManager()
retstr = StringIO()
codec = 'utf-8'
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)


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

if __name__ == "__main__":
    count = 0
    features = {}
    #extract features from pdf like word tokens and sentence tokens and save them to a csv file
    with open('features.csv','wb') as csv_file:
        pdf_id = 0
        csv = csv.writer(csv_file)
        for pdf in listdir('small_dataset'):
            try:
                pdf_id += 1
                text = convert_pdf_to_text('small_dataset/'+pdf)
                words = word_tokenize(text.decode('utf-8'))
                sentences = sent_tokenize(text)
                features[pdf_id] = [words, sentences]
            except:
                count += 1
                pass
    json.dump(features, open('data.json', 'wb'))
    print count
    device.close()
    retstr.close()
 
