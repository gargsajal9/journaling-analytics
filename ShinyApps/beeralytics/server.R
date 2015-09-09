# Beeralytics Shiny App
# PJ 7/9/2015

# Read from Untappd export file (exported as XLS to get column headers, 
# then saved as CSV, and non-printable chars removed)
beers_raw = read.csv("checkin-report_09_07_15_with_header.csv", encoding = "latin1") # or UTF-8

# Remove duplicate rows based on beer name - should be exactly 500 remaining
beers_raw <- subset(beers_raw, !duplicated(beers_raw$beer_name))

# Replace zeroes in ABV and IBU with NA so we don't bias our averages
# This seems to break things since I can't run mean below with mean(na.rm=TRUE) !!
#beers_raw[c("beer_abv", "beer_ibu")][beers_raw[c("beer_abv", "beer_ibu")]==0] <- NA

# Averages per group - use these to impute some missing values for IBU and ABV
av_ibu<-aggregate(beers_raw[,c("beer_ibu")], list(beers_raw$beer_type), mean)
av_ibu_list<-av_ibu$x
names(av_ibu_list)=av_ibu$Group.1
av_abv<-aggregate(beers_raw[,c("beer_abv")], list(beers_raw$beer_type), mean)
av_abv_list<-av_abv$x
names(av_abv_list)=av_abv$Group.1

# Remove NAs in entire data frame
beers_raw[is.na(beers_raw)] <- 0

# Iterate over beer_ibu and beer_abv columns - replace any zeroes with average value from list
beers_imputed=beers_raw
for (row in seq_along(beers_raw$beer_ibu)) {
  if(beers_raw$beer_ibu[row]==0) {
    beers_imputed$beer_ibu[row]=av_ibu_list[beers_raw$beer_type[row]]
  }
  if(beers_raw$beer_abv[row]==0) {
    beers_imputed$beer_abv[row]=av_abv_list[beers_raw$beer_type[row]]
  }
}

# Create jittery versions
beers_raw_jitter=beers_raw
beers_raw_jitter$beer_ibu=jitter(beers_raw$beer_ibu, factor=1, amount=1)
beers_raw_jitter$beer_abv=jitter(beers_raw$beer_abv, factor=1, amount=0.05)
beers_imputed_jitter=beers_imputed
beers_imputed_jitter$beer_ibu=jitter(beers_imputed$beer_ibu, factor=1, amount=1)
beers_imputed_jitter$beer_abv=jitter(beers_imputed$beer_abv, factor=1, amount=0.05)

# Set a unique color for each beer style
colors = rainbow(length(unique(beers_raw$beer_type))) # Create a color for each beer type
names(colors) = sort(unique(beers_raw$beer_type)) # Assign alphabetically by type

# Set a unique color for each rating
#rating_colors = rainbow(length(unique(beers$rating_score))) # Create a color for each rating

# There are only 17 possible ratings so manually create a pallette in grayscale
rating_colors = c("#eeeeee","#eaeaea","#dddddd","#dadada","#cccccc","#bbbbbb","#aaaaaa",
                  "#999999","#888888","#777777","#666666","#555555",
                  "#444444","#333333","#222222","#111111","#000000")

names(rating_colors) = sort(unique(beers_raw$rating_score))

#ecb = function(x,y){ plot(x,t='n'); text(x, labels=beers$beer_type, col=colors[beers$beer_type])}

