#Sophia Kennedy
#WL78890
#importing modules
import os
import glob
import re
import sys
import html2text
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
    def __init__(self, output_path):
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
        




#Calling the main function        
def main():
    start_time=time.time()
    input_path= args['<files>']
    number_of_files = 503
    Listing_query = args['<query_term_weights>'].split()
    
    try:
        os.mkdir(output_path) #Creating a directory if one is not present
    except:
        pass
    #classes Tokenization and Calcal_wts 
    token_izer = Tokenization()
    cal_wts=Calcal_wts()

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
    print(cal_wts.avg_doc_len)
    
    #Finding average of the document length by dividing it with the number of total docs
    cal_wts.avg_doc_len /= float(cal_wts.total_docs)
    print(cal_wts.avg_doc_len)

    
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
    inv_index = Index(output_path)
    for i in range(0, number_files):
        List_docs = Files_List[i]
        size_docs = sum(cal_wts.doc_term_frequency[List_docs].values()) #length of document
        for word in cal_wts.doc_term_frequency[List_docs].keys():
            inv_index.weights[word][List_docs] = cal_wts.term_freq_inverse_doc_freq(word, List_docs, size_docs) #Creating the term weight dictionary

    Posting_id = 0 #variable for Post_ing index counter
    Posting_output = "doc id, term weight\n"
    dictionary_output = "term\ndocument frequency\nLocation of first record in Post_ings file"
    tuple_dictionary = []
    for term in inv_index.weights.keys():
        for doc in inv_index.weights[term].keys():
            Posting_output +=  "%s \t %.8f \n" %(doc, inv_index.weights[term][doc])
            Posting_id += 1
        tuple_dictionary.append((term, str(cal_wts.inverse_doc_freq_uency[term]),
            str(Posting_id - cal_wts.inverse_doc_freq_uency[term] + 1)))
    tuple_dictionary.sort() #sorting based on the term
    dictionary_output +=''.join("\n%s" % '\n'.join(map(str, x)) for x in tuple_dictionary) #string formatting for dictionary

      
    #Writing the output files
    bop=output_path+ '/'+"post_ings.txt"
    with open(bop,'a+',encoding='utf-8') as f2:
        fil=f2.write(Posting_output)
    
    
 
    aop=output_path+'/'+"Dictionary.txt"
    with open(aop,'a+',encoding='utf-8')as f3:
        fil1=f3.write(dictionary_output)
   
    end_time=time.time()
    
    print("tOTAL TIME:" ,end_time-start_time)

    #Printing the size of the files in mb
    print("Postings")
    print(compute_file_size(bop))
    print("Dictionary")
    print(compute_file_size(aop))

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Retrieve 1.0')
    main(arguments)
    
    
