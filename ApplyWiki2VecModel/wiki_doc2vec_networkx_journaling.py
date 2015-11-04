'''
Created on Oct 29, 2015

@author: Changsung Moon (cmoon2@ncsu.edu)
'''


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.manifold import TSNE

from gensim_models import doc2vec

from func.math import cal_width

import networkx as nx


import time
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


model = doc2vec.Doc2Vec.load("../models/wiki_doc2vec/CSC791_Doc_1000feat_5min_8context_mean_NoStopwords_complete_Wiki")
#model = doc2vec.Doc2Vec.load("/Users/csmoon/Documents/workspace/models/wiki_doc2vec/CSC791_Doc_1000feat_5min_8context_mean_NoStopwords_complete_Wiki")

num_feature = 1000          # number of features
threshold_doc = 0.6         # similarity threshold between documents
threshold_topic = 0.5       # similarity threshold between a document and a keyword

show_doc_edge = True        # show edge between documents
show_topic_edge = False     # show edge between a document and a keyword

show_doc_node = True        # show document nodes
show_topic_node = False     # show keyword nodes

# A list of documents
docs = ['P5-Capstone_9', 'A2_1', 'A2_2', 'P5-Capstone_1', 'P5-Capstone_3', 'P5-Capstone_2', 'P5-Capstone_5', 'P5-Capstone_4', 'P5-Capstone_7', 'P5-Capstone_6', 'A6_4', 'A6_5', 'A6_6', 'A6_7', 'A6_1', 'A6_2', 'A6_3', 'A6_8', 'A6_9', 'J1_2', 'J1_3', 'J1_1', 'J1_4', 'P3_1', 'H2_3', 'H2_2', 'H2_1', 'P5-Capstone_8', 'L1_1', 'General_1', 'General_2', 'General_3', 'H1_1', 'E1_1', 'H1_3', 'H1_4', 'H1_5', 'T3_2', 'T3_1', 'A6_10', 'A6_11', 'H1_2', 'T1_1', 'H5_1', 'H5_2', 'H5_3', 'P5-Capstone_11', 'P5-Capstone_10', 'P5-Capstone_13', 'P5-Capstone_12', 'P5-Capstone_15', 'P5-Capstone_14', 'P5-Capstone_17', 'P5-Capstone_16', 'P5-Capstone_19', 'P5-Capstone_18', 'H6_1', 'T2_2', 'T2_1', 'Lecture_6', 'Lecture_7', 'Lecture_4', 'Lecture_5', 'Lecture_2', 'Lecture_3', 'Lecture_1', 'Lecture_8', 'Lecture_9', 'Lecture_25', 'Lecture_24', 'Lecture_21', 'Lecture_20', 'Lecture_23', 'Lecture_22', 'A3_1', 'H4_1', 'H6_3', 'P3_2', 'H6_2', 'Lecture_10', 'Lecture_11', 'Lecture_12', 'Lecture_13', 'Lecture_14', 'Lecture_15', 'Lecture_16', 'Lecture_17', 'Lecture_18', 'Lecture_19', 'P5-Capstone_24', 'P5-Capstone_25', 'P5-Capstone_26', 'P5-Capstone_20', 'P5-Capstone_21', 'P5-Capstone_22', 'P5-Capstone_23']

# A list of keywords
topics = []

