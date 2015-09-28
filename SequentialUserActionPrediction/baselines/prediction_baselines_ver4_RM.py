'''
Created on Jan 10, 2015

@author: Changsung Moon
'''


from components import IPAM
from components import FxLTree2
from components import NullModel


import time

start = time.clock()

input_data_file = "datasets/RealityMining_apps.csv"
input_folder = "outputs/train_test_sets_size_v6_RM/"
sample_input_file = ""

experiment_type = "days"                # ToDo: Remove
rm_query_in_predicted_apps = False      # ToDo: Remove
FxL_use_prev_prob = False               # ToDo: Remove

training_dataset_days = [500, 1000, 1500, 2000]

num_tests = 5
topN = 3


""" Parameters for IPAM """
alpha_IPAM = 0.8

""" Parameters for FxL """
FxL_k = 4




#all_users = ['25', '20', '21', '22', '23', '4', '8', '57', '53', '52', '81', '102', '100', '38', '36', '67', '93', '12', '49', '40', '41', '75', '70']


""" For 84 test users """
all_users = ['25', '26', '27', '20', '21', '22', '23', '28', '4', '8', '58', '55', '54', '57', '56', '51', '50', '53', '52', '89', '82', '83', '81', '86', '87', '84', '85', '102', '100', '101', '106', '39', '38', '33', '32', '31', '30', '37', '36', '35', '34', '60', '61', '62', '63', '64', '65', '67', '68', '69', '6', '99', '91', '90', '93', '94', '97', '96', '11', '10', '13', '12', '15', '17', '16', '19', '18', '49', '46', '44', '42', '40', '41', '5', '9', '77', '76', '75', '74', '73', '71', '70', '79', '78']

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

