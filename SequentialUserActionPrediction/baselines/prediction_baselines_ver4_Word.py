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

input_data_file = "datasets/Word_filtered.csv"
input_folder = "outputs/train_test_sets_size_v6_Word/"
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



#user_black_list = ['M590', 'M068', 'M151', 'M553', 'M000', 'M883', 'M183', 'M927', 'M419', 'M272', 'M464', 'M270', 'M639', '21464']
user_black_list = ['M600', 'M421', 'M590', 'M068', 'M151', 'M553', 'M000', 'M883', 'M183', 'M927', 'M419', 'M272', 'M464', 'M270', 'M639', '21464']
#user_black_list = []
all_users = []

with open(input_data_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for r in reader:
        if r[0] == "USER-ID":
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
        #means_FxL_list[t].append(numpy.mean(means_FxL[t]))
        #print "Mean for Top " + str(t+1) + " = " + str(numpy.mean(means_FxL[t]))
        print "Mean for Top " + str(t+1) + " = " + str(means[t])
        print "STD for Top " + str(t+1) + " = " + str(std[t])
        print "Median for Top " + str(t+1) + " = " + str(medians[t])
    
    print "Done: FxL"
    
    
    print "Start: IPAM"
    (means, std, medians) = IPAM.run_IPAM(topN, input_test_data_folder, training_dataset_size, test_dataset_size, num_users, test_user_names, num_tests, alpha_IPAM, sample_input_file, experiment_type, rm_query_in_predicted_apps)
    
    for t in range(0, topN):
        #means_IPAM_list[t].append(numpy.mean(means_IPAM[t]))
        #print "Mean for Top " + str(t+1) + " = " + str(numpy.mean(means_IPAM[t]))
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



'''
{'M375': 3, 'M118': 0, 'M937': 6, 'M926': 5, 'M974': 7, 'M300': 2, 'M707': 4, 'M242': 1}


Num of training days = 100
Start: IPAM
Mean for Top 1 = [0.45525000000000004]
STD for Top 1 = [0.15940494816661119]
Median for Top 1 = [0.435]
Mean for Top 2 = [0.58474999999999999]
STD for Top 2 = [0.14739381771295568]
Median for Top 2 = [0.60499999999999998]
Mean for Top 3 = [0.66249999999999998]
STD for Top 3 = [0.13374883177059904]
Median for Top 3 = [0.68000000000000005]
Done: IPAM
Start: FxL
Mean for Top 1 = [0.45150000000000007]
STD for Top 1 = [0.1602739841646173]
Median for Top 1 = [0.45000000000000001]
Mean for Top 2 = [0.58625000000000005]
STD for Top 2 = [0.15128925110529168]
Median for Top 2 = [0.59999999999999998]
Mean for Top 3 = [0.65524999999999989]
STD for Top 3 = [0.13980320990592454]
Median for Top 3 = [0.65000000000000002]
Done: FxL


Num of training days = 500
Start: IPAM
Mean for Top 1 = [0.47074999999999995]
STD for Top 1 = [0.15948961564942088]
Median for Top 1 = [0.46000000000000002]
Mean for Top 2 = [0.59849999999999992]
STD for Top 2 = [0.14074000852636043]
Median for Top 2 = [0.60499999999999998]
Mean for Top 3 = [0.67025000000000001]
STD for Top 3 = [0.12528941495593313]
Median for Top 3 = [0.67999999999999994]
Done: IPAM
Start: FxL
Mean for Top 1 = [0.47625000000000001]
STD for Top 1 = [0.15486586938379937]
Median for Top 1 = [0.47999999999999998]
Mean for Top 2 = [0.61624999999999996]
STD for Top 2 = [0.14313782693613872]
Median for Top 2 = [0.63]
Mean for Top 3 = [0.6805000000000001]
STD for Top 3 = [0.13540587136457563]
Median for Top 3 = [0.67500000000000004]
Done: FxL


Num of training days = 1000
Start: IPAM
Mean for Top 1 = [0.47375000000000006]
STD for Top 1 = [0.15602383631996747]
Median for Top 1 = [0.46499999999999997]
Mean for Top 2 = [0.60075000000000001]
STD for Top 2 = [0.13894940625997651]
Median for Top 2 = [0.62]
Mean for Top 3 = [0.67175000000000007]
STD for Top 3 = [0.12819687008659766]
Median for Top 3 = [0.68500000000000005]
Done: IPAM
Start: FxL
Mean for Top 1 = [0.47599999999999998]
STD for Top 1 = [0.14752626884728021]
Median for Top 1 = [0.46499999999999997]
Mean for Top 2 = [0.61899999999999999]
STD for Top 2 = [0.13542156401400776]
Median for Top 2 = [0.625]
Mean for Top 3 = [0.6925]
STD for Top 3 = [0.12299898373563906]
Median for Top 3 = [0.69499999999999995]
Done: FxL


Num of training days = 1500
Start: IPAM
Mean for Top 1 = [0.47424999999999995]
STD for Top 1 = [0.15570625388853204]
Median for Top 1 = [0.46499999999999997]
Mean for Top 2 = [0.60050000000000003]
STD for Top 2 = [0.14040922334376754]
Median for Top 2 = [0.62]
Mean for Top 3 = [0.67074999999999996]
STD for Top 3 = [0.12834304616924128]
Median for Top 3 = [0.68500000000000005]
Done: IPAM
Start: FxL
Mean for Top 1 = [0.47949999999999998]
STD for Top 1 = [0.14470573589184363]
Median for Top 1 = [0.46000000000000002]
Mean for Top 2 = [0.61124999999999996]
STD for Top 2 = [0.13285683083680719]
Median for Top 2 = [0.60499999999999998]
Mean for Top 3 = [0.68900000000000006]
STD for Top 3 = [0.11867602959317437]
Median for Top 3 = [0.68500000000000005]
Done: FxL


Num of training days = 2000
Start: IPAM
Mean for Top 1 = [0.47424999999999995]
STD for Top 1 = [0.15515939385032415]
Median for Top 1 = [0.46499999999999997]
Mean for Top 2 = [0.60049999999999992]
STD for Top 2 = [0.14007051795435041]
Median for Top 2 = [0.62]
Mean for Top 3 = [0.67074999999999996]
STD for Top 3 = [0.12942927605453103]
Median for Top 3 = [0.68500000000000005]
Done: IPAM
Start: FxL
Mean for Top 1 = [0.48250000000000004]
STD for Top 1 = [0.14145228877610994]
Median for Top 1 = [0.46000000000000002]
Mean for Top 2 = [0.61499999999999999]
STD for Top 2 = [0.12911235417263522]
Median for Top 2 = [0.61499999999999999]
Mean for Top 3 = [0.6875]
STD for Top 3 = [0.1192843242006258]
Median for Top 3 = [0.67000000000000004]
Done: FxL
90.024926
'''



"""
RNN_top1_res = [0.2836, 0.3252, 0.3522, 0.3698]
RNN_top2_res = [0.3736, 0.4508, 0.4682, 0.5012]
RNN_top3_res = [0.4432, 0.5216, 0.5476, 0.5776]

                
means_RNN_list.append(RNN_top1_res)
means_RNN_list.append(RNN_top2_res)
means_RNN_list.append(RNN_top3_res)

'''
> std_matrix
          [,1]      [,2]      [,3]      [,4]
[1,] 0.1449949 0.1316185 0.1228453 0.1227656
[2,] 0.1680836 0.1503036 0.1399663 0.1213805
[3,] 0.1818099 0.1510016 0.1521084 0.1317010
'''

HMM_top1_res = [0.1660, 0.1526, 0.1607974, 0.1642]
HMM_top2_res = [0.2722, 0.2986, 0.2915950, 0.3214]
HMM_top3_res = [0.3926, 0.4062, 0.4209934, 0.4260]


means_HMM_list.append(HMM_top1_res)
means_HMM_list.append(HMM_top2_res)
means_HMM_list.append(HMM_top3_res)

'''
> std_matrix
          [,1]      [,2]      [,3]      [,4]
[1,] 0.1556291 0.1300363 0.1242263 0.1294902
[2,] 0.1837399 0.1664394 0.1526830 0.1571690
[3,] 0.1876907 0.1763911 0.1648568 0.1580235
'''

#IPAM
#alpha = 0.8
means_IPAM_list = [[0.41479999999999995, 0.433, 0.43760000000000004, 0.43679999999999991], [0.54239999999999999, 0.55679999999999996, 0.56179999999999997, 0.56259999999999999], [0.62939999999999985, 0.64480000000000004, 0.64680000000000004, 0.6462]]
#FxL
#k = 4
means_FxL_list = [[0.41619999999999996, 0.43080000000000007, 0.44040000000000001, 0.44259999999999988], [0.53160000000000007, 0.55359999999999998, 0.56840000000000002, 0.57999999999999996], [0.60199999999999998, 0.629, 0.64100000000000013, 0.65160000000000007]]
#FSFxL
#num_distinct_items = 4, FS_mode = "weight_freq_prob_neighbor", FS_update_mode = "IPAM", alpha_FS = 0.8, depth = 4, w_FS = 0.4, w_FxL = 0.6
means_FSFxL_list = [[0.43019999999999997, 0.44379999999999997, 0.45160000000000011, 0.45340000000000003], [0.55419999999999991, 0.57220000000000004, 0.57959999999999989, 0.58499999999999996], [0.63840000000000008, 0.66199999999999992, 0.66720000000000002, 0.67579999999999996]]
#Null Model
means_Null_list = [[0.253, 0.253, 0.253, 0.253], [0.43119999999999997, 0.43119999999999997, 0.43119999999999997, 0.43119999999999997], [0.54380000000000006, 0.54380000000000006, 0.54380000000000006, 0.54380000000000006]]





#print "FS"
#print means_FS_list

print "IPAM"
print means_IPAM_list

print "FxL"
print means_FxL_list

print "FSFxL"
print means_FSFxL_list

print "Null Model"
print means_Null_list




plt.figure(1)
#plt.plot(training_dataset_size, f(training_dataset_size), 'bo', means_top1, f(means_top1), 'k')
#plt.plot(training_dataset_size, means_top1, 'bo')
#plt.plot(training_dataset_size, means_GBP[0], 'bo', training_dataset_size, means_GBP[0], 'k--')
plt.xlabel('Training days')
plt.ylabel('Prediction accuracy')
#GBP, = plt.plot(training_dataset_size, means_GBP[0], 'bo', training_dataset_size, means_GBP[0], 'k--')
#IPAM, = plt.plot(training_dataset_size, means_IPAM[0], 'go', training_dataset_size, means_IPAM[0], 'r--')
#plt.plot(training_dataset_days, means_GBP_list[0], 'bs')
#GBP, = plt.plot(training_dataset_days, means_GBP_list[0], '>y--')
FSFxL, = plt.plot(training_dataset_days, means_FSFxL_list[0], 'sr--')
#plt.plot(training_dataset_days, means_IPAM_list[0], 'go')
IPAM, = plt.plot(training_dataset_days, means_IPAM_list[0], 'og--')
#plt.plot(training_dataset_days, means_FxL_list[0], 'k^')
FxL, = plt.plot(training_dataset_days, means_FxL_list[0], '^k--')
RNN, = plt.plot(training_dataset_days, means_RNN_list[0], '*b--')
HMM, = plt.plot(training_dataset_days, means_HMM_list[0], '+k--')
Null, = plt.plot(training_dataset_days, means_Null_list[0], '>k--')
#plt.plot(training_dataset_size, means_IPAMComm[0], 'ko')
#IPAMComm, = plt.plot(training_dataset_size, means_IPAMComm[0], 'k--')
#plt.axis([1, 10, 0, 0.50])
plt.title(title + str('Top 1'))
#plt.legend([FS, IPAM, FxL, RNN, HMM, GBP], ["FS", "IPAM", "FxL", "RNN", "HMM", "GBSP"], loc=4)
plt.legend([FSFxL, FxL, IPAM, RNN, HMM, Null], ["FSFxL", "FxL", "IPAM", "RNN", "HMM", "Null Model"], loc=4)
#plt.legend([GBP, IPAM, FxL, RNN, HMM], ["GBSP", "IPAM", "FxL", "RNN", "HMM"], loc=4)#, bbox_to_anchor=(0.5,-0.1))
#plt.legend([GBP, (GBP, IPAM, FxL)], ["GBP", "IPAM", "FxL"])
#plt.legend([GBP, (GBP, IPAM)], ["GBP", "IPAM", "IPAMComm"])

#fig.savefig('samplefigure', bbox_extra_artists=(lgd,), bbox_inches='tight')

plt.figure(2)
#plt.plot(training_dataset_size, f(training_dataset_size), 'bo', means_top2, f(means_top2), 'k')
#plt.plot(training_dataset_size, means_GBP[1], 'bo', training_dataset_size, means_GBP[1], 'k--')
plt.xlabel('Training days')
plt.ylabel('Prediction accuracy')
#GBP, = plt.plot(training_dataset_size, means_GBP[1], 'bo', training_dataset_size, means_GBP[1], 'k--')
#IPAM, = plt.plot(training_dataset_size, means_IPAM[1], 'go', training_dataset_size, means_IPAM[1], 'r--')
#plt.plot(training_dataset_days, means_GBP_list[1], 'bs')
#GBP, = plt.plot(training_dataset_days, means_GBP_list[1], '>y--')
FSFxL, = plt.plot(training_dataset_days, means_FSFxL_list[1], 'sr--')
#plt.plot(training_dataset_days, means_IPAM_list[1], 'go')
IPAM, = plt.plot(training_dataset_days, means_IPAM_list[1], 'og--')
#plt.plot(training_dataset_days, means_FxL_list[1], 'k^')
FxL, = plt.plot(training_dataset_days, means_FxL_list[1], '^k--')
RNN, = plt.plot(training_dataset_days, means_RNN_list[1], '*b--')
HMM, = plt.plot(training_dataset_days, means_HMM_list[1], '+k--')
Null, = plt.plot(training_dataset_days, means_Null_list[1], '>k--')
#plt.plot(training_dataset_size, means_IPAMComm[1], 'ko')
#IPAMComm, = plt.plot(training_dataset_size, means_IPAMComm[1], 'k--')
#plt.axis([1, 10, 0.10, 0.60])
plt.title(title + str('Top 2'))
#plt.legend([FS, IPAM, FxL, RNN, HMM, GBP], ["FS", "IPAM", "FxL", "RNN", "HMM", "GBSP"], loc=4)
plt.legend([FSFxL, FxL, IPAM, RNN, HMM, Null], ["FSFxL", "FxL", "IPAM", "RNN", "HMM", "Null Model"], loc=4)
#plt.legend([GBP, IPAM, FxL, RNN, HMM], ["GBSP", "IPAM", "FxL", "RNN", "HMM"], loc=4)# loc='center right')
#plt.legend([GBP, (GBP, IPAM, FxL)], ["GBP", "IPAM", "FxL"])
#plt.legend([GBP, (GBP, IPAM)], ["GBP", "IPAM", "IPAMComm"])

plt.figure(3)
#plt.plot(training_dataset_size, f(training_dataset_size), 'bo', means_top3, f(means_top3), 'k')
#plt.plot(training_dataset_size, means_GBP[2], 'bo', training_dataset_size, means_GBP[2], 'k--')
plt.xlabel('Training days')
plt.ylabel('Prediction accuracy')
#GBP, = plt.plot(training_dataset_size, means_GBP[2], 'bo', training_dataset_size, means_GBP[2], 'k--')
#IPAM, = plt.plot(training_dataset_size, means_IPAM[2], 'go', training_dataset_size, means_IPAM[2], 'r--')
#plt.plot(training_dataset_days, means_GBP_list[2], 'bs')
#GBP, = plt.plot(training_dataset_days, means_GBP_list[2], '>y--')
FSFxL, = plt.plot(training_dataset_days, means_FSFxL_list[2], 'sr--')
#plt.plot(training_dataset_days, means_IPAM_list[2], 'go')
IPAM, = plt.plot(training_dataset_days, means_IPAM_list[2], 'og--')
#plt.plot(training_dataset_days, means_FxL_list[2], 'k^')
FxL, = plt.plot(training_dataset_days, means_FxL_list[2], '^k--')
RNN, = plt.plot(training_dataset_days, means_RNN_list[2], '*b--')
HMM, = plt.plot(training_dataset_days, means_HMM_list[2], '+k--')
Null, = plt.plot(training_dataset_days, means_Null_list[2], '>k--')
#plt.plot(training_dataset_size, means_IPAMComm[2], 'ko')
#IPAMComm, = plt.plot(training_dataset_size, means_IPAMComm[2], 'k--')
#plt.axis([0, 31, 0.50, 0.90])
plt.title(title + str('Top 3'))
plt.legend([FSFxL, FxL, IPAM, RNN, HMM, Null], ["FSFxL", "FxL", "IPAM", "RNN", "HMM", "Null Model"], loc=4)
#plt.legend([FS, IPAM, FxL, RNN, HMM, GBP], ["FS", "IPAM", "FxL", "RNN", "HMM", "GBSP"], loc=4)
#plt.legend([GBP, IPAM, FxL, RNN, HMM], ["GBSP", "IPAM", "FxL", "RNN", "HMM"], loc=4)# loc='center right')
#plt.legend([GBP, (GBP, IPAM, FxL)], ["GBP", "IPAM", "FxL"])
#plt.legend([GBP, (GBP, IPAM)], ["GBP", "IPAM", "IPAMComm"])
plt.show()
"""