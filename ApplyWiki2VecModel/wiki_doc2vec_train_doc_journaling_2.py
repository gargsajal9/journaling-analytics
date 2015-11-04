'''
Created on Oct 23, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''


import logging
import nltk

from os import listdir
from os.path import isfile, isdir, join, splitext

from gensim_models import word2vec
from gensim_models import doc2vec_wiki
from gensim_models.doc2vec import LabeledSentence

from func.io import convert_pdf_to_txt
from func.nlp import doc_to_wordlist

from numpy import zeros, empty, isnan, random, sum as np_sum, uint32, float32 as REAL, vstack




logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# Load the wiki word2vec model
wiki2vec_model = word2vec.Word2Vec.load("../datasets/wiki2vec/en_1000_no_stem/en.model")
# Use modified doc2vec codes for applying the wiki word2vec model
model = doc2vec_wiki.Doc2Vec(dm_mean=1, alpha=0.01, min_alpha=0.0001, min_count=5, size=1000, workers=4, train_words=True, train_lbls=True)
model.reset_weights()

# Copy wiki word2vec model to doc2vec model
model.vocab = wiki2vec_model.vocab
model.syn0 = wiki2vec_model.syn0
model.syn1 = wiki2vec_model.syn1
model.index2word = wiki2vec_model.index2word


# Input folder path of CSC 791 dataset
dataset_folder = "../datasets/CSC791_Corpus_Pdf/"     

# Output file name to save the doc2vec model
model_name = "../models/wiki_doc2vec/CSC791_Doc_1000feat_5min_8context_mean_NoStopwords_complete_Wiki"

# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

labeled_sent = []
sentences = []      # Initialize an empty list of sentences
sent_num_start = 0

input_folders = [ sub_dir for sub_dir in listdir(dataset_folder) if isdir(join(dataset_folder, sub_dir)) ]

doc_labels = {}     # to store doc label and its word list of the corresponding document
labeled_docs = []   # to store doc label (for LabeledSentence) and its word list of the corresponding document
total_labels = []

for folder in input_folders:
    print str(folder)
    file_paths = []
    
    dir_path = dataset_folder + folder + str("/")
    files = [ f for f in listdir(dir_path) if isfile(join(dir_path,f)) if ".pdf" in f ]
    sub_dir = [ d for d in listdir(dir_path) if isdir(join(dir_path,d)) ]
    #print sub_dir
    
    for file_name in files:
        file_paths.append(dir_path + file_name)
    
    if len(sub_dir) > 0:
        sub_dir_path = dir_path + sub_dir[0] + str("/")
        files = [ f for f in listdir(sub_dir_path) if isfile(join(sub_dir_path,f)) if ".pdf" in f ]
        sub_dir2 = [ d for d in listdir(sub_dir_path) if isdir(join(sub_dir_path,d)) ]
        
        for file_name in files:
            file_paths.append(sub_dir_path + file_name)
        
        if len(sub_dir2) > 0:
            for subsub_dir in sub_dir2:
                subsub_dir_path = sub_dir_path + subsub_dir + str("/")
                files = [ f for f in listdir(subsub_dir_path) if isfile(join(subsub_dir_path,f)) if ".pdf" in f ]
                
                for file_name in files:
                    file_paths.append(subsub_dir_path + file_name)
                    
    #print file_paths
    #print len(file_paths)
    
    label_i = 1
    
    for file_path in file_paths:
        doc = convert_pdf_to_txt(file_path)
        
        if doc != "":
            doc = doc.decode("utf8")
            doc = doc_to_wordlist(doc, remove_stopwords=True)
            label = str(folder) + "_" + str(label_i)
            label_i = label_i + 1
            
            doc_labels[label] = doc



# Initial a vector of syn0 and syn1 for a vector of a label
new_syn0 = empty((1, model.layer1_size), dtype=REAL)
new_syn1 = empty((1, model.layer1_size), dtype=REAL)

is_first = True

# Initialize and add a vector of syn0 and syn1 for a vector of a label
for doc_label in doc_labels:
    label = 'Doc_%s' % doc_label
    total_labels.append(doc_label)
    labeled_docs.append(LabeledSentence(words = doc_labels[doc_label], labels=[label]))
    
    v = model.append_label_into_vocab(label)    # I made this function in the doc2vec code
    
    random.seed(uint32(model.hashfxn(model.index2word[v.index] + str(model.seed))))
    
    if is_first == True:
        new_syn0[0] = (random.rand(model.layer1_size) - 0.5) / model.layer1_size
        new_syn1[0] = zeros((1, model.layer1_size), dtype=REAL)
        
        is_first = False
    else:
        new_syn0 = vstack([new_syn0, (random.rand(model.layer1_size) - 0.5) / model.layer1_size])
        new_syn1 = vstack([new_syn1, zeros((1, model.layer1_size), dtype=REAL)])

model.syn0 = vstack([model.syn0, new_syn0])
model.syn1 = vstack([model.syn1, new_syn1])

#print total_labels
#print len(total_labels)

model.precalc_sampling()

# Train the doc2vec model
model.train(labeled_docs)

# Convert "nan" values into "0" in vectors
indices_nan = isnan(model.syn0)
model.syn0[indices_nan] = 0.0

indices_nan = isnan(model.syn1)
model.syn1[indices_nan] = 0.0


# If you don't plan to train the model any further, calling 
# init_sims will make the model much more memory-efficient.
model.init_sims(replace=True)

# It can be helpful to create a meaningful model name and 
# save the model for later use. You can load it later using Word2Vec.load()
model.save(model_name)


