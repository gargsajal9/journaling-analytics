shinyUI(fluidPage(
  titlePanel("Paul's 'Beeralytics' - scatter plots of the ~500 Beers I've registered on Untappd"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("I wanted to find a nice way to show all the beers I've tried in one 2D plot. 
               After playing with various embeddings, I found that just plotting ABV vs IBU 
               separated them reasonably well and gave clear meaning to the axes. Processing options:"),
      
      checkboxInput("impute", label = "Impute some missing IBU and ABV values using average for the beer style.", value = FALSE),
      
      checkboxInput("jitter", label = "Add small amounts of random jitter (noise) to ABV and IBU to improve separation.", value = FALSE),
      
      radioButtons("col_scheme", label = "Colour beers by:",
                   choices = list("Style"=1, "Paul's Rating"=2),selected=1),
      
      p("Most beers seem to have ABV between 4 and 6, and IBU between about 5 and 40."),
      
      checkboxInput("zoom", label = "Zoom in on 'typical' beers only", value = FALSE),
      
      p("Labels make the plots look a little cluttered so you can turn these on and off."),
      
      checkboxInput("names", label = "Add beer name labels", value = TRUE),
      checkboxInput("breweries", label = "Add brewery labels", value = FALSE),
      
      p("Please send ideas for how to improve my beeralytics!  (pjones@ncsu.edu)"),
      
      h4("References"),
      a("Untappd", href="http://untappd.com", target="_blank"),
      br(),
      a("What's the meaning of IBU?",href="https://www.beerconnoisseur.com/articles/whats-meaning-ibu", target="_blank"),
      br(),
      a("Shiny for RStudio", href="http://shiny.rstudio.com", target="_blank"),
      br(),
      br(),
      p("(c) PJ 2015-09-06")
    ),
    
    mainPanel(plotOutput("beers"))
  )
))