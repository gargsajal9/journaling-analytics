shinyUI(fluidPage(
  #tags$head(tags$script(src = "message-handler.js")),
  titlePanel("Optimizing Community Detection on Similarity Graphs for CSC791 Journaling docs"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Optimizing Community Detection on Similarity graph for 96 PDF documents from CSC791 advanced algorithms class in Spring 2015. Steps:"),
      
      p("1. Extract ASCII text from PDFs (no Unicode), and transform: lower case, remove whitespace, punctuation, numbers, stop-words & stem"),
      p("2. Create a term-doc matrix using TF-IDF weights, calculate Cosine similarity between pairs of docs, and threshold to create 96x96 adjacency matrix"),
      
      sliderInput("threshold","Choose proximity threshold for creating an edge:",
                               min=0,max=1,value=0.2),
    
      sliderInput("labelpc","Choose proportion of missing labels (%):",
                  min=0,max=100,value=30),
      
      p("3. Run community detection on the resulting graph."),
      
      selectInput("cdalgorithm", 
                  label = "Choose a community detection algorithm:",
                  choices = c("Fast Greedy Modularity Optimization","Edge-Betweenness","Label Propagation"),
                  selected = "Fast Greedy Modularity Optimization"),
      
      p("4. Label communities with assignment by majority vote and determine proportion of missing labels correctly assigned (we want to maximize this)."),
      
      verbatimTextOutput("comms_found"),
      
      p("5. Plot resulting graph with various color options."),
      
      radioButtons("coloring", label = "Color nodes by:",
                   choices = list("Assignment (Goal)"=1, "Community"=2),selected=1),

      #actionButton("run", "Run community detection on this graph"),
      
      h4("References"),
      a("Community Detection in iGraph", href="http://www.r-bloggers.com/summary-of-community-detection-algorithms-in-igraph-0-6/", target="_blank"),
      br(),
      a("Modularity in Networks", href="http://www.pnas.org/content/103/23/8577.full"),
      br(),
      br(),
      p("(c) PJ 2015-08-30")
    ),
    
    mainPanel(plotOutput("proxgraph"))
  )
))