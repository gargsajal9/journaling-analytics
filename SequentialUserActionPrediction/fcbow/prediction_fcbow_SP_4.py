'''
Created on Jul 9, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''


import csv
from components import fcbow_prediction_4_new_vec


''' Set test environments '''
# Training and test datasets
input_folder = "../datasets/sequence_prediction/train_test_sets_size_v6_SP/"
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

    
    
''' For 7 test users '''
#test_users = {'pjones':0, 'aaamosbi':1, 'edbrowne':2, 'fdallen':3, 'bird':4, 'keiserjm':5, 'rkavent':6}
''' For 20 test users '''
test_users = {'pjones':0, 'aaamosbi':1, 'edbrowne':2, 'fdallen':3, 'bird':4, 'keiserjm':5, 'wfszewc':6, 'mikencs':7, 'rkavent':8, 'LAS':9, 'MargaretSilliman':10, 'Sean':11, 'awhairst':12, 'cemcarter':13, 'chris':14, 'richard':15, 'tmadelsp':16, 'tommy':17, 'wmoxbury':18, 'wpobletts':19}

    

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
    

