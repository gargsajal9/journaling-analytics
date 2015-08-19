shinyUI(fluidPage(
  #tags$head(tags$script(src = "message-handler.js")),
  titlePanel("Community Detection on Similarity Graphs for CSC791 Journaling document corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Community Detection on Similarity graph for 96 PDF documents associated with the CSC791 advanced algorithms class in Spring 2015. Steps:"),
      
      p("1. Extract ASCII text from PDFs (no Unicode)"),
      p("2. Transform: lower case, remove whitespace, punctuation, numbers, stop-words & stem"),
      p("3. Create a term-doc matrix using TF-IDF weights"),
      p("4. Calculate Cosine similarity between pairs of docs"),
      p("5. Threshold to create 96x96 adjacency matrix"),
      
      sliderInput("threshold","Choose proximity threshold for creating an edge:",
                               min=0,max=1,value=0.2),
    
      p("6. Run community detection on the resulting graph."),
      
      selectInput("cdalgorithm", 
                  label = "Choose a community detection algorithm:",
                  choices = c("Fast Greedy Modularity Optimization","Edge-Betweenness","Label Propagation"),
                  selected = "Fast Greedy Modularity Optimization"),
      
      verbatimTextOutput("comms_found"),
      
      p("7. Plot resulting graph with various color options."),
      
      radioButtons("coloring", label = "Color nodes by:",
                   choices = list("Assignment (Goal)"=1, "Community"=2),selected=2),

      #actionButton("run", "Run community detection on this graph"),
      
      h4("References"),
      a("K-clique Community Detection", href="http://www.nature.com/nature/journal/v435/n7043/abs/nature03607.html", target="_blank"),
      br(),
      a("Community Detection in iGraph", href="http://www.r-bloggers.com/summary-of-community-detection-algorithms-in-igraph-0-6/", target="_blank"),
      br(),
      a("Modularity in Networks", href="http://www.pnas.org/content/103/23/8577.full"),
      br(),
      br(),
      p("(c) PJ 2015-08-16")
    ),
    
    mainPanel(plotOutput("proxgraph"))
  )
))