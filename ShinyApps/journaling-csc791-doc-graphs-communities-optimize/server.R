# Script to process CSC791 Journaling corpus for Shiny
# PJ 30/8/2015 (built from orginal example by NFS)

#install.packages("tm")
library(tm)
library(igraph)

# PJ - TO INGEST MONTHLY NOTES PDF DOCUMENTS ON MAC
# (1) Had to install Xpdf v3.04 (http://www.foolabs.com/xpdf/download.html)
# (2) Extracted tarball to home dir, and copied 64-bit executables to /usr/local/bin
# (3) Create directory consisting of only PDF files (67 so far)
# (4) Run this command - should get no warnings
corp <- VCorpus(DirSource(directory="CSC791_Corpus_Pdf", mode="binary", recursive="TRUE"), 
                readerControl=list(reader=readPDF))

#setwd("/Users/pjones/Google Drive/LAS Monthly Reports Efforts for DO5/CSC791_Corpus_RawTxt")
#writeCorpus(corp)

#-----------------------------------
# Text Preprocessing
#-----------------------------------

# Dakota's magic code to remove invalid unicode
corp <- tm_map(corp, content_transformer(function(x) iconv(iconv(x, "latin1", "ASCII", sub = ""), sub = "")))

# Other transformations
corp <- tm_map(corp, stripWhitespace)
corp <- tm_map(corp, removePunctuation)
corp <- tm_map(corp, removeNumbers)
corp <- tm_map(corp, content_transformer(tolower))

# Stopword removal
corp <- tm_map(corp, removeWords, stopwords("english"))
#print(corp[[4]])

# Stemming
#install.packages("SnowballC")
library(SnowballC)
corp <- tm_map(corp, stemDocument)
#print(corp[[4]])

library(lsa)

# Create a TermDocumentMatrix using term frequency (tf) or tf-idf
#tdm_tf <- TermDocumentMatrix(corp)
tdm_tfidf <-t(DocumentTermMatrix(corp,control = list(weighting = function(x) weightTfIdf(x, normalize = TRUE))))

# Calculate distance between documents
doc_term_dist_cosine_tfidf <- cosine(as.matrix(tdm_tfidf))

# Document labels
doc_names = doc_term_dist_cosine_tfidf[,0] # Euclid names not available but are the same
assignments <- c("A2","A2","A3","A6","A6","A6","A6","A6","A6","A6","A6","A6","A6","A6","E1","CL","CL","CL","H1","H1",
                 "H1","H1","H1","H2","H2","H2","H4","H5","H5","H5","H6","H6","H6","J1","J1","J1","J1","J1","L1","LE",
                 "LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE","LE",
                 "LE","LE","LE","P3","P3","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5",
                 "P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","P5","T1","T2","T2","T3","T3")

# TO DO - go back and label LE documents with the assignments that they correspond to. This should improve performance.

# Colour by assignment number - now happens dynamically
#cols <- as.factor(assignments)
#col.rainbow <- rainbow(18)
#col.rainbow[13]="#000000ff" # lecture notes
#palette(col.rainbow)

# Only using Cosine TF-IDF in this app
doc_term_dist <- doc_term_dist_cosine_tfidf

# Server code - gets run whenever a user loads the app or clicks a widget (so minimal computation)
shinyServer(
  function(input, output, session) {
    
    #----------------------------------
    # Graph visualization
    #----------------------------------
    
    output$proxgraph <- renderPlot({
      
      threshold <- input$threshold
      doc_sim_graph <- doc_term_dist
      doc_sim_graph[doc_term_dist<threshold] <- 0
      doc_sim_graph[doc_term_dist>=threshold] <- 1
      G <- graph.adjacency(doc_sim_graph,mode="undirected",diag=FALSE)
      
      # Remove assignment labels for a certain percentage of the data
      assignments2<-assignments
      rvals<-runif(length(assignments2),0,100)
      for(index in seq_along(rvals)) { if(rvals[index]<input$labelpc) { assignments2[index]="?" } }
      
      # Create pallette for the assignment numbers we have available
      cols <- as.factor(assignments2)
      col.rainbow <- rainbow(length(levels(cols))+1)
      col.rainbow[1]="#000000ff" # unlabelled
      palette(col.rainbow)
      
      if(input$coloring=="1") { # Color by Assignment
        V(G)$color <- cols
      }
      
      # Run community detection algorithm and plot results
      if(input$cdalgorithm=="Fast Greedy Modularity Optimization") {
        Gcom <- fastgreedy.community(G)
        if(input$coloring=="2") { # Color by Community
          V(G)$color <- Gcom$membership + 1
        }
      }
      else if(input$cdalgorithm=="Edge-Betweenness") { # Edge Betweenness
        Gcom <- edge.betweenness.community(G)
        if(input$coloring=="2") { # Color by Community
          V(G)$color <- Gcom$membership + 1
        }
      }
      else { # Label Propagation
        Gcom <- label.propagation.community(G)
        if(input$coloring=="2") { # Color by Community
          V(G)$color <- Gcom$membership + 1
        }
      }
      
      # Counters for correct and incorrect classifications
      correct=0
      wrong=0
      
      # Guess a label for each community based on a majority vote of labelled documents
      # TO DO: this is horribly slow!
      for (comm in 1:max(Gcom$membership)) { # Iterate over communities we found
        assignments3<-assignments2
        for (doc_num in 1:length(assignments2)) { # Extract documents in this community
          if (Gcom$membership[doc_num]==comm) { assignments3[doc_num]=assignments2[doc_num] }
          else { assignments3[doc_num]<-NA }
        }
        # Convert ? to NA, then do majority vote on remainder (sorts ties randomly)
        assignments4<-assignments3
        assignments4[assignments4=="?"]<-NA
        winner<-sort(table(assignments4),decreasing=TRUE)[1] # Extract 'winner'
        
        if(!is.null(names(winner)) && length(winner)>0) {
          # Now, with this winner label, what proportion of ? in this community get labelled correctly?
          for(doc_num in 1:length(assignments3)) {
            if(!is.na(assignments3[doc_num]) && assignments3[doc_num]=="?") {
              #print(c("assignment",assignments[doc_num],"guess",names(winner)))
              if (assignments[doc_num]==names(winner)) { correct=correct+1 } # We classified it correctly
              else { wrong=wrong+1 }
            }
          }
        } # END if(no winner)
        else { # We have no way of labelling this community so must count all members as wrong
          wrong=wrong+sum(Gcom$membership==comm)
        }
      } # Go to next community
      
      # Update text output to say how many communities we found
      output$comms_found <- renderText({
        paste("Communities:",max(Gcom$membership)," AvModularity:",round(mean(Gcom$modularity),digits=2),
              "Correct:",correct," Wrong:",wrong, " %CorrectlyLabelled:", round(100*correct/(correct+wrong),digits=0))
      })
      
      # Plot the graph using chosen color scheme and (ideally) a deterministic layout, although
      # I can't find a deterministic layout that looks half-decent (circle and sphere are crap).
      layout = layout.fruchterman.reingold(G)
      plot(G,  vertex.size=5, vertex.label.font=2, vertex.label.cex=0.5, 
           vertex.label=assignments2, vertex.label.color="white", layout=layout,
           main="Graph embedding of similarity between docs in Term-Doc Matrix")
      
    }, height = 800)
  }
)
