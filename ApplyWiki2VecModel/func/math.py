'''
Created on Oct 30, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''


def cal_width(weight, threshold):
    width = 0
    
    if weight >= threshold and weight < 0.5:
        width = 1
    elif weight >= 0.5 and weight < 0.6:
        width = 2
    elif weight >= 0.6 and weight < 0.7:
        width = 3
    elif weight >= 0.7 and weight < 0.8:
        width = 4
    elif weight >= 0.8 and weight < 0.9:
        width = 5
    elif weight >= 0.9 and weight <= 1.0:
        width = 6
        
        
    '''    
    if weight >= 0.0 and weight < 0.1:
        width = 1
    elif weight >= 0.1 and weight < 0.2:
        width = 2
    elif weight >= 0.2 and weight < 0.3:
        width = 3
    elif weight >= 0.3 and weight < 0.4:
        width = 4
    elif weight >= 0.4 and weight < 0.5:
        width = 5
    elif weight >= 0.5 and weight < 0.6:
        width = 6
    elif weight >= 0.6 and weight < 0.7:
        width = 7
    elif weight >= 0.7 and weight < 0.8:
        width = 8
    elif weight >= 0.8 and weight < 0.9:
        width = 9
    elif weight >= 0.9 and weight <= 1.0:
        width = 10
    '''
        
        
    return width
