# -------------------------------------------------------------------------------
# CSC791 Project 2 - Paul Jones, Student ID 0001110202, pjones@ncsu.edu
#
# R implementation of k-clique overlapping community detection algorithm from
# Paper 6 - "Uncovering the overlapping community structure of 
# complex networks in nature and society", Palla et al, 2005.
#
# Note: key parts of the algorithm are implemented as functions, which reside in
# a separate file - this is both to improve source code clarity and to provide
# more meaningful profiling results from Rprof.
#
# Script last updated: October 3, 2014
# -------------------------------------------------------------------------------

# Import functions from separate file
source("k-clique-comm-detection-functions.R")

if(!interactive()) { args<-commandArgs(TRUE) }
if(interactive()) { args<-commandArgs() }

if(length(args)!=1)
{
	stop("Must supply an argument of youtube, dblp or amazon.")
}

out_dir <- paste("output",args[1],sep="-")
cat("Writing to output directory:",out_dir,"\n")

dir.create(out_dir, showWarnings = FALSE)

library(igraph)

# Enable CPU profiling
prof_file <- paste(out_dir,"Rprof.out",sep="/")
Rprof(filename = prof_file, append = FALSE, interval = 0.02,
      memory.profiling = FALSE, gc.profiling = FALSE, 
      line.profiling = FALSE, numfiles = 100L, bufsize = 10000L)
       
# Get current working directory (not needed in Rscript mode)
#this.dir <- dirname(parent.frame(2)$ofile) 
#setwd(this.dir) 

# Compose name of graph file from command line argument
# CHANGE THIS TO PROCESS DIFFERENT SIZED GRAPHS
graph_file <- paste("graphs/",args[1],".graph.small",sep="")

# --------------------------------------------------------------------------------
# Ingest graph and report basic statistics, including clique number
# --------------------------------------------------------------------------------

# Log timestamp (for profiling) and display progress
now <- format(Sys.time(), "%H:%M:%OS3")
cat(now,"Ingesting",graph_file,"... ")

# Read in graph as an edgelist - file must be preprocessed to remove header line
G=read.graph(graph_file,format=c("edgelist"),directed=FALSE)

# Report an estimate of the memory consumed by the graph
cat(format(object.size(G),units="auto"),"\n")

# Find clique number (size of maximal clique)
C=clique.number(G)

# Report graph statistics (for debugging)
now <- format(Sys.time(), "%H:%M:%OS3")
cat(now,"Graph has",length(V(G)),"vertices,",length(E(G)),"edges, and clique number",C,"\n")

# ----------------------------------------------------------------------------------
# Run the k-clique community detection algorithm and save output to files
# ----------------------------------------------------------------------------------

now <- format(Sys.time(), "%H:%M:%OS3")
cat(now,"Finding all maximal cliques in the graph... ")

# First, extract all maximal cliques (maximal complete subgraphs)
c=maximal.cliques(G)

# Report an estimate of the memory consumed by the maximal cliques object
cat(format(object.size(c),units="auto"),"\n")

now <- format(Sys.time(), "%H:%M:%OS3")
cat(now,"Calculating clique overlap matrix... ")

# Next, calculate the clique overlap matrix (this is the most resource intensive part)
m <- clique_overlap(c)

# Report an estimate of the memory consumed by the matrix
cat(format(object.size(m),units="auto"),"\n")

# Given the clique overlap matrix, we can now quickly find all communities using k-cliques
# from size 2 up to the clique-number. We then combine results and remove sub-sets to
# extract all the maximal communities in the original graph.

kcc_comm_list <- list()

for(k in 2:2) # CHANGE THIS TO ONLY INCLUDE SOME CLIQUE SIZES (was 2:C)
{
	now <- format(Sys.time(), "%H:%M:%OS3")
    cat(now,"Finding communities for k =",k,"... ")
	
    # Find k-clique components (separate components in the k-clique matrix)
    kcc <- k_clique_components(m,k)

    # Extract k-clique communities using the original clique list
    kcc_comm <- k_clique_communities(kcc,c)
    
    kcc_comm_list <- append(kcc_comm_list, kcc_comm)
    
    # Report an estimate of the memory consumed by the community list
    cat(format(object.size(kcc_comm),units="auto"),"\n")
}

# Finally, we combine the k-clique communities to find maximal communities.
# Sort first by length, then iterate over the list, find subsets, and remove.

now <- format(Sys.time(), "%H:%M:%OS3")
cat(now,"Combining and de-duping... ")

for(possible_subset in kcc_comm_list)
{
    for(set in kcc_comm_list)
    {
        # Check if the current list is shorter (necessary condition for a subset)
        if(length(possible_subset) < length(set))
        {
            if(length(setdiff(possible_subset,set))==0)
            {
                # Debugging
             	#cat("Removing dupe:",possible_subset," from ",set,"\n")
            	
                # Delete the dupe
                kcc_comm_list[possible_subset] <- NULL

                # Break out of the inner for loop - no point checking any others since the possible
                # subset doesn't exist any more!
                break
            }
        }
    }    
}

# Report an estimate of the memory consumed by the combined list
cat(format(object.size(kcc_comm_list),units="auto"),"\n")

# --------------------------------------------------------------------------------
# Prepare output files and tidy up
# --------------------------------------------------------------------------------

now <- format(Sys.time(), "%H:%M:%OS3")
cat(now,"Preparing output file... ")

# Remove NULL entries from the list
kcc_comm_list[sapply(kcc_comm_list, is.null)] <- NULL

# Subtract 1 from each node ID (igraph uses 1-offset; input files are 0-offset)
kcc_comm_list <- rapply(kcc_comm_list,function(x) x=x-1,how="replace")

# Print ready for output file
out_comm_file <- paste(out_dir,"output-comm.txt",sep="/")
out <- lapply(kcc_comm_list, cat, "\n", file=out_comm_file, append=TRUE)

cat("done.\n")

# Stop profiling
Rprof(NULL)

# Summarise the Rprof results and write them to a file
profsumm_file <- file(paste(out_dir,"Rprof-summary.out",sep="/"),"w+")
sink(profsumm_file,type="output")
summprof <- summaryRprof(filename = prof_file, chunksize = 5000, memory = "none", 
            lines = "hide", index = 2, diff = TRUE, exclude = NULL, basenames = 1)
summprof
sink()
flush(profsumm_file)
close(profsumm_file)

