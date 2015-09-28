'''
Created on Jul 9, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''

import csv


'''
    Extract sequence data from input .csv file
'''
def extract_seq_from_csv(input_data_file):
    training_seq = []
    test_seq = []
    
    training_size = 0
    #test_size = 0
    row_num = -1
    
    with open(input_data_file, 'r') as csvfile:
        #is_first_row = True
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            row_num = row_num + 1
            
            if row_num == 0:
                training_size = int(r[0])
                #test_size = int(r[1])
                continue
            
            if row_num <= training_size:
                training_seq.append(r[0].replace(' ', '_'))
            else:
                test_seq.append(r[0].replace(' ', '_'))
    
    return (training_seq, test_seq)


