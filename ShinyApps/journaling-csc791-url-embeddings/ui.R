shinyUI(fluidPage(
  titlePanel("Visualizations of CSC791 class Journaling URL corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Similarity visualizations for 347 web pages (with at least 1kB of text content) associated with the CSC791 advanced algorithms class in Spring 2015. Processing steps:"),
      
      p("1. Extract ASCII text from URLs using DiffBot, and filter for >1k of text content"),
      p("2. Transform lower case, remove stop-words, whitespace, punctuation & numbers, then stem"),
      p("3. Create a term-doc matrix using TF/IDF weights"),
      p("4. Calculate Cosine similarity between all pairs"),
      p("5. Run 2-D t-SNE embedding algorithm on 347x347 matrix"),
      p("6. Plot results with coloured points and labelled in various ways"),
      
      radioButtons("colors", label = "Choose color scheme for points:",
                   choices = list("By Domain"=1, "By Task (Assignment)"=2, "By Sub-task (Action)"=3), selected=2),
      
      radioButtons("labels", label = "Choose label for each point:",
                   choices = list("Domain"=1, "URL"=2, "Task (Assignment)"=3, "Sub-task (Action)"=4, "None"=5),selected=5),
      
      h4("References"),
      a("Shiny for RStudio", href="http://shiny.rstudio.com", target="_blank"),
      br(),
      a("t-SNE algorithm", href="http://lvdmaaten.github.io/tsne/", target="_blank"),
      br(),
      br(),
      p("(c) PJ 2015-08-19 (with thanks to SL and NFS)")
    ),
    
    mainPanel(plotOutput("tsne"))
  )
))