
#importing modules
"""
Usage:
  retrieve.py wts <files> <query_term_weights>
  retrieve.py -h | --help
  retrieve.py --version

Arguments:
    wts specify weights to query terms

Options:
  -h --help     Show this screen.
  --version     Show version.

"""



import operator
import os
import sys
import html2text
import collections
from nltk.tokenize import word_tokenize
from operator import itemgetter
import collections
from collections import OrderedDict
from collections import Counter
import time
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import math
import time
from docopt import docopt

class Tokenization:
    def __init__(self):
        try:
            self.stopwords = open('stoplist.txt').read().splitlines() #from file
            self.stopwords.extend(nltk.corpus.stopwords.words('english')) #from nltk corpus
        except Exception:
            pass
        
    #Extract text from html
    def extract_html(self,file1):
        Extract_html=html2text.html2text(file1.read())
        return Extract_html

    
	

    def token_it(self,text):
        tokenizer = RegexpTokenizer('[a-zA-Z]\w+\'?\w*')
        tokens =tokenizer.tokenize(text)
        words = [w.lower() for w in tokens if len(w) > 2]
        #Code to remove Stopwords
        words = [word for word in words if word not in self.stopwords]
        return words


class Index:
    """Variables to build index"""
    def __init__(self):
        self.weights = collections.defaultdict(dict) #term : document : normalized term weight
        

def compute_file_size(file):
    #Function to Compute the file size in MB
    megb = 1024*1024.0
    if type(file) is list: #Return for multiple files
        return sum([os.path.getsize(filename) for filename in file]) / megb
    else: #Return for a single file
        return os.path.getsize(file)/ (megb)



class Calcal_wts:

    def __init__(self):
        
        self.doc_term_frequency = collections.defaultdict(dict) #document : term : freq_uency
        self.total_docs = 0 #Total Number of documents
        self.avg_doc_len = 0 #Average length of documents
        self.inverse_doc_freq_uency = {} #Inverse Document freq_uency

    

    def freq_uency(self, tokens):
        #Computing the frequency of tokens and its frequency
        index = {}
        for (term, freq_uency) in collections.Counter(tokens).items():
            index[term] = freq_uency
            
        return index
    
    def inverse_frequency(self,Total_freq):
        self.inverse_doc_freq_uency.update(Total_freq)
        with open('total_freq.txt','w+',encoding='utf-8') as freq_file:
            freq_file.write(str(self.inverse_doc_freq_uency))
            
    def score(self,Total_freq,freq):
        #calculating the score by dividing the frequency of a doc with total freq
        score=freq / float(Total_freq)
        return score


    
    def idf(self, word):
        #formula to compute inverse document frequency
        return math.log(self.total_docs / float(self.inverse_doc_freq_uency[word]))
   
    def term_freq_inverse_doc_freq(self, word, doc, doclength):
        #The final computation
        term_freq_uency = self.doc_term_frequency[doc][word]
        tf_value = self.score(term_freq_uency, doclength)
        idf_value = self.idf(word)
        return tf_value * idf_value
        


def file_id(doc):
    return os.path.basename(doc)

#Calling the main function        
def main(args):
    start_time=time.time()
    input_path= args['<files>']
    number_of_files = 503
    query_list = args['<query_term_weights>'].split()
    
    #classes Tokenization and Calcal_wts 
    token_izer = Tokenization()
    cal_wts=Calcal_wts()


    #Code to convert into a query vector dictionary
    query_vector = {}
    query_tuple = zip(query_list[::2],query_list[1::2])
    for wt, qt in query_tuple:
        final_query_term = token_izer.token_it(qt)
        if len(final_query_term) > 0:
            query_vector[final_query_term[0]] = eval(wt)

    #iterating through the input files for the task of tokenization
    for file in os.listdir(input_path):  #iterate through the list of directories in the input path
        cur_dir=os.path.abspath(input_path)+'/'+file
        ip=os.listdir(input_path)
        file1=open(cur_dir,'r',encoding='utf-8',errors='ignore')
        text=token_izer.extract_html(file1)
        tokens=token_izer.token_it(text)
        Frequency_term=cal_wts.freq_uency(tokens)
        splitting_file=os.path.splitext(file)
        
        
        Total_frequency=cal_wts.inverse_frequency(Frequency_term)
        for tok in tokens:
            cal_wts.doc_term_frequency[splitting_file[0]][tok]=Frequency_term[tok]
            
    #Creating a words_bag for storing the words
    words_bag = []
    for docs in cal_wts.doc_term_frequency.values():
        words_bag.extend(docs.keys()) # code for computing document freq_uency in idf
    cal_wts.inverse_doc_freq_uency = cal_wts.freq_uency(words_bag)
    cal_wts.total_docs = len(cal_wts.doc_term_frequency.keys())

    #Adding up the values in the doc_term_frequency to find the length of values in all docs
    for d in cal_wts.doc_term_frequency.keys():
        cal_wts.avg_doc_len += sum(cal_wts.doc_term_frequency[d].values())
    
    #Finding average of the document length by dividing it with the number of total docs
    cal_wts.avg_doc_len /= float(cal_wts.total_docs)
    

    
    #Number of files in the input directory
    list = os.listdir(input_path) 
    number_files = len(list)

    #Creating a list of names of files in the input directory
    Files_List=[]
    for file in os.listdir(input_path):  #iterate through the list of directories in the input path
        cur_dir=os.path.abspath(input_path)+'/'+file
        splitting_file=os.path.splitext(file) #Splits the file from ".html"
        Files_List.append(splitting_file[0]) 

    #Code for inverted index
    inv_index = Index()
    for i in range(0, number_files):
        List_docs = Files_List[i]
        size_docs = sum(cal_wts.doc_term_frequency[List_docs].values()) #length of document
        for word in cal_wts.doc_term_frequency[List_docs].keys():
            inv_index.weights[word][List_docs] = cal_wts.term_freq_inverse_doc_freq(word, List_docs, size_docs) #Creating the term weight dictionary

    #code for similarity scores
    similar_scores = {key: 0 for key in Files_List}
    for term, wt in query_vector.items():
        for doc in inv_index.weights[term].keys():
            similar_scores[doc]  += inv_index.weights[term][doc] * wt #code to calculate similarity score

    similar_scores_n = {file_id(k):v for k,v in similar_scores.items() if v != 0} # calculation for non zero similarity scores
    if len(similar_scores_n) > 0:
        sorted_scores = sorted(similar_scores_n.items(),key=itemgetter(1),reverse=True )
        print(sorted_scores[:10])


if __name__=='__main__':
    arguments = docopt(__doc__, version='Retrieve 1.0')
    main(arguments)
   

    
