shinyUI(fluidPage(
  titlePanel("Similarity Graphs of CSC791 class Journaling document corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Similarity graph visualizations for 97 PDF documents associated with the CSC791 advanced algorithms class in Spring 2015."),
      
      p("Processing steps:"),
      p("1. Extract ASCII text from PDFs (no Unicode) and transform to lower case"),
      p("2. Remove whitespace, punctuation and numbers"),
      p("3. Remove English stop-words and apply stemming"),
      p("4. Create a term-document matrix"),
      
      checkboxInput("tfidf", label = "Use TF-IDF weights, as opposed to just term frequencies", value = TRUE),
      
      p("5. Calculate a normalized proximity between all pairs of documents"),
      
      selectInput("algorithm", 
                  label = "Choose a proximity measure:",
                  choices = c("Cosine","Euclidean","Kullback-Leibler"),
                  selected = "Cosine"),
      
      p("6. Threshold on proximity to create 97x97 adjacency matrix"),
      
      sliderInput("threshold","Choose proximity threshold for creating an edge:",
                               min=0,max=1,value=0.2),
    
      p("7. Plot resulting graph with vertices coloured by assignment number."),
      
      #checkboxInput("filenames", label = "Show document filenames", value = TRUE),
      #checkboxInput("assignments", label = "Show assignment numbers", value = TRUE),
      
      h4("References"),
      a("Shiny for RStudio", href="http://shiny.rstudio.com", target="_blank"),
      br(),
      br(),
      p("(c) PJ 2015-08-12 (with thanks to SL and NFS)")
    ),
    
    mainPanel(plotOutput("proxgraph"))
  )
))