# Server code - gets run whenever a user loads the app or clicks a widget (so minimal computation)
shinyServer(
  function(input, output) {
    output$beers <- renderPlot({
      
      if(input$impute) { if(input$jitter) { beers=beers_imputed_jitter} else { beers=beers_imputed } }
      else { if(input$jitter) { beers=beers_raw_jitter } else { beers=beers_raw } }
      
      if(input$col_scheme=="1") { # Style
        if(!input$zoom) {
          # Simple plot of ABV vs IBU, colored by style
          plot(beers$beer_abv, beers$beer_ibu, col=colors[beers$beer_type], pch=16, cex=0.5, 
               xlim=c(0,11), ylim=c(0,100),main="Paul's 500 Beers on Untappd, coloured by Style", 
               xlab="Alcohol by Volume (%)", ylab="International Bitterness Units (IBU)")
          if (input$names) text(beers$beer_abv, beers$beer_ibu+1.1,labels=beers$beer_name,cex=0.5,col=colors[beers$beer_type])
          if (input$breweries) text(beers$beer_abv, beers$beer_ibu-1.1,labels=beers$brewery_name,cex=0.5,col=colors[beers$beer_type])
          legend(-0.2,102,names(colors[1:44]),col=colors[1:44],pch=16,cex=0.6,pt.cex=0.6,bty="n")
          legend(1.8 ,102,names(colors[45:88]),col=colors[45:88],pch=16,cex=0.6,pt.cex=0.6,bty="n")
        }
        else {
          # Simple plot of ABV vs IBU, colored by style (zoomed)
          plot(beers$beer_abv, beers$beer_ibu, col=colors[beers$beer_type], pch=16, cex=0.5, 
               xlim=c(4,6), ylim=c(5,40),main="Paul's 500 Beers on Untappd, coloured by Style\n(Zoomed on Sensible Beers Only)", 
               xlab="Alcohol by Volume (%)", ylab="International Bitterness Units (IBU)")
          if (input$names) text(beers$beer_abv, beers$beer_ibu+0.3,labels=beers$beer_name,cex=0.5,col=colors[beers$beer_type])
          if (input$breweries) text(beers$beer_abv, beers$beer_ibu-0.3,labels=beers$brewery_name,cex=0.5,col=colors[beers$beer_type])
          #legend(-0.2,102,names(colors[1:44]),col=colors[1:44],pch=16,cex=0.5,pt.cex=0.5,bty="n")
          #legend(1.8 ,102,names(colors[45:88]),col=colors[45:88],pch=16,cex=0.5,pt.cex=0.5,bty="n")
        }
      }
      else if(input$col_scheme=="2") { # rating
        if(!input$zoom) {
          # Simple plot of ABV vs IBU, colored by rating
          plot(beers$beer_abv, beers$beer_ibu, col=rating_colors[as.character(beers$rating_score)], pch=16, cex=0.5, 
               xlim=c(0,11), ylim=c(0,100),main="Paul's 500 Beers on Untappd, coloured by Rating", 
               xlab="Alcohol by Volume (%)", ylab="International Bitterness Units (IBU)")
          if (input$names) text(beers$beer_abv, beers$beer_ibu+1.3,labels=beers$beer_name,cex=0.5,col=rating_colors[as.character(beers$rating_score)])
          if (input$breweries) text(beers$beer_abv, beers$beer_ibu-1.3,labels=beers$brewery_name,cex=0.5,col=rating_colors[as.character(beers$rating_score)])
          legend(0,100,names(rating_colors),col=rating_colors,pch=16,cex=1.0,pt.cex=1.0,bty="n",title="Rating")
        }
        else {
          # Simple plot of ABV vs IBU, colored by rating (zoomed)
          plot(beers$beer_abv, beers$beer_ibu, col=rating_colors[as.character(beers$rating_score)], pch=16, cex=0.5, 
               xlim=c(4,6), ylim=c(5,40),main="Paul's 500 Beers on Untappd, coloured by Rating\n(Zoomed on Sensible Beers Only)", 
               xlab="Alcohol by Volume (%)", ylab="International Bitterness Units (IBU)")
          if (input$names) text(beers$beer_abv, beers$beer_ibu+0.3,labels=beers$beer_name,cex=0.5,col=rating_colors[as.character(beers$rating_score)])
          if (input$breweries) text(beers$beer_abv, beers$beer_ibu-0.3,labels=beers$brewery_name,cex=0.5,col=rating_colors[as.character(beers$rating_score)])
          #legend(3.95,40,names(rating_colors),col=rating_colors,pch=16,cex=0.5,pt.cex=0.5,bty="n",title="Rating")
        }
      }
      
      # TO DO - add ability to label by beer name and brewery
      #plot(data, col=cols, pch=16, main="2D embedding of similarity between docs in Term-Doc Matrix")
      #d <- data.frame(data, names=doc_names)
      #text_offset <- ((max(data[,2])-min(data[,2]))/100)
      #if (input$filenames) text(d[,1],d[,2]+text_offset,labels=row.names(d),cex=0.4,col="black")
      #if (input$assignments) text(d[,1],d[,2]-text_offset,labels=assignments,cex=0.6,col="black")
      
      # For graphs
      #plot(graph.adjacency(doc_sim_graph_cosine,mode="undirected",diag=FALSE), vertex.size=5, vertex.color=cols, vertex.label.font=2, vertex.label.cex=0.5, vertex.label=assignments, vertex.label.color="white")
      
    }, height = 800)
  }
)

# identify points 
#identify(beers$beer_abv, beers$beer_ibu, labels=beers$beer_name) 

# Failed attempt at t-SNE
#library(tsne)
# Numerical columns are ABV, IBU and Rating
#tsne_beers = tsne(beers[,c("beer_abv", "beer_ibu", "rating_score")], 
#                  epoch_callback = ecb, initial_dims=3, k=2, max_iter=100, perplexity=50)
#plot(tsne_beers)