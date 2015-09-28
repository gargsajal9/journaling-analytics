'''
Created on Jul 9, 2015

@author: Changsung Moon (csmoon2@ncsu.edu)
'''

import operator
import numpy
import math

from copy import deepcopy

from numpy import zeros, outer, exp, dot, random, uint32, isnan, sum as np_sum, float32 as REAL

from scipy.spatial import distance

from func import io
from func import Tree


from models import word2vec_fcbow
from gensim import utils, matutils  # utility fnc for pickling, common scipy operations etc




def prediction_fcbow(topN, model, t_size, context_names, test_sub_seq, cbow_mean, freq_tree, beta):
    top = []
    score_dict = {}
    freq_dict = {}
    sim_dict = {}
    context_vecs = []
    
    for name in context_names:
        if model.new_vocab_syn0.has_key(name) == False:
            context_vecs.append(model.syn0[model.vocab[name].index])
        else:
            context_vecs.append(model.new_vocab_syn0[name])
    

    
    all_actions_vocab = model.vocab

    j = -1

    while len(context_vecs) >= 1:
        
        j = j + 1
      
        if j > 0:
            del context_vecs[0]
            del test_sub_seq[0]
            
        if len(context_vecs) == 0:
            break
    
        
        #print test_sub_seq
        
        #l1 = np_sum(model.syn0[context_indices], axis=0) # 1 x layer1_size
        l1 = np_sum(context_vecs, axis=0) # 1 x layer1_size
        
        if context_vecs and cbow_mean:
            l1 /= len(context_vecs)



        new_actions = model.new_vocab_syn1.keys()
        
        for new_action in new_actions:
            if "LabCon_" in new_action:
                continue
            
            l2a = model.new_vocab_syn1[new_action]
            fa = 1. / (1. + exp(-dot(l1, l2a.T))) # propagate hidden -> output
            #dist = 1. - fa
            #dist = math.pow(dist, 2)
            #sim = 1. / (1. + dist)
            
            sim = fa
            
            score = 0
            
            freq = Tree.returnFreq(freq_tree, test_sub_seq, new_action)
            freq_log = 0
            
            if freq > 0:   
                freq_log = max(0, math.log(freq))
                #freq_log = sigmoid(freq_log)
                #freq_log = math.tanh(freq_log)
                
                if freq_log > 0:
                    if freq_dict.has_key(new_action):
                        freq_dict[new_action] += freq_log
                    else:
                        freq_dict[new_action] = freq_log

            if sim_dict.has_key(new_action):
                sim_dict[new_action] += max(0, sim)
            else:
                sim_dict[new_action] = max(0, sim)
                
                
        for action in all_actions_vocab:
            if "LabCon_" in action:
                continue
            
            
            action_obj = all_actions_vocab[action]
            #print action_obj
            
            l2a = deepcopy(model.syn1[action_obj.point]) # 2d matrix, codelen x layer1_size
            #l2a = deepcopy(model.syn1neg[action_obj.index]) # 2d matrix, codelen x layer1_size
            
            '''
            print "Size of syn1 = " + str(len(model.syn1))
            print "Length of vocab = " + str(len(model.vocab))
            print "index 89 = " + str(model.syn1[89])
            print action_obj.point
            print model.syn1
            #print l2a
            '''
            #print model.syn1
            
            
            u = dot(l1, l2a.T)
            #print u
            fa = 1. / (1. + exp(u)) # propagate hidden -> output
            #fa = 1. / (1. + exp(dot(l1, l2a.T))) # propagate hidden -> output
            #ga = (1. - action_obj.code - fa)
            #ga = (action_obj.code - fa)
            
            
            dist = distance.sqeuclidean(action_obj.code, fa)
            #dist = distance.euclidean(action_obj.code, fa)
            
            #dist = numpy.sum(ga)
            #dist = numpy.abs(dist)
            #print dist
            sim = 1. / (1. + dist)
            
            

            freq = Tree.returnFreq(freq_tree, test_sub_seq, action)
            freq_log = 0

            if freq > 0:

                freq_log = max(0, math.log(freq))
               
                if freq_log > 0:
                #if freq > 1:
                    if freq_dict.has_key(action):
                        freq_dict[action] += freq_log
                    else:
                        freq_dict[action] = freq_log
                
                
            if sim_dict.has_key(action):
                sim_dict[action] += max(0, sim)
            else:
                sim_dict[action] = max(0, sim)
      
                   
    total_sum_freq = numpy.sum(freq_dict.values())    
    total_sum_sim = numpy.sum(sim_dict.values())  
    
    
    
    for f_i in freq_dict:
        if total_sum_freq != 0:
            freq_dict[f_i] = freq_dict[f_i] / float(total_sum_freq)
    
    for s_i in sim_dict:
        if total_sum_sim != 0:
            sim_dict[s_i] = sim_dict[s_i] / float(total_sum_sim)

    
    for action in sim_dict:
        if freq_dict.has_key(action):
            score_dict[action] = (beta * freq_dict[action]) + ((1.0 - beta) * sim_dict[action])
        else:
            score_dict[action] = (1.0 - beta) * sim_dict[action]
        

    sorted_score_list = sorted(score_dict.items(), key=operator.itemgetter(1))
    sorted_score_list.reverse()
    
    freq_dict = sorted(freq_dict.items(), key=operator.itemgetter(1))
    freq_dict.reverse()
    
    sim_dict = sorted(sim_dict.items(), key=operator.itemgetter(1))
    sim_dict.reverse()
    
    #print freq_dict
    #print sim_dict
    #print "\n"
    
    '''
    print freq_dict
    print sim_dict
    #print "\n"
    print sorted_score_list
    print "\n"
    '''
    
    
    for i in range(0, topN):
        top.append(sorted_score_list[i][0])
    

    return (top, sorted_score_list)




