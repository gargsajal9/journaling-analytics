# Script to process CSC791 Journaling corpus for Shiny
# PJ 11/8/2015 (built from orginal example by NFS)

#install.packages("tm")
library(tm)
library(igraph)

# check file formats supported by the data readers
#getReaders()

# PJ - TO INGEST MONTHLY NOTES PDF DOCUMENTS ON MAC
# (1) Had to install Xpdf v3.04 (http://www.foolabs.com/xpdf/download.html)
# (2) Extracted tarball to home dir, and copied 64-bit executables to /usr/local/bin
# (3) Create directory consisting of only PDF files (67 so far)
# (4) Run this command - should get no warnings

#corp <- VCorpus(DirSource(directory="/Users/pjones/Google Drive/LAS Monthly Reports Efforts for DO5/CSC791_Corpus_Pdf",
#                   mode="binary", recursive="TRUE"), readerControl=list(reader=readPDF))
                   
#corp <- VCorpus(DirSource(directory="CSC791_Corpus_Pdf", mode="binary", recursive="TRUE"), readerControl=list(reader=readPDF))

#class(corp)
#mode(corp)
#inspect(corp[1])
#print(corp[[4]])

#setwd("/Users/pjones/Google Drive/LAS Monthly Reports Efforts for DO5/CSC791_Corpus_RawTxt")
#writeCorpus(corp)

# Create a corpus file and save it to source file location
#setwd("~/Documents/RProjects/journaling-csc791-doc-graphs")
#save(corp,file="CSC791_Corpus_Pdf.RData")

# Load corpus from file
load(file="../data/CSC791_Corpus_Pdf.RData")

#-----------------------------------
# Text Preprocessing
#-----------------------------------
#getTransformations()
#help(tm_map)

# Dakota's magic code to remove invalid unicode
corp <- tm_map(corp, content_transformer(function(x) iconv(iconv(x, "latin1", "ASCII", sub = ""), sub = "")))

# Other transformations
corp <- tm_map(corp, stripWhitespace)
corp <- tm_map(corp, removePunctuation)
corp <- tm_map(corp, removeNumbers)
corp <- tm_map(corp, content_transformer(tolower))
#mode(corp)

# Stopword removal
corp <- tm_map(corp, removeWords, stopwords("english"))
#print(corp[[4]])

# Stemming
#install.packages("SnowballC")
library(SnowballC)
corp <- tm_map(corp, stemDocument)
#print(corp[[4]])

#setwd("/Users/pjones/Google Drive/LAS Monthly Reports Efforts for DO5/CSC791_Corpus_Transformed")
#writeCorpus(corp)

#-----------------------------------------
# Ex. 3: Build vector-space model for Corpora:
#  Create document-by-terms matrix.
# With such a model one can either view documents
#  in the space of terms/keywords or
#  view terms/keyword in the space of documents
# Once a vector/feature space is built,
# clustering, classification, etc, could be applied
#-----------------------------------------

# Create a term-document matrix from a corpus
# Check the number of documents in the Corpus
#length(corp)
# Documents as rows and terms as columns
#dtm <- DocumentTermMatrix(corp)
#dim(dtm)
#inspect(dtm[2:5, 200:205])
# Note: Matrix is very sparse (too many zero's); apply 
# R packages optimized for sparse matrices (if needed)

# or vice versa: terms is rows and docs as columns
#tdm <- TermDocumentMatrix(corp)
#dim(tdm)
#nspect(tdm[200:205, 2:5])

#-----------------------------------------
# Ex. 4: Basic operations over the Corpus:
#   most frequent terms, terms associated w/
#   other terms, removing sparse terms,
#   include only terms from the dictionary
#-----------------------------------------

# terms that appear in all the documents
#findFreqTerms(dtm, 96)
# terms that appear in at least half of all the documents
#findFreqTerms(dtm, 48)

# terms that are at least 0.8 correlated with count-min"
#findAssocs(dtm, "count-min", 0.8)

# remove sparse terms: removes those terms 
# that are at least 40 percent sparse,
# i.e. at least 40% or more docs do not have this term
#inspect(removeSparseTerms(dtm, 0.4))

#------------------------------
# Ex. 6: LSA (Latent Semantic Analysis)
#   for topic modeling
#------------------------------

#install.packages("lsa")
library(lsa)

# Create a simple TermDocumentMatrix using term frequency (tf)
tdm_tf <- TermDocumentMatrix(corp)

# Create a TermDocumentMatrix using tf-idf
tdm_tfidf <-t(DocumentTermMatrix(corp,control = list(weighting = function(x) weightTfIdf(x, normalize = TRUE))))

# cosine similarity  matrix between 
# all column vectors of matrix
#tdm_cos <- 1-(cosine(as.textmatrix(as.matrix(tdm))))

# perform LSA
#help(dimcalc_share)
#lsaReuters <- lsa(as.textmatrix(as.matrix(tdm)), dims=dimcalc_share())
#plot(lsaReuters$sk)

# Run LSA assuming 2 topics
#lsaMN <- lsa(as.textmatrix(as.matrix(tdm)), dims=2)
#class(lsaMN)
# Note: LSAspace object consists of Tk, Sk, Dk

# terms to topics
# lsaMN$tk
# documents to topics
# lsaMN$dk

# Use Option-Command-L to clear console!

# Function to normalize 0-1
range01 <- function(x){(x-min(x))/(max(x)-min(x))}

