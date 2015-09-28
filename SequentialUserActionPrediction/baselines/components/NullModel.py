'''
Created on Apr 26, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''
import csv
import numpy
from copy import deepcopy
from functions import functions_SP


def run_NullModel(topN, input_test_data_folder, training_dataset_size, test_dataset_size, num_users, test_user_names, num_tests, sample_input_file, experiment_type, rm_query_in_predicted_apps):
    is_sample_test = False
    
    if sample_input_file != "":
        is_sample_test = True

    means = []
    std = []
    medians = []
    
    for i in range(0, topN):
        means.append([])
        std.append([])
        medians.append([])
    
    for t_size in training_dataset_size:
        folder_size = t_size
        test_results_accuracy = [[0 for x in xrange((num_tests*num_users))] for x in xrange(topN)]
        result_i = 0
        for user in test_user_names:
            #print user

            for test_i in range(1, (num_tests+1)):
                
                top_accuracy = numpy.zeros(topN)
                
                if is_sample_test == True:
                    input_data_file = sample_input_file
                else:
                    input_data_file = input_test_data_folder + str(folder_size) + "/" + str(user) + "-" + str(test_i) + ".csv"
                
                #print input_data_file
                
                if experiment_type == "days":
                    with open(input_data_file, 'r') as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for r in reader:
                            t_size = int(r[0])
                            test_dataset_size = int(r[1])
                            break
                
                (data_item_seq, data_timestamp_seq) = functions_SP.extract_app_seq_from_csv(input_data_file, t_size)
                training_seq = data_item_seq[0:t_size]
                test_seq = data_item_seq[t_size:(t_size+test_dataset_size)]
                
                uniq_item_seq = list(set(data_item_seq))
                uniq_item_seq.sort()
                num_uniq_item = len(uniq_item_seq)
                
                
                ''' Prediction '''
                
                for next_item_i in range(0, len(test_seq)):  
                    #top = numpy.zeros(topN)
                    top = [-1, -1, -1]
                    
                    cur_item_i = next_item_i - 1
                    
                    if next_item_i == 0:
                        prev_item = training_seq[(t_size - 1)]
                    else:
                        prev_item = test_seq[cur_item_i]
                        
                        
                    next_item = test_seq[next_item_i]
                    
                    #sub_test_seq = []
                    
                    if cur_item_i > 0:
                        sub_test_seq = list(test_seq[0:(cur_item_i+1)])
                        #sub_test_seq = test_seq[0:(cur_item_i+1)]
                        #sub_test_seq.append(test_seq[0:(cur_item_i+1)])
                    else:
                        sub_test_seq = list(training_seq[(t_size - 1)])
                        #sub_test_seq = training_seq[(t_size - 1)]
                        #sub_test_seq.append(training_seq[(t_size - 1)])
                    
                    #print sub_test_seq
                    
                    top_i = 0
                    
                    if len(sub_test_seq) == 1:
                        for i in range(0, topN):
                            top[i] = sub_test_seq[0]
                    elif len(sub_test_seq) == 2:
                        top[0] = sub_test_seq[1]
                        top[1] = sub_test_seq[0]
                        top[2] = sub_test_seq[0]
                    elif len(sub_test_seq) == 3:
                        top[0] = sub_test_seq[2]
                        top[1] = sub_test_seq[1]
                        top[2] = sub_test_seq[0]
                    else:
                        for i in range(0, len(sub_test_seq)):
                            j = (len(sub_test_seq) - 1) - i
                            cur_item = sub_test_seq[j]
                            if cur_item not in top:
                                #print cur_item
                                top[top_i] = cur_item
                                top_i = top_i + 1
                            
                            if top_i >= topN:
                                break
                    
                    if rm_query_in_predicted_apps == True:
                        try:
                            top.remove(prev_item)
                        except ValueError:
                            pass
                    
                    '''
                    print sub_test_seq
                    print next_item     
                    print top
                    print "\n"
                    '''
                    
                    for t in range(0, topN):
                        if top[t] == next_item:
                            for k in range(t, topN):
                                top_accuracy[k] = top_accuracy[k] + 1
                            break
                    
    
                
                
                for t in xrange(0, topN):
                    test_results_accuracy[t][result_i] = float(top_accuracy[t]) / float(test_dataset_size)
                
                #print test_results_accuracy    
                
                result_i = result_i + 1
                
                #print float(top_accuracy[0]) / float(test_dataset_size)
        """        
        print "Training dataset size = " + str(t_size)
        print "Mean for Top 1 = " + str(numpy.mean(test_results_accuracy[0]))
        print "Mean for Top 2 = " + str(numpy.mean(test_results_accuracy[1]))
        print "Mean for Top 3 = " + str(numpy.mean(test_results_accuracy[2]))  
        """
        
        for t in range(0, topN):
            means[t].append(numpy.mean(test_results_accuracy[t]))
            std[t].append(numpy.std(test_results_accuracy[t]))
            medians[t].append(numpy.median(test_results_accuracy[t]))
                
    return (means, std, medians)
                
                