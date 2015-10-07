from io import StringIO

import logging
import nltk

from os import listdir
from os.path import isfile, isdir, join, splitext
from gensim.models import word2vec
from gensim.models import doc2vec
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from func.io import convert_pdf_to_txt
from func.io import convert_docx_to_txt
from func.nlp import doc_to_sentences
from func.nlp import words_to_phrases

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dataset_folder = "./CSC791_Corpus_Pdf/"     # For Monthly Notes dataset


# Load the punkt tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

sentences = []      # Initialize an empty list of sentences

input_folders = [ sub_dir for sub_dir in listdir(dataset_folder) if isdir(join(dataset_folder, sub_dir)) ]
for folder in input_folders:
    dir_path = dataset_folder + folder + str("/")
    files = [ f for f in listdir(dir_path) if isfile(join(dir_path,f)) ]
    for file in files:
        #file = file.replace(".","")
        file_path = dir_path + file
        file_name, file_extension = splitext(file_path)
        doc = ""

        try:
            if file_extension == ".pdf":
                doc = convert_pdf_to_txt(file_path)
            elif file_extension == ".docx":
                doc = convert_docx_to_txt(file_path)
            else:
                continue
        except:
            continue

        if doc != "":
            doc = doc.decode("utf8")
            doc = words_to_phrases(doc)
            doc = doc.lower()

            sentences += doc_to_sentences(doc, tokenizer, remove_stopwords=False)


print len(sentences)
# sentences_string = ""
# for item in sentences:
#     item = " ".join(item)
#     sentences_string += "\n"+item
#
#
# with open("sentences.txt", "w") as text_file:
#     text_file.write("%s" % sentences_string)
#print sentences[0]


# Set values for various parameters
num_features = 300    # Word vector dimensionality
min_word_count = 10   # Minimum word count
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words

# Initialize and train the model (this will take some time)
print "Training model..."
model = word2vec.Word2Vec(sentences, workers=num_workers, size=num_features, min_count = min_word_count, window = context, sample = downsampling)
# If you don't plan to train the model any further, calling
# init_sims will make the model much more memory-efficient.
model.init_sims(replace=True)

# It can be helpful to create a meaningful model name and
# save the model for later use. You can load it later using Word2Vec.load()
model_name = "CSC791_Corpus_300features_10minwords_10context_FalseStopwords_Phrase"
model.save(model_name)



