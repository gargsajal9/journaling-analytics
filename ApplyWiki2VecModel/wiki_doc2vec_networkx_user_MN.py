'''
Created on Oct 29, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from gensim_models import doc2vec

from func.math import cal_width

import networkx as nx


import time
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#model = doc2vec.Doc2Vec.load("../models/wiki_doc2vec/MN_People_1000feat_5min_8context_mean_NoStopwords_complete_Wiki")
#model = doc2vec.Doc2Vec.load("/Users/csmoon/Documents/workspace/models/wiki_doc2vec/MN_People_1000feat_5min_8context_mean_NoStopwords_complete_Wiki")

num_feature = 1000      # number of features
threshold_user = 0.6    # similarity threshold between users
threshold_topic = 0.5   # similarity threshold between an user and a keyword


show_user_edge = True   # show edge between users
show_topic_edge = True  # show edge between an user and a keyword

show_user_node = True   # show user nodes
show_topic_node = True  # show keyword nodes

# Parameter of loaded doc2vec model: mean or sum
sum_or_mean = 'mean'

# Index of the divided dataset based on time period (ex., 1 means the first 3 months of the dataset in this case)
dataset_index = 1
# 0 means the whole months, and number indicates the time period of the divided dataset
months = 0

if months == 0:
    users = ['FeleciaVega', 'Laughlin', 'JDH', 'streck', 'mlbarne', 'tait', 'Ariana', 'William', 'tma', 'Cumbee', 'jmkeis2', 'Amass', 'SBent', 'Wachter', 'PJ', 'Boone', 'esricha', 'EDB', 'Moore', 'Mumford', 'CVazquez', 'aaamosbi', 'Cstacy', 'awhairst']
elif months == 3:
    if dataset_index == 1:
        users = ['EDB', 'Moore', 'Mumford', 'William', 'aaamosbi', 'mlbarne', 'PJ', 'awhairst', 'JDH']
    elif dataset_index == 2:
        users = ['EDB', 'JDH', 'Mumford', 'tait', 'SBent', 'William', 'aaamosbi', 'mlbarne', 'PJ', 'tma', 'awhairst']
    elif dataset_index == 3:
        users = ['Laughlin', 'JDH', 'Mumford', 'Wachter', 'streck', 'SBent', 'aaamosbi', 'mlbarne', 'tait', 'Cumbee', 'PJ', 'tma', 'awhairst']    
    elif dataset_index == 4:
        users = ['Laughlin', 'SBent', 'Wachter', 'streck', 'tma', 'aaamosbi', 'tait', 'Cstacy', 'PJ', 'Cumbee', 'awhairst']
    elif dataset_index == 5:    
        users = ['Amass', 'FeleciaVega', 'Laughlin', 'JDH', 'Mumford', 'CVazquez', 'streck', 'SBent', 'Ariana', 'William', 'tma', 'mlbarne', 'tait', 'Cstacy', 'Boone', 'Wachter', 'PJ', 'Cumbee', 'esricha', 'awhairst', 'jmkeis2']

 
if months == 0:   
    model = doc2vec.Doc2Vec.load("../models/wiki_doc2vec/MN_People_1000feat_5min_8context_" + str(sum_or_mean) + "_NoStopwords_complete_Wiki")
else:
    model_name = "../models/wiki_doc2vec/MN_People_1000feat_5min_8context_" + str(sum_or_mean) + "_NoStopwords_" + str(dataset_index) + "_" + str(months) + "months" 
    model = doc2vec.Doc2Vec.load(model_name)
    

# A list of keywords
topics = ['infrastructure', 'cognitive', 'workflow', 'semantic', 'analysis', 'instrumentation', 'journaling', 'application', 'web', 'collaboration', 'model', 'data', 'narrative', 'framework', 'visualization']
removed_topics = ['future', 'budget', 'nfl', 'conference', 'security', 'government', 'staff', 'financial', 'management', 'database', 'language']


# Draw a graph through networkx package
G=nx.Graph()

if show_user_node == True:
    G.add_nodes_from(users)

if show_topic_node == True:
    G.add_nodes_from(topics)


# Add edges between users
if show_user_edge == True:
    for i in range(0, len(users)):
        user_i = users[i]
        
        for j in range(i+1, len(users)):
            user_j = users[j]
            
            edge_w = model.similarity('User_%s' % user_i, 'User_%s' % user_j)
            
            if edge_w > threshold_user:
                G.add_edge(user_i, user_j, weight=edge_w)


# Add edges between user and topic
if show_topic_edge == True:
    for user in users:
        for topic in topics:
            edge_w = model.similarity('User_%s' % user, topic)
            
            if edge_w > threshold_topic:
                G.add_edge(user, topic, weight=edge_w)


#pos = nx.graphviz_layout(G)
pos=nx.spring_layout(G) # positions for all nodes

#nx.draw(G, with_labels=True)
#nx.draw_random(G)
#nx.draw_circular(G)
#nx.draw_spectral(G)
#nx.draw_networkx(G, pos)

#plt.savefig("path.png")


if show_user_node == True:
    nx.draw_networkx_nodes(G,pos,
                           nodelist=users,
                           node_color='r',
                           node_size=400,
                       alpha=0.4)
    
if show_topic_node == True:
    nx.draw_networkx_nodes(G,pos,
                           nodelist=topics,
                           node_color='b',
                           node_size=300,
                       alpha=0.4)


for (u,v,d) in G.edges(data='weight'):
    if (v in topics) or (u in topics):
        edge_c = 'b'
        edge_w = cal_width(d['weight'], threshold_topic)    # Adjust width of an edge according to its weight
    else:
        edge_c = 'r'
        edge_w = cal_width(d['weight'], threshold_user)     # Adjust width of an edge according to its weight
    
    nx.draw_networkx_edges(G,pos, edgelist=[(u, v)], width=edge_w, alpha=0.3,edge_color=edge_c)


labels = {}


for node in G.nodes():
    labels[node] = node
    
nx.draw_networkx_labels(G,pos,labels,font_size=10)


plt.show()
