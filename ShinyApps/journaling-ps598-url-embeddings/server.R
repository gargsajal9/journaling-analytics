# Script to process PS598 Journaling URL corpus for Shiny
# PJ 16/11/2015 (built from orginal example by NFS)

#install.packages("tm")
library(tm)
                   
#corp <- VCorpus(DirSource(directory="corpus-diffbot-text-1000", mode="text", recursive="TRUE"), 
#                readerControl=list(reader=readPlain))

#class(corp)
#mode(corp)
#inspect(corp[1])
#print(corp[[4]])

# Create a corpus file and save it to source file location
#setwd("~/Documents/RProjects/journaling-ps598-url-embeddings")
#save(corp,file="corpus-diffbot-text-1000.RData")

# Load corpus from file
load(file="corpus-diffbot-text-1000.RData")

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

#install.packages("lsa")
library(lsa)

# Create a simple TermDocumentMatrix using term frequency (tf)
#tdm <- TermDocumentMatrix(corp)

# Create a TermDocumentMatrix using tf-idf
tdm <-t(DocumentTermMatrix(corp,control = list(weighting = function(x) weightTfIdf(x, normalize = FALSE))))

# cosine similarity  matrix between 
# all column vectors of matrix
#tdm_cos <- 1-(cosine(as.textmatrix(as.matrix(tdm))))

# Use Option-Command-L to clear console!

# Calculate euclidean/cosine distance between documents
library(fields)
#doc_term_dist_euclid <- rdist(t(as.matrix(tdm)), t(as.matrix(tdm)))
doc_term_dist_cosine <- cosine(as.matrix(tdm)) # or 1-cosine? # Preserves row names

#---------------------------------
# Vector Embedding visualizations
#---------------------------------

# Use t-SNE embedding
#install.packages("tsne")
library(tsne)

PS598_tsne_cosine <- tsne(as.matrix(doc_term_dist_cosine),max_iter=2000)

# URL labels
url_names_0 = doc_term_dist_cosine[,0]
url_names = rownames(doc_term_dist_cosine)
domains <- rapply(strsplit(url_names,"_"), function(x) head(x, 1))

# Load in group dictionary
grp = read.csv("tmp-http-url-group-dict.csv")

# Load in assignment dictionary
ass = read.csv("tmp-http-url-assignment-dict.csv")

# Load in sub-task dictionary
sub = read.csv("tmp-http-url-subtask-dict.csv")

# For each entry in url_names, look up the URL in the grp, ass and sub dictionaries. If it exists,
# append assignment or subtask to the appropriate array. If not, append an empty string.
groups<-NULL
assignments<-NULL
subtasks<-NULL

# A bug in this section was causing incorrect labelling of URLs - now check what happens if
# grep matches no URLs in the dictionary or more than one.
for (url in url_names) 
{
  # Add group labels to each URL
  index <- grep(url,grp[,1],ignore.case=F)
  if(length(index)==0) { group <- "NONE" } else 
   {group <- as.character(grp[index,2])}
  groups <- c(groups,paste(group))
  
  # Add assignment labels to each URL
  index <- grep(url,ass[,1],ignore.case=F)
  if(length(index)==0) { assignment <- "NONE" } else 
  {assignment <- as.character(ass[index,2])}
  assignments <- c(assignments,paste(assignment))
  
  # Add subtask labels to each URL
  index <- grep(url,sub[,1],ignore.case=F)
  if(length(index)==0) { subtask <- "NONE" } else 
  {subtask <- as.character(sub[index,2])}
  subtasks <- c(subtasks,paste(subtask))
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
      else if(input$colors=="2") { # Color by Group (Topic)
        cols <- as.factor(groups)
        col.rainbow <- rainbow(length(unique(groups)))
        palette(col.rainbow)
      }
      else if(input$colors=="3") { # Color by Task (Assignment)
        cols <- as.factor(assignments)
        col.rainbow <- rainbow(length(unique(assignments)))
        palette(col.rainbow)
      }
      else { # Color by Sub-task (Action)
        cols <- as.factor(subtasks)
        col.rainbow <- rainbow(length(unique(subtasks)))
        palette(col.rainbow)
      }
      
      data <- PS598_tsne_cosine
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
      else if(input$labels=="3") { # Label by Group (Topic)
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix")
        d <- data.frame(data, names=domains)
        text(d[,1],d[,2]-text_offset,labels=groups,cex=0.6,col="black")
      }
      else if(input$labels=="4") { # Label by Analysis Stage
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix")
        d <- data.frame(data, names=domains)
        text(d[,1],d[,2]-text_offset,labels=assignments,cex=0.6,col="black")
      }
      else if(input$labels=="5") { # Label by Task
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix")
        d <- data.frame(data, names=domains)
        text(d[,1],d[,2]-text_offset,labels=subtasks,cex=0.6,col="black")
      }
      else { # No labels
        plot(data, col=cols, pch=16, main="2D embedding of similarity between URLs in Term-Doc Matrix")
      }
      
    }, height = 800)
  }
)
