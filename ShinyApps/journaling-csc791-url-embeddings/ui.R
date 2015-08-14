shinyUI(fluidPage(
  titlePanel("Visualizations of CSC791 class Journaling URL corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Similarity visualizations for 347 web pages (with at least 1kB of text content) associated with the CSC791 advanced algorithms class in Spring 2015."),
      
      p("Processing steps:"),
      p("1. Extract ASCII text from URLs using DiffBot, and filter for >1k of text content"),
      p("2. Transform lower case, remove whitespace, punctuation and numbers"),
      p("3. Remove English stop-words and apply stemming"),
      p("4. Create a term-document matrix using TF/IDF weights"),
      p("5. Calculate Cosine similarity between all pairs of documents"),
      p("6. Run 2-D t-SNE embedding algorithm on 347x347 matrix"),
      p("7. Plot results with coloured points and labelled in various ways"),
      
      radioButtons("colors", label = "Choose color scheme for points:",
                   choices = list("By Domain"=1, "By Assignment"=2),selected=2),
      
      radioButtons("labels", label = "Choose label for each point:",
                   choices = list("Domain"=1, "URL"=2, "Assignment"=3, "None"=4),selected=4),
      
      h4("References"),
      a("Shiny for RStudio", href="http://shiny.rstudio.com", target="_blank"),
      br(),
      a("t-SNE algorithm", href="http://lvdmaaten.github.io/tsne/", target="_blank"),
      br(),
      br(),
      p("(c) PJ 2015-08-14 (with thanks to SL and NFS)")
    ),
    
    mainPanel(plotOutput("tsne"))
  )
))