# No Lecture
#docs = ['P5-Capstone_9', 'A2_1', 'A2_2', 'P5-Capstone_1', 'P5-Capstone_3', 'P5-Capstone_2', 'P5-Capstone_5', 'P5-Capstone_4', 'P5-Capstone_7', 'P5-Capstone_6', 'A6_4', 'A6_5', 'A6_6', 'A6_7', 'A6_1', 'A6_2', 'A6_3', 'A6_8', 'A6_9', 'J1_2', 'J1_3', 'J1_1', 'J1_4', 'P3_1', 'H2_3', 'H2_2', 'H2_1', 'P5-Capstone_8', 'L1_1', 'General_1', 'General_2', 'General_3', 'H1_1', 'E1_1', 'H1_3', 'H1_4', 'H1_5', 'T3_2', 'T3_1', 'A6_10', 'A6_11', 'H1_2', 'T1_1', 'H5_1', 'H5_2', 'H5_3', 'P5-Capstone_11', 'P5-Capstone_10', 'P5-Capstone_13', 'P5-Capstone_12', 'P5-Capstone_15', 'P5-Capstone_14', 'P5-Capstone_17', 'P5-Capstone_16', 'P5-Capstone_19', 'P5-Capstone_18', 'H6_1', 'T2_2', 'T2_1', 'A3_1', 'H4_1', 'H6_3', 'P3_2', 'H6_2', 'P5-Capstone_24', 'P5-Capstone_25', 'P5-Capstone_26', 'P5-Capstone_20', 'P5-Capstone_21', 'P5-Capstone_22', 'P5-Capstone_23']

# No Lecture, No Capstone
#docs = ['A2_1', 'A2_2', 'A6_4', 'A6_5', 'A6_6', 'A6_7', 'A6_1', 'A6_2', 'A6_3', 'A6_8', 'A6_9', 'J1_2', 'J1_3', 'J1_1', 'J1_4', 'P3_1', 'H2_3', 'H2_2', 'H2_1', 'L1_1', 'General_1', 'General_2', 'General_3', 'H1_1', 'E1_1', 'H1_3', 'H1_4', 'H1_5', 'T3_2', 'T3_1', 'A6_10', 'A6_11', 'H1_2', 'T1_1', 'H5_1', 'H5_2', 'H5_3', 'H6_1', 'T2_2', 'T2_1', 'A3_1', 'H4_1', 'H6_3', 'P3_2', 'H6_2']

topics = []


# Draw a graph through networkx package
G=nx.Graph()

if show_doc_node == True:
    G.add_nodes_from(docs)

if show_topic_node == True:
    G.add_nodes_from(topics)


# Add edges between documents
if show_doc_edge == True:
    for i in range(0, len(docs)):
        doc_i = docs[i]
        
        for j in range(i+1, len(docs)):
            doc_j = docs[j]
            
            edge_w = model.similarity('Doc_%s' % doc_i, 'Doc_%s' % doc_j)
            
            if edge_w > threshold_doc:
                G.add_edge(doc_i, doc_j, weight=edge_w)


# Add edges between document and topic
if show_topic_edge == True:
    for doc in docs:
        for topic in topics:
            edge_w = model.similarity('Doc_%s' % doc, topic)
            
            if edge_w > threshold_topic:
                G.add_edge(doc, topic, weight=edge_w)


#pos = nx.graphviz_layout(G)
pos=nx.spring_layout(G) # positions for all nodes

#nx.draw(G, with_labels=True)
#nx.draw_random(G)
#nx.draw_circular(G)
#nx.draw_spectral(G)
#nx.draw_networkx(G, pos)

#plt.savefig("path.png")


if show_doc_node == True:
    nx.draw_networkx_nodes(G,pos,
                           nodelist=docs,
                           node_color='r',
                           node_size=400,
                       alpha=0.5)

if show_topic_node == True:
    nx.draw_networkx_nodes(G,pos,
                           nodelist=topics,
                           node_color='b',
                           node_size=300,
                       alpha=0.5)


for (u,v,d) in G.edges(data='weight'):

    if (v in topics) or (u in topics):
        edge_c = 'b'
        edge_w = cal_width(d['weight'], threshold_topic)    # Adjust width of an edge according to its weight
    else:
        edge_c = 'r'
        edge_w = cal_width(d['weight'], threshold_doc)      # Adjust width of an edge according to its weight
    
    nx.draw_networkx_edges(G,pos, edgelist=[(u, v)], width=edge_w, alpha=0.3,edge_color=edge_c)


labels = {}


for node in G.nodes():
    labels[node] = node
    
nx.draw_networkx_labels(G,pos,labels,font_size=10)


plt.show()
