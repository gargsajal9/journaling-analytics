'''
Created on Jul 9, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''


import csv
from components import fcbow_prediction_4_new_vec


''' Set test environments '''
# The whole dataset to find user IDs
input_data_file = "../datasets/sequence_prediction/udc_top20_no_bundle.csv"
# Training and test datasets
input_folder = "../datasets/sequence_prediction/train_test_sets_size_v7_UDC/"
# To test with a sample file
sample_input_file = ""

# Training sizes
training_dataset_sizes = [1000, 2000, 4000, 8000]

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

    
    
''' Extract test user IDs '''
all_users = []

with open(input_data_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for r in reader:
        if r[0] == "userId":
            continue
        if r[0] not in all_users:
            all_users.append(r[0])

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

Training size = 1000
/Users/csmoon/Documents/workspace/fcbow_seq_prediction/models/word2vec_fcbow.py:535: UserWarning: C extension compilation failed, training will be slow. Install a C compiler and reinstall gensim for fast training.
  warnings.warn("C extension compilation failed, training will be slow. Install a C compiler and reinstall gensim for fast training.")
Mean for Top 1 = [0.48519999999999996]
STD for Top 1 = [0.15129758755512263]
Median for Top 1 = [0.46499999999999997]
Mean for Top 3 = [0.68389999999999995]
STD for Top 3 = [0.13103354532332551]
Median for Top 3 = [0.68000000000000005]


Training size = 2000
Mean for Top 1 = [0.49409999999999998]
STD for Top 1 = [0.14950648815352463]
Median for Top 1 = [0.47999999999999998]
Mean for Top 3 = [0.70600000000000007]
STD for Top 3 = [0.11912178642045292]
Median for Top 3 = [0.70499999999999996]


Training size = 4000
Mean for Top 1 = [0.49970000000000014]
STD for Top 1 = [0.14767840058722195]
Median for Top 1 = [0.47999999999999998]
Mean for Top 3 = [0.71539999999999992]
STD for Top 3 = [0.11829133527017099]
Median for Top 3 = [0.71499999999999997]


Training size = 8000
Mean for Top 1 = [0.50590000000000002]
STD for Top 1 = [0.14519707297325246]
Median for Top 1 = [0.48999999999999999]
Mean for Top 3 = [0.72380000000000011]
STD for Top 3 = [0.11303786976053645]
Median for Top 3 = [0.72999999999999998]
'''

