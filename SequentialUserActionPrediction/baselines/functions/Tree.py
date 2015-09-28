'''
Created on Mar 24, 2015

@author: Changsung Moon
'''

from ete2 import Tree
from copy import deepcopy

def updateTree(tree, sub_seq, target):
    sub_seq_rev = deepcopy(list(reversed(sub_seq)))
    
    for i in range(0, len(sub_seq_rev)):
        ind = i
        
        cur_node = tree.get_tree_root()
                        
        while ind >= 0:
            item = sub_seq_rev[ind]
        
            children_nodes = cur_node.get_children()
            children_names = []
            
            for children_node in children_nodes:
                children_names.append(children_node.name)
            
            if item not in children_names:
                cur_node = cur_node.add_child(name=item, dist=1)
            else:
                child_i = children_names.index(item)
                cur_node = children_nodes[child_i]
            
                if ind == 0:
                    last_children_nodes = cur_node.get_children()
                    last_children_names = []
                    
                    for last_children_node in last_children_nodes:
                        last_children_names.append(last_children_node.name)
                        
                    if target in last_children_names:    
                        target_i = last_children_names.index(target)
                        target_node = last_children_nodes[target_i]
                        target_node.dist = target_node.dist + 1
                    else:
                        cur_node = cur_node.add_child(name=target, dist=1)
                        
            ind = ind - 1
        
    return tree


def calScore(tree, sub_seq, target):
    score = 0
    weight = 0
    sub_seq_rev = deepcopy(list(reversed(sub_seq)))
    
    for i in range(0, len(sub_seq_rev)):
        ind = i
        #found = True
        freq = 0
        weight = weight + 1
        
        cur_node = tree.get_tree_root()
        
        while ind >= 0:
            item = sub_seq_rev[ind]
            
            children_nodes = cur_node.get_children()
            children_names = []
            
            for children_node in children_nodes:
                children_names.append(children_node.name)
            
            if item not in children_names:
                #found = False
                break
            else:
                child_i = children_names.index(item)
                cur_node = children_nodes[child_i]
            
                if ind == 0:
                    last_children_nodes = cur_node.get_children()
                    last_children_names = []
                    
                    for last_children_node in last_children_nodes:
                        last_children_names.append(last_children_node.name)
                        
                    if target in last_children_names:
                        target_i = last_children_names.index(target)
                        target_node = last_children_nodes[target_i]
                        score = score + (weight * target_node.dist)
                        
                        '''
                        print last_children_names
                        print weight
                        print target_node.dist
                        print score
                        '''
            
            ind = ind - 1
            
        #if found == False:
            #break
    
    return score


def buildFreqTree(data_seq, depth):
    
    t = Tree() # Creates an empty tree
    
    for start_i in range(0, len(data_seq)):
        end_i = start_i + depth - 1
        
        if end_i >= len(data_seq):
            end_i = len(data_seq) - 1
            
        sub_seq = data_seq[start_i:(end_i+1)]
        
        if len(sub_seq) <= 1:
            break
        
        cur_node = t.get_tree_root()
        
        for item in sub_seq:
            children_nodes = cur_node.get_children()
            children_names = []
            
            for children_node in children_nodes:
                children_names.append(children_node.name)
                
            #print children_names
            
            if item not in children_names:
                cur_node = cur_node.add_child(name=item, dist=1)
            else:
                child_i = children_names.index(item)
                cur_node = children_nodes[child_i]
                cur_node.dist = cur_node.dist + 1
    
    
    return t

"""
''' TEST '''
data_seq = ['A', 'A', 'B', 'C', 'B', 'C', 'A', 'B', 'C', 'B']
#data_seq = ['A', 'A', 'B', 'C', 'B']
depth = 4

t = buildFreqTree(data_seq, depth)
print t.get_ascii(attributes=["name", "dist"], show_internal=True)

sub_seq = ['B']
target = 'C'

s = calScore(t, sub_seq, target)
print s

updated_tree = updateTree(t, ['A', 'A', 'B'], 'D')
print updated_tree.get_ascii(attributes=["name", "dist"], show_internal=True)
"""