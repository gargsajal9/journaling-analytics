'''
Created on Jul 9, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''


import csv
from components import fcbow_prediction_4_new_vec


''' Set test environments '''
# Training and test datasets
input_folder = "../datasets/sequence_prediction/train_test_sets_size_v6_RM/"
# To test with a sample file
sample_input_file = ""

# Training sizes
training_dataset_sizes = [500, 1000, 1500, 2000]

num_tests = 5               # Number of tests
topN = 3                    # N number for top N prediction
num_validation_set = 0      # If 0, train with training data and test with test data. 
                            # else use the last "num_validation_set" data in the training data as the validation set


''' Set values for various parameters '''
num_features = 50           # Action vector dimensionality                           
min_word_count = 0          # Minimum action count                 
num_workers = 1             # Number of threads to run in parallel
context = 5                 # Context window size                                                                                    
downsampling = 0            # Downsample setting for frequent actions
cbow_mean = 1               # If 0, use the sum of the context word vectors. If 1, use the mean.
context_labeling = True     # If True, label context actions based on their positions
build_vocab_total = False   # If True, build vocab in CBOW with training and test datasets, else build it with training dataset
alpha_training = 0.3        # Learning rate for training
alpha_test = 0.1            # Learning rate for test
beta = 0.5                  # Score voting rate: score(action) = beta * Prob_freq + (1 - beta) * Prob_vec
update_model = True         # If True, update vectors by backpropagation
update_one_time = False     # If True, update vectors one time with the context length. If False, update them as the length is reduced.

    
    
''' Extract the following test user IDs '''
#all_users = ['25', '20', '21', '22', '23', '4', '8', '57', '53', '52', '81', '102', '100', '38', '36', '67', '93', '12', '49', '40', '41', '75', '70']
# For 84 test users
all_users = ['25', '26', '27', '20', '21', '22', '23', '28', '4', '8', '58', '55', '54', '57', '56', '51', '50', '53', '52', '89', '82', '83', '81', '86', '87', '84', '85', '102', '100', '101', '106', '39', '38', '33', '32', '31', '30', '37', '36', '35', '34', '60', '61', '62', '63', '64', '65', '67', '68', '69', '6', '99', '91', '90', '93', '94', '97', '96', '11', '10', '13', '12', '15', '17', '16', '19', '18', '49', '46', '44', '42', '40', '41', '5', '9', '77', '76', '75', '74', '73', '71', '70', '79', '78']


all_users.sort()

test_users = {}
test_users_num_records = {}

user_i = 0
for user in all_users:
    test_users[user] = user_i
    test_users_num_records[user] = 0
    user_i = user_i + 1
    

''' Sample TEST '''
'''
sample_input_file = "../datasets/test/aaamosbi-1.csv"
num_tests = 1
test_users = {'sample_test': 0}
'''
""""""""""""""""""""


test_user_names = test_users.keys()

            
for training_size in training_dataset_sizes:
    print "\n"
    print "Training size = " + str(training_size)
    
    input_test_data_folder = input_folder + "csv/"
    training_dataset_size = [training_size]
    
    #print "Start: F-CBOW Prediction"
    (means, std, medians) = fcbow_prediction_4_new_vec.run_model(topN, input_test_data_folder, training_dataset_size, test_user_names, num_tests, sample_input_file, num_features, min_word_count, num_workers, context, downsampling, alpha_training, alpha_test, beta, cbow_mean, update_model, context_labeling, build_vocab_total, num_validation_set, update_one_time)
    

    for t in range(0, topN):
        # Skip printing results of top 2
        if t == 1:
            continue
        
        print "Mean for Top " + str(t+1) + " = " + str(means[t])
        print "STD for Top " + str(t+1) + " = " + str(std[t])
        print "Median for Top " + str(t+1) + " = " + str(medians[t])
    
    #print "Done: F-CBOW Prediction"
    
    
'''
context = 5, beta = 0.5

Training size = 500
/Users/csmoon/Documents/workspace/fcbow_seq_prediction/models/word2vec_fcbow.py:535: UserWarning: C extension compilation failed, training will be slow. Install a C compiler and reinstall gensim for fast training.
  warnings.warn("C extension compilation failed, training will be slow. Install a C compiler and reinstall gensim for fast training.")
Mean for Top 1 = [0.53502380952380957]
STD for Top 1 = [0.086380935974167614]
Median for Top 1 = [0.53000000000000003]
Mean for Top 3 = [0.82578571428571423]
STD for Top 3 = [0.077328007528316159]
Median for Top 3 = [0.83999999999999997]


Training size = 1000
Mean for Top 1 = [0.54161904761904767]
STD for Top 1 = [0.083818100210530266]
Median for Top 1 = [0.54000000000000004]
Mean for Top 3 = [0.83059523809523816]
STD for Top 3 = [0.076627596522094013]
Median for Top 3 = [0.83999999999999997]


Training size = 1500
Mean for Top 1 = [0.54254761904761906]
STD for Top 1 = [0.084607976203122881]
Median for Top 1 = [0.54000000000000004]
Mean for Top 3 = [0.83309523809523789]
STD for Top 3 = [0.076559596930013726]
Median for Top 3 = [0.83999999999999997]


Training size = 2000
Mean for Top 1 = [0.54435714285714287]
STD for Top 1 = [0.083294177875930867]
Median for Top 1 = [0.54000000000000004]
Mean for Top 3 = [0.83459523809523817]
STD for Top 3 = [0.075217639624343413]
Median for Top 3 = [0.83999999999999997]
'''

