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
from func.io import convert_docx_to_txt
from func.nlp import doc_to_wordlist
#from func.nlp import append_label_into_vocab
from numpy import zeros, empty, isnan, random, sum as np_sum, uint32, float32 as REAL, vstack


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# Parameter of doc2vec: dm_mean = 0 or 1
sum_or_mean = 'mean'
dm_mean = 1

if sum_or_mean == 'sum':
    dm_mean = 0
else:
    dm_mean = 1


# Load the wiki word2vec model
wiki2vec_model = word2vec.Word2Vec.load("../datasets/wiki2vec/en_1000_no_stem/en.model")
# Use modified doc2vec codes for applying the wiki word2vec model
model = doc2vec_wiki.Doc2Vec(dm_mean=dm_mean, alpha=0.01, min_alpha=0.0001, min_count=5, size=1000, workers=4, train_words=True, train_lbls=True)
model.reset_weights()

# Copy wiki word2vec model to doc2vec model
model.vocab = wiki2vec_model.vocab
model.syn0 = wiki2vec_model.syn0
model.syn1 = wiki2vec_model.syn1
model.index2word = wiki2vec_model.index2word

# Index of the divided dataset based on time period (ex., 1 means the first 3 months of the dataset in this case)
dataset_index = 1
# 0 means the whole months, and number indicates the time period of the divided dataset
months = 3

if months == 0:
    # Input folder path of Monthly Notes dataset
    dataset_folder = "../datasets/LAS_Monthly_Notes_nontxt2/"
    # Output file name to save the doc2vec model
    model_name = "../models/wiki_doc2vec/MN_People_1000feat_5min_8context_" + str(sum_or_mean) + "_NoStopwords_complete_Wiki"
else:
    # Input folder path of Monthly Notes dataset
    dataset_folder = "../datasets/LAS_MN_" + str(dataset_index) + "_3months/"
    # Output file name to save the doc2vec model
    model_name = "../models/wiki_doc2vec/MN_People_1000feat_5min_8context_" + str(sum_or_mean) + "_NoStopwords_" + str(dataset_index) + "_" + str(months) + "months"    
 




# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

users = {}              # to store user label and its word list of the corresponding document
labeled_people = []     # to store user label (for LabeledSentence) and its word list of the corresponding document
sentences = []          
sent_num_start = 0

input_folders = [ sub_dir for sub_dir in listdir(dataset_folder) if isdir(join(dataset_folder, sub_dir)) ]

for folder in input_folders:
    dir_path = dataset_folder + folder + str("/")
    files = [ f for f in listdir(dir_path) if isfile(join(dir_path,f)) ]
    
    for file in files:
        file_path = dir_path + file
        file_name, file_extension = splitext(file_path)
    
        doc = ""
        user = ""
        
        if file_extension == ".pdf":
            user = file.split("_")[0]
            doc = convert_pdf_to_txt(file_path)
        elif file_extension == ".docx":
            user = file.split("_")[0]
            doc = convert_docx_to_txt(file_path)
        else:
            continue
            
        if doc != "":
            doc = doc.decode("utf8")
            doc = doc_to_wordlist(doc)

            if users.has_key(user):
                users[user] += doc
            else:
                users[user] = doc

        
print users.keys()
print "Number of users = " + str(len(users))


# Initial a vector of syn0 and syn1 for a vector of a label
new_syn0 = empty((1, model.layer1_size), dtype=REAL)
new_syn1 = empty((1, model.layer1_size), dtype=REAL)

is_first = True

# Initialize and add a vector of syn0 and syn1 for a vector of a label
for user in users:
    label = 'User_%s' % user
    labeled_people.append(LabeledSentence(words = users[user], labels=[label]))
    
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

   
model.precalc_sampling()

# Train the doc2vec model
model.train(labeled_people)

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







