# ---------------------------------------------------------------------------------------
# Function to calculate a clique overlap matrix from a list of all maximal cliques in 
# the graph (c).
# ---------------------------------------------------------------------------------------

clique_overlap <- function(c)
{
	# Allocate the clique overlap matrix
    num_cliques=length(c)
    m <- matrix(, nrow=num_cliques, ncol=num_cliques)

    # Populate the clique overlap matrix - each row (and column) represents a clique; 
    # the matrix elements are equal to the number of common nodes between the
    # corresponding two cliques, and the diagonal entries are equal to the size of the clique.

    for(row in 1:nrow(m))
    {
	    for(col in 1:row) # Populate lower half only
	    {
		    # Populate with number of elements in common
		    m[row,col]=length(intersect(unlist(c[row]),unlist(c[col])))
	    }
    }
    
    return(m)
 }

# ---------------------------------------------------------------------------------------
# Function to return k-clique component matrix from the clique overlap matrix
# m is a lower-symmetric clique overlap matrix; k is the size of the cliques to use
# ---------------------------------------------------------------------------------------

k_clique_components <- function(m,k)
{
	for(row in 1:nrow(m))
    {
	    for(col in 1:row) # Deal with lower half only
	    {
		    # Delete diagonal elements smaller than k
		    if(col==row && m[row,col]<k) 
		    {
		            m[row,col]=0
		    }
		    # Delete off-diagonal elements that are smaller than k-1
		    else if(col!=row && m[row,col]<(k-1))
		    {
		    	    m[row,col]=0
		    }
		    # Replace all other non-zero elements with 1
		    else if(m[row,col]>1)
		    {
		    	    m[row,col]=1
		    }
	    }
    }
    return (m)
}

# ---------------------------------------------------------------------------------------
# Function to return the community members from the a k-clique component matrix.
# kc is the k-clique component matrix; c is a list of cliques and the nodes each contains
# ---------------------------------------------------------------------------------------

k_clique_communities <- function(kc,c)
{
	# Declare an empty list to hold our communities
	comm_list <- list()
	
    # Extract all non-zero elements, corresponding to the k-communities
    kc_comm <- lapply(seq(NCOL(kc)),function(x) which(kc[,x] == 1))

    # Iterate over the results, extracting the clique IDs that form a community
    for(list_id in kc_comm)
    {
	    if(length(unlist(kc_comm[list_id]))>0)
	    {
	    	# Create an empty vector
	    	s <- vector()
	    	
		    # Extract list of clique IDs that are in a community together
		    for(clique_id in unlist(kc_comm[list_id]))
		    {
			    # Extract node IDs from the original clique list
			    # Combine and dedupe into a single set to output communities
			    s <- sort(union(unlist(c[clique_id]),s))
		    }
		    #cat(s,"\n")
		    comm_list <- append(comm_list, list(s))
	    }
    }
    return (comm_list)
}

