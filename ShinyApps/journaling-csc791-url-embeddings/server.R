# Script to process CSC791 Journaling URL corpus for Shiny
# PJ 14/8/2015 (built from orginal example by NFS)

#install.packages("tm")
library(tm)

# check file formats supported by the data readers
#getReaders()

# PJ - TO INGEST MONTHLY NOTES PDF DOCUMENTS ON MAC
# (1) Had to install Xpdf v3.04 (http://www.foolabs.com/xpdf/download.html)
# (2) Extracted tarball to home dir, and copied 64-bit executables to /usr/local/bin
# (3) Create directory consisting of only PDF files (67 so far)
# (4) Run this command - should get no warnings

#corp <- VCorpus(DirSource(directory="/Users/pjones/Google Drive/LAS Monthly Reports Efforts for DO5/CSC791_Corpus_Pdf",
#                   mode="binary", recursive="TRUE"), readerControl=list(reader=readPDF))
                   
corp <- VCorpus(DirSource(directory="corpus-diffbot-text-1000", mode="text", recursive="TRUE"), 
                readerControl=list(reader=readPlain))

#class(corp)
#mode(corp)
#inspect(corp[1])
#print(corp[[4]])

#setwd("/Users/pjones/Google Drive/LAS Monthly Reports Efforts for DO5/CSC791_Corpus_RawTxt")
#writeCorpus(corp)

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
#tdm <- TermDocumentMatrix(corp)

# Create a TermDocumentMatrix using tf-idf
tdm <-t(DocumentTermMatrix(corp,control = list(weighting = function(x) weightTfIdf(x, normalize = FALSE))))

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

# Calculate euclidean/cosine distance between documents
library(fields)
#doc_term_dist_euclid <- rdist(t(as.matrix(tdm)), t(as.matrix(tdm)))
doc_term_dist_cosine <- cosine(as.matrix(tdm)) # or 1-cosine? # Preserves row names

# Calculate KL distance between URLs
#library(entropy)
#doc_term_dist_kl <- matrix(data=0, nrow=97, ncol=97)
#combn( ncol(as.matrix(tdm)), 2, 
#      function(x) doc_term_dist_kl[x[1],x[2]] <- KL.plugin(t(as.matrix(tdm[,x[1]])+0.1),t(as.matrix(tdm[,x[2]])+0.1)))
#for (c1 in 1:ncol(tdm)) {
#  for (c2 in 1:ncol(tdm)) {
#    doc_term_dist_kl[c1,c2] <- KL.plugin(t(as.matrix(tdm[,c1])+0.1),t(as.matrix(tdm[,c2])+0.1)) }}
  
# This should be a 97x97 distance matrix
#dim(as.matrix(doc_term_dist))

# Testing for graph plotting
# TO DO: move to separate app!
#threshold <- 0.2
#doc_sim_graph_cosine <- doc_term_dist_cosine
#doc_sim_graph_cosine[doc_term_dist_cosine<threshold] <- 0
#doc_sim_graph_cosine[doc_term_dist_cosine>=threshold] <- 1
#plot(graph.adjacency(doc_sim_graph_cosine,mode="undirected",diag=FALSE))

#---------------------------------
# Vector Embedding visualizations
#---------------------------------

# Optional clean-up stwp (replace NaN with 0)
# replace all non-finite values with 0
#doc_term_dist_euclid[!is.finite(doc_term_dist_euclid)] <- 0
#doc_term_dist_cosine[!is.finite(doc_term_dist_cosine)] <- 0
#doc_term_dist_kl[!is.finite(doc_term_dist_kl)] <- 0

# Use first two components of PCA for our embedding
#CSC791_pca_euclid <- prcomp(doc_term_dist_euclid)
#CSC791_pca_euclid <- cbind(CSC791_pca_euclid$x[,1],CSC791_pca_euclid$x[,2])
#CSC791_pca_cosine <- prcomp(doc_term_dist_cosine)
#CSC791_pca_cosine <- cbind(CSC791_pca_cosine$x[,1],CSC791_pca_cosine$x[,2])
#CSC791_pca_kl <- prcomp(doc_term_dist_kl)
#CSC791_pca_kl <- cbind(CSC791_pca_kl$x[,1],CSC791_pca_kl$x[,2])

# MDS embedding with 2 dimensions
#CSC791_mds_euclid <- cmdscale(doc_term_dist_euclid, k=2)
#CSC791_mds_cosine <- cmdscale(doc_term_dist_cosine, k=2, add=TRUE)$points # Additive const, otherwise fails
#CSC791_mds_kl <- cmdscale(doc_term_dist_kl, k=2)

# Use t-SNE embedding
#install.packages("tsne")
library(tsne)
#CSC791_tsne_euclid <- tsne(as.matrix(doc_term_dist_euclid),max_iter=2000)
CSC791_tsne_cosine <- tsne(as.matrix(doc_term_dist_cosine),max_iter=2000)
#CSC791_tsne_kl <- tsne(as.matrix(doc_term_dist_kl),max_iter=2000)

# URL labels
url_names_0 = doc_term_dist_cosine[,0]
url_names = rownames(doc_term_dist_cosine)
domains <- rapply(strsplit(url_names,"_"), function(x) head(x, 1))

# Load in assignment dictionary
ass = read.csv("tmp-http-url-assignment-dict.csv")

# For each entry in url_names, look up the URL in the ass dictionary. If it exists,
# append the assignment number to the assignments array. If not, append an empty string.
assignments<-NULL
for (url in url_names) {
  assignment <- ass[grep(url,ass[,1],ignore.case=T),2]
  assignments <- c(assignments,paste(assignment))
}

# Server code - gets run whenever a user loads the app or clicks a widget (so minimal computation)
shinyServer(
  function(input, output) {
    output$tsne <- renderPlot({
      
      if(input$colors=="1") { # Color by Domain
        cols <- as.factor(domains)
        col.rainbow <- rainbow(length(unique(domains)))
        palette(col.rainbow)
      }
      else { # Color by Assignment
        cols <- as.factor(assignments)
        col.rainbow <- rainbow(length(unique(assignments)))
        palette(col.rainbow)
      }
      
      data <- CSC791_tsne_cosine
      text_offset <- ((max(data[,2])-min(data[,2]))/100)
      
      if(input$labels=="1") { # Label by Domain
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix") 
        d <- data.frame(data, names=domains)
        text(d[,1],d[,2]+text_offset,labels=d$names,cex=0.4,col="black")
      }
      else if(input$labels=="2") { # Label by full URL
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix")
        d <- data.frame(data, names=url_names_0)
        text(d[,1],d[,2]+text_offset,labels=row.names(d),cex=0.4,col="black")
      }
      else if(input$labels=="3") { # Label by Assignment Number
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix")
        d <- data.frame(data, names=domains)
        text(d[,1],d[,2]-text_offset,labels=assignments,cex=0.6,col="black")
      }
      else { # No labels
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix")
      }
      
    }, height = 800)
  }
)
