'''
Created on Mar 15, 2015

@author: Changsung Moon
'''

import csv
import numpy
import heapq
from copy import deepcopy
from functions import functions_SP
from functions import Tree


def run_FxL(topN, input_test_data_folder, training_dataset_size, test_dataset_size, num_users, test_user_names, num_tests, FxL_k, sample_input_file, experiment_type, rm_query_in_predicted_apps, FxL_use_prev_prob):
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
                
                '''
                data_num_seq = deepcopy(data_item_seq)
                
                for i in range(0, len(data_num_seq)):
                    item = data_num_seq[i]
                    data_num_seq[i] = uniq_item_seq.index(item)
                
                training_num_seq = deepcopy(data_num_seq[0:t_size])
                test_num_seq = deepcopy(data_num_seq[t_size:(t_size+test_dataset_size)])
                '''
                
                ''' Build initial FxL Tree '''
                freq_tree = Tree.buildFreqTree(training_seq, FxL_k)
                
                #print tree_action_dic
                #print tree_freq_dic

                ''' Prediction '''
                
                for next_item_i in range(0, len(test_seq)):  
                    
                    #top = [-1, -1, -1, -1]
                    
                    if next_item_i == 0:
                        prev_item = training_seq[(t_size - 1)]
                    else:
                        prev_item = test_seq[(next_item_i - 1)]
                        
                    next_item = test_seq[next_item_i]
                    
                    ''' For FxL scores and probabilities calculations '''
                    score_list = [0 for x in xrange(num_uniq_item)]
                    score_list_prob = [0 for x in xrange(num_uniq_item)]
                    sub_seq = []
                    
                    if next_item_i == 0:
                        sub_seq.append(training_seq[(t_size-1)])
                    else:
                        s_i = next_item_i - FxL_k + 1
                        
                        if s_i < 0:
                            s_i = 0
                            
                        sub_seq = deepcopy(test_seq[s_i:next_item_i])
                        
                    #for uniq_item in uniq_item_seq:
                    for score_i in range(0, len(score_list)):
                        target = uniq_item_seq[score_i]
                        score = Tree.calScore(freq_tree, sub_seq, target)
                        score_list[score_i] = score
                        
                    sum_scores = numpy.sum(score_list)
                    if sum_scores != 0:
                        for s in range(0, len(score_list)):
                            score_list_prob[s] = float(score_list[s]) / sum_scores
                          
                    
                    ''' Prediction '''
       
                    top = []
                    
                    while len(top) < topN+1:
                        max_value = numpy.max(score_list_prob)
                        max_i = score_list_prob.index(max_value)
                        score_list_prob[max_i] = -1
                        p = uniq_item_seq[max_i]
                        
                        if p not in top:
                            top.append(p)
                            
                        if len(top) > 2:
                            break
                    
                    if rm_query_in_predicted_apps == True:
                        try:
                            top.remove(prev_item)
                        except ValueError:
                            pass
                    
                    #print "top = " + str(top)
                    #print next_item
                    
                    for t in range(0, topN):
                        if top[t] == next_item:
                            for k in range(t, topN):
                                top_accuracy[k] = top_accuracy[k] + 1
                            break
                        
                    
                    ''' Update FxL Tree '''
                    freq_tree = Tree.updateTree(freq_tree, sub_seq, next_item)
                        
                        
                    '''
                    print "\n"
                    print "query_app: " + str(prev_item) + ", next_app: " + str(next_item)
                    print top
                    print score_list
                    print prob_list
                    '''
                for t in xrange(0, topN):
                    test_results_accuracy[t][result_i] = float(top_accuracy[t]) / float(test_dataset_size)
                
                #print test_results_accuracy    
                
                result_i = result_i + 1
                
                #print float(top_accuracy[0]) / float(test_dataset_size)
        
            
        for t in range(0, topN):
            means[t].append(numpy.mean(test_results_accuracy[t]))
            std[t].append(numpy.std(test_results_accuracy[t]))
            medians[t].append(numpy.median(test_results_accuracy[t]))
            
                
    #return (means_list, std_list)
    return (means, std, medians)


