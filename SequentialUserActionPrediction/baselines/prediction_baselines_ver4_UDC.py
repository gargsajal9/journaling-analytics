'''
Created on Jan 10, 2015

@author: Changsung Moon
'''

import csv
from components import IPAM
from components import FxLTree2
from components import NullModel

import time

start = time.clock()

input_data_file = "datasets/udc_top20_no_bundle.csv"
input_folder = "outputs/train_test_sets_size_v7_UDC/"
sample_input_file = ""

experiment_type = "days"                # ToDo: Remove
rm_query_in_predicted_apps = False      # ToDo: Remove
FxL_use_prev_prob = False               # ToDo: Remove


training_dataset_days = [1000, 2000, 4000, 8000]

num_tests = 5
topN = 3

title = ""


""" Parameters for IPAM """
alpha_IPAM = 0.8

""" Parameters for FxL """
FxL_k = 4



user_black_list = []
all_users = []

with open(input_data_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for r in reader:
        if r[0] == "userId":
            continue
        if r[0] in user_black_list:
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



""" Sample TEST """
#sample_input_file = "output_train_test_sets/simple_test.csv"
"""
sample_input_file = "outputs/train_test_sets_days_UDC_no_bundle_fixed_test_len/csv/1/512621-1.csv"
#sample_input_file = "outputs/train_test_sets_days_UDC_no_bundle_fixed_test_len/csv/1/69963-1.csv"
#sample_input_file = "outputs/train_test_sets_days_UDC_no_bundle_fixed_test_len/sample_test2.csv"
training_dataset_days = [1]
#test_dataset_size = 100
num_tests = 1
test_users = {'512621': 0}
#test_users = {'69963': 0}
"""
""""""""""""""""""""


''' A list of user names '''
test_user_names = test_users.keys()
print test_users

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