def update_fcbow_model(model, next_action, context_names, alpha, cbow_mean, weight_sum=False):
    #next_action_obj = model.vocab[next_action]
    new_actions = model.new_vocab_syn1.keys()
    #all_actions_vocab = model.vocab
    
    context_vecs = []
    
    for name in context_names:
        if model.new_vocab_syn0.has_key(name) == False:
            context_vecs.append(model.syn0[model.vocab[name].index])
        else:
            context_vecs.append(model.new_vocab_syn0[name])
    
    #print next_action
    #print new_actions
    
    is_next_action_new = False
    
    #if next_action not in all_actions_vocab:
    if next_action in new_actions:
        is_next_action_new = True

    
    if is_next_action_new == False:
        next_action_obj = model.vocab[next_action]
    else:
        next_action_vec = model.new_vocab_syn1[next_action]
    
    
    if len(context_vecs) >= 1:
        #while sim < 0.5:
        #for i in range(0, 2):
        #print sim
        

        l1 = np_sum(context_vecs, axis=0) # 1 x layer1_size
        #l1 = np_sum(model.syn0[context_indices], axis=0) # 1 x layer1_size
        
        if context_vecs and cbow_mean:
            l1 /= len(context_vecs)
          
        neu1e = zeros(l1.shape)
        
        if is_next_action_new == False:    
            l2a = deepcopy(model.syn1[next_action_obj.point]) # 2d matrix, codelen x layer1_size
            fa = 1. / (1. + exp(-dot(l1, l2a.T))) # propagate hidden -> output
            ga = (1. - next_action_obj.code - fa) * alpha # vector of error gradients multiplied by the learning rate
            #ga = (next_action_obj.code - fa) * alpha # vector of error gradients multiplied by the learning rate
            #ga = (fa - next_action_obj.code) * alpha # vector of error gradients multiplied by the learning rate
            
            neu1e = zeros(l1.shape)
            model.syn1[next_action_obj.point] += outer(ga, l1) # learn hidden -> output
            #model.syn1[next_action_obj.point] -= outer(ga, l1) # learn hidden -> output
        
            neu1e += dot(ga, l2a) # save error
        else:
            fa = 1. / (1. + exp(-dot(l1, next_action_vec.T))) # propagate hidden -> output
            ga = (1. - fa) * alpha # vector of error gradients multiplied by the learning rate
            #print fa
            #print ga
            #print "type of next_action_vec = " + str(type(next_action_vec))
            #print next_action_vec.shape
            error = outer(ga, l1)
            #print error
            #print next_action_vec
            next_action_vec += error[0] # learn hidden -> output
            #next_action_vec += outer(ga, l1) # learn hidden -> output
            #print next_action_vec
            #print "\n"
            model.new_vocab_syn1[next_action] = next_action_vec
            neu1e += dot(ga, next_action_vec) # save error
        
        for name in context_names:
            if model.new_vocab_syn0.has_key(name) == False:
                model.syn0[model.vocab[name].index] += neu1e # learn input -> hidden, here for all words in the window separately
            else:
                model.new_vocab_syn0[name] += neu1e
                
        #model.syn0[context_indices] += neu1e # learn input -> hidden, here for all words in the window separately
        
     
    
    return model




