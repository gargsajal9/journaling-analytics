shinyUI(fluidPage(
  titlePanel("Visualizations of PS598 Class Group Project Journaling URL corpus"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Similarity visualizations for 121 web pages (marked relevant, and with at least 1kB of text content) associated with the PS598 international security class group project in Fall 2015. Processing steps:"),
      
      p("1. Extract ASCII text from URLs using DiffBot, and filter for >1k of text content"),
      p("2. Transform lower case, remove stop-words, whitespace, punctuation & numbers, then stem"),
      p("3. Create a term-doc matrix using TF/IDF weights"),
      p("4. Calculate Cosine similarity between all pairs"),
      p("5. Run 2-D t-SNE embedding algorithm on 121x121 matrix"),
      p("6. Plot results with coloured points and labelled in various ways"),
      
      radioButtons("colors", label = "Choose color scheme for points:",
                   choices = list("By Domain"=1, "By Group (Topic)"=2, "By Analysis Stage"=3, "By Task"=4), selected=2),
      
      radioButtons("labels", label = "Choose label for each point:",
                   choices = list("Domain"=1, "URL"=2, "Group (Topic)"=3, "Analysis Stage"=4, "Task"=5, "None"=6),selected=6),
      
      h4("References"),
      a("Shiny for RStudio", href="http://shiny.rstudio.com", target="_blank"),
      br(),
      a("t-SNE algorithm", href="http://lvdmaaten.github.io/tsne/", target="_blank"),
      br(),
      br(),
      p("(c) PJ 2015-11-16")
    ),
    
    mainPanel(plotOutput("tsne"))
  )
))