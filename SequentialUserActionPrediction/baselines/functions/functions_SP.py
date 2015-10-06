'''
Created on Jan 10, 2015

@author: Changsung Moon
'''

import csv
import datetime


def extract_uniq_app_list(input_data_file, test_users):
    data_all_uniq_app = []
    
    with open(input_data_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if r[1] == "AppName":
                continue
            
            if test_users.has_key(r[0]):
                if str(r[1]).find('Safari (') > -1:
                    r[1] = "Safari"
                elif str(r[1]).find('Google Chrome (') > -1:
                    r[1] = "Google Chrome"
                elif str(r[1]).find('HP LaserJet 500 colorMFP M570d') > -1:
                    r[1] = "HP LaserJet 500 colorMFP M570d"
                elif str(r[1]).find('Photosmart Premium C309g-m') > -1:    
                    r[1] = "Photosmart Premium C309g-m"
                
                data_all_uniq_app.append(r[1])
    
    data_all_uniq_app = list(set(data_all_uniq_app))
    data_all_uniq_app.sort()
  
    return data_all_uniq_app


'''
Extract distinct application names and their label into a list
'''
def extract_app_label(input_applist_file):
    data_app_label = {}
    
    with open(input_applist_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if r[0] == "AppName":
                continue
            
            data_app_label[r[0]] = r[1]
    
    return data_app_label

'''
Extract application sequence only for user labels and timestamps
'''
def extract_userapp_seq(input_data_file, data_app_label, test_users):
    data_all_userapp_seq_list = []
    data_all_timestamp_seq_list = []
    for i in range(0, len(test_users)):
        data_all_userapp_seq_list.append([])
        data_all_timestamp_seq_list.append([])
        
    with open(input_data_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if r[1] == "AppName":
                continue
            
            if test_users.has_key(r[0]):
                user_num = test_users[r[0]]
                
                """ Remove web domain values of web browsers like Safari (www.google.com) -> Safari """
                if str(r[1]).find('Safari (') > -1:
                    r[1] = "Safari"
                elif str(r[1]).find('Google Chrome (') > -1:
                    r[1] = "Google Chrome"
                elif str(r[1]).find('HP LaserJet 500 colorMFP M570d') > -1:
                    r[1] = "HP LaserJet 500 colorMFP M570d"
                elif str(r[1]).find('Photosmart Premium C309g-m') > -1:    
                    r[1] = "Photosmart Premium C309g-m"

                """
                if r[1] not in data_app_label:
                    print str(r[1]) + " is not in the labeled list"
                    continue
                """
                
                """ Extract only user labeled applications AND Change the timestamp format from POSIX to human readable """    
                if data_app_label[r[1]] == "user":
                    l = len(data_all_userapp_seq_list[user_num])
                    if l > 0:
                        last_app = data_all_userapp_seq_list[user_num][l-1]
                        
                        if last_app != r[1]:
                            data_all_userapp_seq_list[user_num].append(r[1])
                            data_all_timestamp_seq_list[user_num].append(datetime.datetime.fromtimestamp(int(r[2].replace(' ', '')[:-3].upper())).strftime('%Y-%m-%d'))
                            
                    else:
                        data_all_userapp_seq_list[user_num].append(r[1])
                        data_all_timestamp_seq_list[user_num].append(datetime.datetime.fromtimestamp(int(r[2].replace(' ', '')[:-3].upper())).strftime('%Y-%m-%d'))
                        
    return (data_all_userapp_seq_list, data_all_timestamp_seq_list)


'''
Extract application sequence only for user labels and timestamps 
(Allow repeated acation sequence)
'''
def extract_userapp_seq_allow_repeats(input_data_file, data_app_label, test_users):
    data_all_userapp_seq_list = []
    data_all_timestamp_seq_list = []
    for i in range(0, len(test_users)):
        data_all_userapp_seq_list.append([])
        data_all_timestamp_seq_list.append([])
        
    with open(input_data_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if r[1] == "AppName":
                continue
            
            if test_users.has_key(r[0]):
                user_num = test_users[r[0]]
                
                """ Remove web domain values of web browsers like Safari (www.google.com) -> Safari """
                if str(r[1]).find('Safari (') > -1:
                    r[1] = "Safari"
                elif str(r[1]).find('Google Chrome (') > -1:
                    r[1] = "Google Chrome"
                elif str(r[1]).find('HP LaserJet 500 colorMFP M570d') > -1:
                    r[1] = "HP LaserJet 500 colorMFP M570d"
                elif str(r[1]).find('Photosmart Premium C309g-m') > -1:    
                    r[1] = "Photosmart Premium C309g-m"

                """
                if r[1] not in data_app_label:
                    print str(r[1]) + " is not in the labeled list"
                    continue
                """
                
                """ Extract only user labeled applications AND Change the timestamp format from POSIX to human readable """    
                if data_app_label[r[1]] == "user":
                    data_all_userapp_seq_list[user_num].append(r[1])
                    data_all_timestamp_seq_list[user_num].append(datetime.datetime.fromtimestamp(int(r[2].replace(' ', '')[:-3].upper())).strftime('%Y-%m-%d'))
                         
                    '''   
                    l = len(data_all_userapp_seq_list[user_num])
                    if l > 0:
                        #last_app = data_all_userapp_seq_list[user_num][l-1]
                        
                        if last_app != r[1]:
                            data_all_userapp_seq_list[user_num].append(r[1])
                            data_all_timestamp_seq_list[user_num].append(datetime.datetime.fromtimestamp(int(r[2].replace(' ', '')[:-3].upper())).strftime('%Y-%m-%d'))
                            
                    else:
                        data_all_userapp_seq_list[user_num].append(r[1])
                        data_all_timestamp_seq_list[user_num].append(datetime.datetime.fromtimestamp(int(r[2].replace(' ', '')[:-3].upper())).strftime('%Y-%m-%d'))
                    '''
                        
    return (data_all_userapp_seq_list, data_all_timestamp_seq_list)


def extract_app_seq_from_csv(input_data_file, t_size):
    data_app_seq = []
    data_timestamp_seq = []
    
    with open(input_data_file, 'r') as csvfile:
        is_first_row = True
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if is_first_row == True:
                is_first_row = False
                continue
            
            data_app_seq.append(r[0])
            data_timestamp_seq.append(r[1])
    
    return (data_app_seq, data_timestamp_seq)


'''
Reduce length of repeating sequences, for example, 1,2,1,2,1,2,3,4 => 1,2,1,2,3,4 where the num_allowed_repeat = 4
'''
def reduce_seq(tmp_data_all_userapp_seq_list, tmp_data_all_timestamp_seq_list, num_allowed_repeat):
    data_all_userapp_seq_list = []
    data_all_timestamp_seq_list = []
    
    for user_i in range(0, len(tmp_data_all_userapp_seq_list)):
        data_all_userapp_seq_list.append([])
        data_all_timestamp_seq_list.append([])
        
        data_all_userapp_seq_list[user_i].append(tmp_data_all_userapp_seq_list[user_i][0])
        data_all_userapp_seq_list[user_i].append(tmp_data_all_userapp_seq_list[user_i][1])
        data_all_timestamp_seq_list[user_i].append(tmp_data_all_timestamp_seq_list[user_i][0])
        data_all_timestamp_seq_list[user_i].append(tmp_data_all_timestamp_seq_list[user_i][1])
        
        #first_repeat_app = tmp_data_all_userapp_seq_list[user_i][0]
        #second_repeat_app = tmp_data_all_userapp_seq_list[user_i][1]
        last_repeat_app = tmp_data_all_userapp_seq_list[user_i][1]
        
        length = 2
        for app_i in range(1, (len(tmp_data_all_userapp_seq_list[user_i]) - 1)):
            prev_app = tmp_data_all_userapp_seq_list[user_i][(app_i - 1)]
            curr_app = tmp_data_all_userapp_seq_list[user_i][app_i]
            next_app = tmp_data_all_userapp_seq_list[user_i][(app_i + 1)]
            
            if prev_app != next_app:
                if length > (num_allowed_repeat-1) and curr_app != last_repeat_app:
                    data_all_userapp_seq_list[user_i].append(curr_app)
                    data_all_timestamp_seq_list[user_i].append(tmp_data_all_timestamp_seq_list[user_i][app_i])
                    
                data_all_userapp_seq_list[user_i].append(next_app)
                data_all_timestamp_seq_list[user_i].append(tmp_data_all_timestamp_seq_list[user_i][(app_i + 1)])
                #first_repeat_app = curr_app
                #second_repeat_app = next_app
                last_repeat_app = next_app
                length = 2
            else:
                    length = length + 1
                    if length <= (num_allowed_repeat-1):
                        data_all_userapp_seq_list[user_i].append(next_app)
                        data_all_timestamp_seq_list[user_i].append(tmp_data_all_timestamp_seq_list[user_i][(app_i + 1)])
                        last_repeat_app = next_app
 
    return (data_all_userapp_seq_list, data_all_timestamp_seq_list)
    
    
    
'''
Extract action sequence from UDC dataset
(Allow repeated action sequence)
'''
def extract_action_UDC(input_data_file, test_users):
    data_all_action_seq_list = []
    data_all_timestamp_seq_list = []
    for i in range(0, len(test_users)):
        data_all_action_seq_list.append([])
        data_all_timestamp_seq_list.append([])
        
    first_date = 0
    last_date = 0
    
    with open(input_data_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if r[0] == "userId":
                continue
            
            if test_users.has_key(r[0]):
                user_num = test_users[r[0]]
                
                """ Extract only user actions AND Change the timestamp format from POSIX to human readable """    
                data_all_action_seq_list[user_num].append(r[1])
                #print int(r[2].replace(' ', '')[:-3].upper())
                current_date = datetime.datetime.fromtimestamp(int(r[2].replace(' ', '')[:-3].upper())).strftime('%Y-%m-%d')
                data_all_timestamp_seq_list[user_num].append(current_date)
                       
                if first_date == 0:
                    first_date = current_date
                    
                last_date = current_date     
       
    #print first_date
    #print last_date   
                        
    return (data_all_action_seq_list, data_all_timestamp_seq_list)    
    


'''
Extract action sequence from Word dataset
(Allow repeated action sequence)
'''
def extract_action_Word(input_data_file, test_users):
    data_all_action_seq_list = []
    data_all_timestamp_seq_list = []
    for i in range(0, len(test_users)):
        data_all_action_seq_list.append([])
        data_all_timestamp_seq_list.append([])
        
    first_date = 0
    last_date = 0
    
    with open(input_data_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if r[0] == "USER-ID":
                continue
            
            if test_users.has_key(r[0]):
                user_num = test_users[r[0]]
                
                """ Extract only user actions AND Change the timestamp format from YY-MM-DD to YYYY-MM-DD """    
                data_all_action_seq_list[user_num].append(r[1])

                #splited_date = r[2].split("-")
                #current_date = str(int(splited_date[1])) + "/" + str(int(splited_date[2])) + "/" + "19" + splited_date[0]
                current_date = "19" + str(r[2])
                data_all_timestamp_seq_list[user_num].append(current_date)
                       
                if first_date == 0:
                    first_date = current_date
                    
                last_date = current_date     
       
    #print first_date
    #print last_date   
                        
    return (data_all_action_seq_list, data_all_timestamp_seq_list)    


'''
Extract action sequence from RealityMining dataset
(Allow repeated action sequence)
'''

def convertDatetime(dt):
   result = datetime.date.fromordinal(int(dt)) + datetime.timedelta(days=dt%1) - datetime.timedelta(days=366) - datetime.timedelta(hours=5)
   return result.strftime('%Y-%m-%d')

def extract_action_RealityMining(input_data_file, test_users):
    data_all_action_seq_list = []
    data_all_timestamp_seq_list = []
    for i in range(0, len(test_users)):
        data_all_action_seq_list.append([])
        data_all_timestamp_seq_list.append([])
        
    first_date = 0
    last_date = 0
    
    with open(input_data_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for r in reader:
            if r[0] == "user_id":
                continue
            
            if test_users.has_key(r[0]):
                user_num = test_users[r[0]]
                
                """ Extract only user actions AND Change the timestamp format from POSIX to human readable """    
                data_all_action_seq_list[user_num].append(r[1])
                #print r[2]
                current_date = convertDatetime(float(r[2]))
                data_all_timestamp_seq_list[user_num].append(current_date)
                #print current_date
                       
                if first_date == 0:
                    first_date = current_date
                    
                last_date = current_date     
       
    #print first_date
    #print last_date   
                        
    return (data_all_action_seq_list, data_all_timestamp_seq_list) 