def init_model(seq_list, num_features, min_word_count, num_workers, context, downsampling, cbow_mean, context_labeling, alpha_training):
    
    # Initialize and train the model (this will take some time)
    #print "Initiating model..."
    #model = word2vec_seq_modified_labeled.Word2Vec(seq_list, workers=num_workers, size=num_features, min_count = min_word_count, window = context, sample = downsampling, sg=algo, cbow_mean = cbow_mean)
    model = word2vec_fcbow.Word2Vec(seq_list, alpha=alpha_training, workers=num_workers, size=num_features, min_count = min_word_count, window = context, sample = downsampling, sg=0, cbow_mean = cbow_mean, context_labeling = context_labeling)

    return model



def test_model(topN, model, test_seq, last_action, t_size, context_window, alpha, beta, update_model, cbow_mean, freq_tree, update_one_time):
    all_actions_vocab = model.vocab
    
    top_accuracy = numpy.zeros(topN)
    
    current_action = last_action
    #print model.vocab[current_action]
    
    #for pos, word in enumerate(test_seq):
        
        #print "pos = " + str(pos)
        #print "word = " + str(word)
        #print "word.point = " + str(word.point)
        #print "\n"
      
    #print "test_seq = " + str(test_seq)  
        
    for i in range(0, len(test_seq)):
        
        #print str(i) + " / " + str(len(test_seq))
        
        top = []
        next_action = test_seq[i]
        
        if i != 0:
            current_action = test_seq[i-1]

        #print "Current: " + current_action
        #current_vocab_obj = model.vocab[current_action]
        #print "current word index: " + str(current_vocab_obj.index)

        #DEL
        #context_indices = []
        context_names = []
        context_vecs = []
        test_sub_seq = [] 
        
        if i == 0:
            if model.context_labeling == True:
                labeled_last_action = "LabCon_" + str(last_action) + "_" + str(i)
                #DEL
                #context_indices.append(model.vocab[labeled_last_action].index)
                
                context_names.append(labeled_last_action)
                
                if model.new_vocab_syn0.has_key(labeled_last_action):
                    context_vecs.append(model.new_vocab_syn0[labeled_last_action])
                else:
                    context_vecs.append(model.syn0[model.vocab[labeled_last_action].index])
            else:
                #DEL
                #context_indices.append(model.vocab[last_action].index)
                
                context_names.append(last_action)
                
                if model.new_vocab_syn0.has_key(last_action):
                    context_vecs.append(model.new_vocab_syn0[last_action])
                else:
                    context_vecs.append(model.syn0[model.vocab[last_action].index])
            test_sub_seq.append(last_action)
        else:    
            for j in range(0, context_window):
                index = i - j - 1
                
                if index >= 0:
                    if model.context_labeling == True:
                        labeled_action = "LabCon_" + str(test_seq[index]) + "_" + str(j)
                        #DEL
                        #context_indices.append(model.vocab[labeled_action].index)
                    
                        context_names.append(labeled_action)
                        
                        if model.new_vocab_syn0.has_key(labeled_action):
                            context_vecs.append(model.new_vocab_syn0[labeled_action])
                        else:
                            context_vecs.append(model.syn0[model.vocab[labeled_action].index])
                    else:
                        #DEL
                        #context_indices.append(model.vocab[test_seq[index]].index)
                        
                        context_names.append(test_seq[index])
                        
                        if model.new_vocab_syn0.has_key(test_seq[index]):
                            context_vecs.append(model.new_vocab_syn0[test_seq[index]])
                        else:
                            context_vecs.append(model.syn0[model.vocab[test_seq[index]].index])
                    
                    test_sub_seq.append(test_seq[index])

        if i < context_window and i != 0:
            if model.context_labeling == True:
                labeled_last_action = "LabCon_" + str(last_action) + "_" + str(i)
                #DEL
                #context_indices.append(model.vocab[labeled_last_action].index)
                
                context_names.append(labeled_last_action)
                
                if model.new_vocab_syn0.has_key(labeled_last_action):
                    context_vecs.append(model.new_vocab_syn0[labeled_last_action])
                else:
                    context_vecs.append(model.syn0[model.vocab[labeled_last_action].index])
            else:
                #DEL
                #context_indices.append(model.vocab[last_action].index)
                
                context_names.append(last_action)
                
                if model.new_vocab_syn0.has_key(last_action):
                    context_vecs.append(model.new_vocab_syn0[last_action])
                else:
                    context_vecs.append(model.syn0[model.vocab[last_action].index])
                    
            test_sub_seq.append(last_action)  
        
        #DEL
        #context_indices.reverse()
        #context_indices_origin = deepcopy(context_indices)

        
        context_names.reverse()
        context_vecs.reverse()
        test_sub_seq.reverse()
        context_names_origin = deepcopy(context_names)
        context_vecs_origin = deepcopy(context_vecs)
        test_sub_seq_origin = deepcopy(test_sub_seq)
        
        #print freq_tree.get_ascii(attributes=["name", "dist"], show_internal=True)

        #print next_action
        (top, sorted_sim) = prediction_fcbow(topN, model, t_size, context_names, test_sub_seq, cbow_mean, freq_tree, beta)
        #(top, sorted_sim) = prediction_fcbow(topN, model, t_size, context_vecs, test_sub_seq, cbow_mean, freq_tree, beta)
        #print "Prediction Done"
        
        if next_action not in all_actions_vocab:
            #print "New action"
            if model.new_vocab_syn0.has_key(next_action) == False:
                if model.context_labeling == True:
                    for j in range(0, context_window):               
                        labeled_action = "LabCon_" + str(next_action) + "_" + str(j)
                        random.seed(uint32(model.hashfxn(labeled_action + str(model.seed))))
                        new_vec = (random.rand(model.layer1_size) - 0.5) / model.layer1_size
                        model.add_new_vocab_syn0(labeled_action, new_vec)
                        
                        new_vec = zeros((1, model.layer1_size), dtype=REAL)
                        model.add_new_vocab_syn1(labeled_action, new_vec)
                
                #l1 = np_sum(model.syn0[context_indices], axis=0)
                random.seed(uint32(model.hashfxn(next_action + str(model.seed))))
                new_vec = (random.rand(model.layer1_size) - 0.5) / model.layer1_size
                model.add_new_vocab_syn0(next_action, new_vec)
                
                new_vec = zeros((1, model.layer1_size), dtype=REAL)
                model.add_new_vocab_syn1(next_action, new_vec)
                #l1 = np_sum(context_vecs_origin, axis=0)
                #model.add_new_vocab(next_action, l1)
                    
                    
        if update_model == True:
            
            if update_one_time == False:
                context_names = []
                c_i = len(context_names_origin) - 1
                while len(context_names) < len(context_names_origin):
                    context_names.append(context_names_origin[c_i])
                    c_i = c_i - 1
                    model = update_fcbow_model(model, next_action, context_names, alpha, cbow_mean)
            else:
                model = update_fcbow_model(model, next_action, context_names_origin, alpha, cbow_mean)

            #model = update_cbow_model(model, next_action, context_indices_origin, alpha, cbow_mean)    
            freq_tree = Tree.updateTree(freq_tree, test_sub_seq_origin, next_action)
        #print "Update Done"
        
        for t in range(0, topN):
            if top[t] == next_action:
                for k in range(t, topN):
                    top_accuracy[k] = top_accuracy[k] + 1
                break
        
        
        '''
        print "Current: " + current_action
        print "Target: " + target_action
        print "Predict: " + str(predicted_action[0][0])
        print "\n"
        '''
  
    return top_accuracy


