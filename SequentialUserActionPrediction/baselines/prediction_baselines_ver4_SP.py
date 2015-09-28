'''
Created on Jan 10, 2015

@author: Changsung Moon
'''

from components import IPAM
from components import FxLTree2
from components import NullModel

import time

start = time.clock()


input_folder = "outputs/train_test_sets_size_v6_SP/"
sample_input_file = ""

experiment_type = "days"                # ToDo: Remove
rm_query_in_predicted_apps = False      # ToDo: Remove
FxL_use_prev_prob = False               # ToDo: Remove

training_dataset_days = [500, 1000, 1500, 2000]

num_tests = 5
topN = 3

title = ""




""" Parameters for IPAM """
alpha_IPAM = 0.8

""" Parameters for FxL """
FxL_k = 4



""" For 7 test users """
#test_users = {'pjones':0, 'aaamosbi':1, 'edbrowne':2, 'fdallen':3, 'bird':4, 'keiserjm':5, 'rkavent':6}
""" For 20 test users """
test_users = {'pjones':0, 'aaamosbi':1, 'edbrowne':2, 'fdallen':3, 'bird':4, 'keiserjm':5, 'wfszewc':6, 'mikencs':7, 'rkavent':8, 'LAS':9, 'MargaretSilliman':10, 'Sean':11, 'awhairst':12, 'cemcarter':13, 'chris':14, 'richard':15, 'tmadelsp':16, 'tommy':17, 'wmoxbury':18, 'wpobletts':19}


""" Sample TEST """
#sample_input_file = "output_train_test_sets/simple_test.csv"
"""
sample_input_file = "output_train_test_sets/3000-wfszewc-1.csv"
training_dataset_size = [3000]
test_dataset_size = 100
num_tests = 1
test_users = {'simple_test': 0}
"""
""""""""""""""""""""


#test_users_num_records = {'pjones':0, 'aaamosbi':0, 'edbrowne':0, 'fdallen':0, 'bird':0, 'keiserjm':0}
test_user_names = test_users.keys()
num_users = len(test_user_names)


for training_days in training_dataset_days:
    #input_test_data_folder = input_folder + str(num_repeating) + "/csv/"
    
    print "\n"
    print "Num of training days = " + str(training_days)
    
    input_test_data_folder = input_folder + "csv/"
    training_dataset_size = [training_days]
    test_dataset_size = -1
    
    
    
    print "Start: FxL"
    (means, std, medians) = FxLTree2.run_FxL(topN, input_test_data_folder, training_dataset_size, test_dataset_size, num_users, test_user_names, num_tests, FxL_k, sample_input_file, experiment_type, rm_query_in_predicted_apps, FxL_use_prev_prob)
   
    for t in range(0, topN):
        print "Mean for Top " + str(t+1) + " = " + str(means[t])
        print "STD for Top " + str(t+1) + " = " + str(std[t])
        print "Median for Top " + str(t+1) + " = " + str(medians[t])
    
    print "Done: FxL"
    
    
    print "Start: IPAM"
    (means, std, medians) = IPAM.run_IPAM(topN, input_test_data_folder, training_dataset_size, test_dataset_size, num_users, test_user_names, num_tests, alpha_IPAM, sample_input_file, experiment_type, rm_query_in_predicted_apps)
    
    for t in range(0, topN):
        print "Mean for Top " + str(t+1) + " = " + str(means[t])
        print "STD for Top " + str(t+1) + " = " + str(std[t])
        print "Median for Top " + str(t+1) + " = " + str(medians[t])
    
    print "Done: IPAM"
    
    
    
    print "Start: Null Model Prediction"
    (means, std, medians) = NullModel.run_NullModel(topN, input_test_data_folder, training_dataset_size, test_dataset_size, num_users, test_user_names, num_tests, sample_input_file, experiment_type, rm_query_in_predicted_apps)
    
    for t in range(0, topN):
        print "Mean for Top " + str(t+1) + " = " + str(means[t])
        print "STD for Top " + str(t+1) + " = " + str(std[t])
        print "Median for Top " + str(t+1) + " = " + str(medians[t])
    
    print "Done: Null Model Prediction"
    

end = time.clock()
print end - start