# Calculate euclidean/cosine distance between documents
library(fields)
doc_term_dist_euclid_tf <- rdist(t(as.matrix(tdm_tf)), t(as.matrix(tdm_tf)))
doc_term_dist_euclid_tfidf <- rdist(t(as.matrix(tdm_tfidf)), t(as.matrix(tdm_tfidf)))
doc_term_dist_cosine_tf <- cosine(as.matrix(tdm_tf)) # or 1-cosine? # Preserves row names
doc_term_dist_cosine_tfidf <- cosine(as.matrix(tdm_tfidf))

#library(MASS)
#write.matrix(format(doc_term_dist_cosine, scientific=FALSE), 
#             file = paste("/Users/pjones/csc791-cosine-sim.csv"), sep=",")

library(entropy)
doc_term_dist_kl_tf <- matrix(data=0, nrow=97, ncol=97)
doc_term_dist_kl_tfidf <- matrix(data=0, nrow=97, ncol=97)
#combn( ncol(as.matrix(tdm)), 2, 
#      function(x) doc_term_dist_kl[x[1],x[2]] <- KL.plugin(t(as.matrix(tdm[,x[1]])+0.1),t(as.matrix(tdm[,x[2]])+0.1)))
for (c1 in 1:ncol(tdm_tf)) {
  for (c2 in 1:ncol(tdm_tf)) {
    doc_term_dist_kl_tf[c1,c2] <- KL.plugin(t(as.matrix(tdm_tf[,c1])+0.1),t(as.matrix(tdm_tf[,c2])+0.1)) 
    doc_term_dist_kl_tfidf[c1,c2] <- KL.plugin(t(as.matrix(tdm_tfidf[,c1])+0.1),t(as.matrix(tdm_tfidf[,c2])+0.1)) 
    }}

# This should be a 97x97 distance matrix
#dim(as.matrix(doc_term_dist))

# Optional clean-up stwp (replace NaN with 0)
# replace all non-finite values with 0
doc_term_dist_euclid_tf[!is.finite(doc_term_dist_euclid_tf)] <- 0
doc_term_dist_euclid_tfidf[!is.finite(doc_term_dist_euclid_tfidf)] <- 0
doc_term_dist_cosine_tf[!is.finite(doc_term_dist_cosine_tf)] <- 0
doc_term_dist_cosine_tfidf[!is.finite(doc_term_dist_cosine_tfidf)] <- 0
#doc_term_dist_kl[!is.finite(doc_term_dist_kl)] <- 0

doc_term_dist_euclid_tf <- 1-(range01(doc_term_dist_euclid_tf)) # Convert to similarity
doc_term_dist_euclid_tfidf <- 1-(range01(doc_term_dist_euclid_tfidf))
doc_term_dist_cosine_tf <- range01(doc_term_dist_cosine_tf)
doc_term_dist_cosine_tfidf <- range01(doc_term_dist_cosine_tfidf)
doc_term_dist_kl_tf <- 1-(range01(doc_term_dist_kl_tf)) # Convert to similarity
doc_term_dist_kl_tfidf <- 1-(range01(doc_term_dist_kl_tfidf))

# Document labels
doc_names = doc_term_dist_cosine_tf[,0] # Euclid names not available but are the same
assignments <- c("A2","A2","A3","A6","A6","A6","A6","A6","A6","A6","A6","A6","A6","A6","E1","CL","CL","CL","H1","H1",
                 "H1","H1","H1","H2","H2","H2","H4","H5","H5","H5","H6","H6","H6","J1","J1","J1","J1","J1","L1","LE",
                 "LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE",
                 "LE","LE","LE","P3","P3","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5",
                 "P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","T1","T2","T2","T3","T3")

# Colour by assignment number
cols <- as.factor(assignments)
col.rainbow <- rainbow(18)
col.rainbow[13]="#000000ff" # lecture notes
palette(col.rainbow)

# Server code - gets run whenever a user loads the app or clicks a widget (so minimal computation)
shinyServer(
  function(input, output) {
    output$proxgraph <- renderPlot({
    
      if (input$tfidf)  { 
        doc_term_dist <- switch(input$algorithm, "Cosine" = doc_term_dist_cosine_tfidf, 
                                        "Euclidean" = doc_term_dist_euclid_tfidf,
                                        "Kullback-Leibler" = doc_term_dist_kl_tfidf)
      }
      else {
        doc_term_dist <- switch(input$algorithm, "Cosine" = doc_term_dist_cosine_tf, 
                                "Euclidean" = doc_term_dist_euclid_tf,
                                "Kullback-Leibler" = doc_term_dist_kl_tf)
      }
      
      #----------------------------------
      # Graph visualizations
      #----------------------------------
      
      threshold <- input$threshold
      doc_sim_graph <- doc_term_dist
      doc_sim_graph[doc_term_dist<threshold] <- 0
      doc_sim_graph[doc_term_dist>=threshold] <- 1
      
      # Plot the graph
      plot(graph.adjacency(doc_sim_graph,mode="undirected",diag=FALSE), 
           vertex.size=5, vertex.color=cols, vertex.label.font=2, vertex.label.cex=0.5, 
           vertex.label=assignments, vertex.label.color="white",
           main="Graph embedding of similarity between docs in Term-Doc Matrix")
      
      # Add labels
      #d <- data.frame(data, names=doc_names)
      #text_offset <- ((max(data[,2])-min(data[,2]))/100)
      #if (input$filenames) text(d[,1],d[,2]+text_offset,labels=row.names(d),cex=0.4,col="black")
      #if (input$assignments) text(d[,1],d[,2]-text_offset,labels=assignments,cex=0.6,col="black")
      
    }, height = 800)
  }
)
