'''
Created on Jan 15, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''

import csv
import numpy
from copy import deepcopy
from functions import functions_SP


def update_row(state_table, row_to_change, app, alpha_IPAM):
    for i in range(0, len(state_table[row_to_change])):
        if i == app:
            state_table[row_to_change][i] = state_table[row_to_change][i] + float(1 - alpha_IPAM)
        else:
            state_table[row_to_change][i] = state_table[row_to_change][i] * alpha_IPAM
                       
    row_sum = numpy.sum(state_table[row_to_change])
    #print row_sum
    if row_sum > 1:
        gap = row_sum - 1
        state_table[row_to_change][app] = state_table[row_to_change][app] - gap  
        #print gap
    elif row_sum < 1:
        gap = 1 - row_sum
        state_table[row_to_change][app] = state_table[row_to_change][app] + gap 
        #print gap
        
    return state_table



def run_IPAM(topN, input_test_data_folder, training_dataset_size, test_dataset_size, num_users, test_user_names, num_tests, alpha_IPAM, sample_input_file, experiment_type, rm_query_in_predicted_apps):
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
            #print "user = " + str(user)
            #test_results_accuracy = [[0 for x in xrange(num_tests)] for x in xrange(3)]
            for test_i in range(1, (num_tests+1)):
                
                top_accuracy = numpy.zeros(topN)
                
                if is_sample_test == True:
                    input_data_file = sample_input_file
                else:
                    input_data_file = input_test_data_folder + str(folder_size) + "/" + str(user) + "-" + str(test_i) + ".csv"
                
                
                if experiment_type == "days":
                    with open(input_data_file, 'r') as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for r in reader:
                            t_size = int(r[0])
                            test_dataset_size = int(r[1])
                            break
                
                (data_app_seq, data_timestamp_seq) = functions_SP.extract_app_seq_from_csv(input_data_file, t_size)
                training_seq = data_app_seq[0:t_size]
                test_seq = data_app_seq[t_size:(t_size+test_dataset_size)]
                
                uniq_app_seq = deepcopy(list(set(data_app_seq)))
                uniq_app_seq.sort()
                num_uniq_app = len(uniq_app_seq)
                
                data_num_seq = deepcopy(list(data_app_seq))
                
                for i in range(0, len(data_num_seq)):
                    app = data_num_seq[i]
                    data_num_seq[i] = uniq_app_seq.index(app)
                
                training_num_seq = deepcopy(list(data_num_seq[0:t_size]))
                test_num_seq = deepcopy(list(data_num_seq[t_size:(t_size+test_dataset_size)]))
                #print test_num_seq
                default_index = num_uniq_app
                check_if_new_row = [0 for x in xrange(num_uniq_app)]
                state_table = [[0 for x in xrange(num_uniq_app)] for x in xrange((num_uniq_app + 1))]
                #print num_uniq_app
                #print state_table
                
                """ For first input from training seqence """
                app = training_num_seq[0]
                check_if_new_row[app] = 1
                state_table[default_index][app] = 1
                
                #print state_table
                
                for app_i in range(1, len(training_num_seq)):
                    prev_app = training_num_seq[(app_i - 1)]
                    app = training_num_seq[app_i]
                    is_new_row = False
                    
                    if check_if_new_row[app] == 0:
                        check_if_new_row[app] = 1
                        is_new_row = True
                
                    #print str(prev_app) + " " + str(app) + " " + str(default_index)  
                    
                    if is_new_row == False:
                        ''' update the default row '''
                        state_table = list(update_row(state_table, default_index, app, alpha_IPAM))
                                   
                        ''' update the prev_app row '''
                        state_table = list(update_row(state_table, prev_app, app, alpha_IPAM))
                        
                    else:
                        ''' update the default row '''
                        state_table = list(update_row(state_table, default_index, app, alpha_IPAM))
                                   
                        ''' update the prev_app row '''
                        state_table = list(update_row(state_table, prev_app, app, alpha_IPAM))
                        #print "Happens Default Copy"
                        state_table[app] = deepcopy(list(state_table[default_index]))
                        #print state_table[app]
                        
                    #print state_table
                
                #print "test 1111 "
                #print state_table[0]
                #test = state_table[0]
                #print test       
                
                ''' Prediction '''
                for next_app_i in range(0, len(test_num_seq)):
                    #top = [-1, -1, -1, -1]
                    top = numpy.zeros(topN+1)
                    
                    if next_app_i == 0:
                        prev_app = training_num_seq[(t_size - 1)]
                    else:
                        prev_app = test_num_seq[(next_app_i - 1)]
                        
                    next_app = test_num_seq[next_app_i]
                    #print prev_app
                    row_prev_app = deepcopy(state_table[prev_app])
                    row_default = deepcopy(state_table[default_index])
                    #print "test: "
                    #print row_prev_app
                    #if prev_app == 0:
                        #print row_prev_app
                    #print state_table[prev_app]
                    row_prev_app_sorted = deepcopy(row_prev_app)
                    #row_prev_app_sorted.sort(reverse=True)
                    row_prev_app_sorted = sorted(row_prev_app_sorted, reverse=True)
                    
                    row_default_sorted = deepcopy(row_default)
                    #row_default_sorted.sort(reverse=True)
                    row_default_sorted = sorted(row_default_sorted, reverse=True)
                    #print row_prev_app_sorted
                    for j in xrange(0, topN):
                        top_prob = row_prev_app_sorted[j]
                        #print top_prob
                        
                        if top_prob > 0:
                            top[j] = row_prev_app.index(row_prev_app_sorted[j])
                        else:
                            for d_i in range(0, len(row_default_sorted)):
                                predicted_app = row_default.index(row_default_sorted[d_i])
                                
                                if predicted_app not in top:
                                    top[j] = predicted_app
                                    break
                    
                    if rm_query_in_predicted_apps == True:
                        try:
                            top.remove(prev_app)
                        except ValueError:
                            pass
                    
                    for t in range(0, topN):
                        if top[t] == next_app:
                            for k in range(t, topN):
                                top_accuracy[k] = top_accuracy[k] + 1
                            break
                        
                    #print top
                    #print next_app
                    
                    is_new_row = False
                    
                    if check_if_new_row[next_app] == 0:
                        check_if_new_row[next_app] = 1
                        is_new_row = True
                
                    if is_new_row == False:
                        
                        ''' update the default row '''
                        state_table = list(update_row(state_table, default_index, next_app, alpha_IPAM))
                                   
                        ''' update the prev_app row '''
                        state_table = list(update_row(state_table, prev_app, next_app, alpha_IPAM))
                        
                    else:
                        
                        ''' update the default row '''
                        state_table = list(update_row(state_table, default_index, next_app, alpha_IPAM))
                                   
                        ''' update the prev_app row '''
                        state_table = list(update_row(state_table, prev_app, next_app, alpha_IPAM))
                        
                        state_table[next_app] = list(state_table[default_index])
                        
                    #print state_table
            
                for t in xrange(0, topN):
                    test_results_accuracy[t][result_i] = float(top_accuracy[t]) / float(test_dataset_size)
                    
                result_i = result_i + 1
                
                #print float(top_accuracy[0]) / float(test_dataset_size)
                #print top_accuracy
        
        #print test_results_accuracy[2]
        
        
        for t in range(0, topN):
            means[t].append(numpy.mean(test_results_accuracy[t]))
            std[t].append(numpy.std(test_results_accuracy[t]))
            medians[t].append(numpy.median(test_results_accuracy[t]))
            
        
    return (means, std, medians)
                
