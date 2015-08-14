shinyUI(fluidPage(
  titlePanel("Visualizations of CSC791 class Journaling document corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Similarity visualizations for 97 PDF documents associated with the CSC791 advanced algorithms class in Spring 2015."),
      
      p("Processing steps:"),
      p("1. Extract ASCII text from PDFs (no Unicode) and transform to lower case"),
      p("2. Remove whitespace, punctuation and numbers"),
      p("3. Remove English stop-words and apply stemming"),
      p("4. Create a term-document matrix using TF/IDF weights"),
      p("5. Calculate proximity between all pairs of documents"),
      
      selectInput("algorithm", 
                  label = "Choose a proximity measure:",
                  choices = c("Cosine","Euclidean","Kullback-Leibler"),
                  selected = "Cosine"),
      
      p("6. Run 2-D embedding algorithm on 97x97 matrix"),
      
      radioButtons("embedding", label = "Choose embedding algorithm:",
                   choices = list("PCA"=1, "MDS"=2, "t-SNE"=3),selected=3),
    
      p("7. Plot results with points coloured by assignment number"),
      
      checkboxInput("filenames", label = "Show document filenames", value = TRUE),
      checkboxInput("assignments", label = "Show assignment numbers", value = TRUE),
      
      h4("References"),
      a("Shiny for RStudio", href="http://shiny.rstudio.com", target="_blank"),
      br(),
      a("t-SNE algorithm", href="http://lvdmaaten.github.io/tsne/", target="_blank"),
      br(),
      br(),
      p("(c) PJ 2015-08-11 (with thanks to SL and NFS)")
    ),
    
    mainPanel(plotOutput("tsne"))
  )
))