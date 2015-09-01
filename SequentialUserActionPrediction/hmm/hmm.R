

forward.backward <- function(y, nhid, q,P,F){
  
  nevents <- length(y)
  alpha <- matrix(nrow=nevents, ncol=nhid)
  beta <- matrix(nrow=nevents, ncol=nhid)
  post <- matrix(nrow=nevents, ncol=nhid)
  
  # initialisation: 
  alpha[1,] <- q * F[,y[1]]
  beta[nevents,] <- rep(1, nhid)
  
  # forward pass:
  for(i in 2:nevents){ 
    alpha[i,] <- (alpha[i-1,] %*% P) * F[,y[i]]
    # normalise for numerical stability:
    alpha[i,] <- alpha[i,]/sum(alpha[i,])
  }
  
  # backward pass:
  for(i in (nevents-1):1){
    beta[i,] <- (beta[i+1,] * F[,y[i+1]]) %*% t(P)
    # normalise for numerical stability:
    beta[i,] <- beta[i,]/sum(beta[i,])
  } 
  
  # eventwise posterior:
  for(i in 1:nevents){ 
    post[i,] <- alpha[i,]*beta[i,] 
    post[i,] <- post[i,]/sum(post[i,]) 
  }
  
  # return:
  post
}

########################################################################

baum.welch <- function(y, nhid, nvis, maxiters=100, tolerance=1e-06){
  
  # parameters:
  P <- matrix(runif(nhid*nhid), nrow=nhid, ncol=nhid) # transition matrix
  F <- matrix(runif(nvis*nhid), nrow=nhid, ncol=nvis) # emission matrix
  P <- P/rowSums(P)
  F <- F/rowSums(F)
  q <- rep(1/nhid, nhid)
  nevents <- length(y)
  
  # main loop:
  for(iter in 1:maxiters){
    
    cat(iter, '\r')
    
    # E-step:
    post <- forward.backward(y, nhid, q,P,F)
    
    # M-step:
    q0 <- 0
    q <- post[1,]
    # P:
    P0 <- P
    P <- matrix(0, nrow=nhid, ncol=nhid)
    for(i in 2:nevents) P <- P + post[i-1,] %*% t(post[i,])
    P <- P/(nevents - 1) # joint distribution
    Pmarg <- colSums(post)
    Pmarg <- Pmarg/sum(Pmarg) # marginals
    for(i in 1:nhid) P[i,] <- P[i,]/Pmarg[i]
    P <- P/rowSums(P)
    # F:
    F0 <- F
    F <- matrix(0, nrow=nhid, ncol=nvis)
    for(i in 1:nevents) F[, y[i]] <- F[, y[i]] + post[i,] 
    F <- F/nevents # joint distribution
    for(i in 1:nhid) F[i,] <- F[i,]/Pmarg[i]
    
    # check for convergence:
    if(sum((P - P0)^2) < tolerance & 
         sum((F - F0)^2) < tolerance &
         sum((q - q0)^2) < tolerance ) break
  }
  
  # BONUS:
  # compute state distributions for the observable values:
  val <- unique(y)
  S <- matrix(0, nrow=max(val), ncol=nhid+2)
  for(v in val){
    dist <- sapply(1:nhid, function(i){ F[i,v]/Pmarg[i] })
    dist <- dist/sum(dist)
    count <- sum(y==v)
    S[v,] <- c(v, count, dist)
  }
  
  # return:
  list(q=q, P=P, F=F, S=S)
}