'''
    Train F-CBOW model and make predictions
'''
def run_model(topN, input_test_data_folder, training_dataset_size, test_user_names, num_tests, sample_input_file, num_features, min_word_count, num_workers, context, downsampling, alpha_training, alpha_test, beta, cbow_mean, update_model, tree_weight_gap, context_labeling, build_vocab_total, num_validation_set=0, update_one_time=False):
    is_sample_test = False
    
    if sample_input_file != "":
        is_sample_test = True
    
    means = []      # Accuracies
    std = []        # Standard Deviations
    medians = []    # Medians
    
    num_users = len(test_user_names)
    
    for i in range(0, topN):
        means.append([])
        std.append([])
        medians.append([])
    
    for t_size in training_dataset_size:
        folder_size = t_size
        # Array to store accuracy results
        test_results_accuracy = [[0 for x in xrange((num_tests*num_users))] for x in xrange(topN)]
        result_i = 0
        
        for user in test_user_names:
            for test_i in range(1, (num_tests+1)):
                # Array for top N accuracies
                top_accuracy = numpy.zeros(topN)
                
                if is_sample_test == True:
                    input_data_file = sample_input_file
                else:
                    input_data_file = input_test_data_folder + str(folder_size) + "/" + str(user) + "-" + str(test_i) + ".csv"
                    
                    
                training_seq_list = []
                test_seq_list = []
                total_seq_list = []
                
                # Extract training and test sequence data
                (training_seq, test_seq) = io.extract_seq_from_csv(input_data_file)
                
                # If larger than 0, validation set will be extracted from training data and run validation
                if num_validation_set > 0:
                    test_seq = training_seq[(t_size - num_validation_set) : t_size]
                    training_seq = training_seq[0 : (t_size - num_validation_set)]
    
                training_seq_list.append(training_seq)
                test_seq_list.append(test_seq)
                
                total_seq_list.append(training_seq)
                total_seq_list.append(test_seq)
                
                num_training_seq = len(training_seq)
                num_test_seq = len(test_seq)
                
                
                # Initiate a model
                model = init_model(training_seq_list, num_features, min_word_count, num_workers, context, downsampling, cbow_mean, context_labeling, alpha_training)
                
                if context_labeling == True:
                    labeled_actions = []
                    
                    #if build_vocab_total == True:
                    #    set_action = list(set(total_seq_list[0]))
                    #else:
                    set_action = list(set(training_seq))
                        
                    for a in set_action:
                        for label in range(context):
                            labeled_a = "LabCon_" + str(a) + "_" + str(label)
                            labeled_actions.append(labeled_a)
                      
                    if build_vocab_total == True:      
                        set_action = list(set(total_seq_list[1]))
                        
                        for a in set_action:
                            for label in range(context):
                                labeled_a = "LabCon_" + str(a) + "_" + str(label)
                                #if labeled_a not in labeled_actions:
                                labeled_actions.append(labeled_a)
                    
                        total_seq_list.append(labeled_actions)
                    else:
                        training_seq_list.append(labeled_actions)
                    
                
                
                # Build CBOW vocabulary
                if build_vocab_total == True:
                    # Build vocabulary with training and test datasets
                    model.build_vocab(total_seq_list)
                else:
                    # Build vocabulary with training dataset
                    model.build_vocab(training_seq_list)

                #print len(model.vocab)
                #model.reset_weights()
                
  
                # Train a model
                model.train([training_seq])
                
                indices_nan = isnan(model.syn0)
                model.syn0[indices_nan] = 0.0
                
                indices_nan = isnan(model.syn1)
                model.syn1[indices_nan] = 0.0
                
                #print model.syn1
                
                # Build initial Trie to store frequencies of patterns
                freq_tree = Tree.buildFreqTree(training_seq, context)
                #print freq_tree.get_ascii(show_internal=True)
                
                # If you don't plan to train the model any further, calling 
                # init_sims will make the model much more memory-efficient.
                #model.init_sims(replace=True)
                #model.save(model_name)
                
                # Run predictions with the model
                top_accuracy = test_model(topN, model, test_seq, training_seq[num_training_seq-1], t_size, context, alpha_test, beta, update_model, cbow_mean, freq_tree, update_one_time)
                
                #print "TEST done"
                
                model.init_sims(replace=True)
                
                #print "INIT done"
                
                for t in xrange(0, topN):
                    test_results_accuracy[t][result_i] = float(top_accuracy[t]) / float(num_test_seq)
                        
                result_i = result_i + 1   
        
            #print "user = " + str(user) + " DONE"
            #print test_results_accuracy
            
        for t in range(0, topN):
            means[t].append(numpy.mean(test_results_accuracy[t]))
            std[t].append(numpy.std(test_results_accuracy[t]))
            medians[t].append(numpy.median(test_results_accuracy[t]))
            
        
    return (means, std, medians)         




