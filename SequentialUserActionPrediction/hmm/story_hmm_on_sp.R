

#> mean_matrix
#[,1]      [,2]      [,3]      [,4]      [,5]
#[1,] 0.3288140 0.3559048 0.3556190 0.3485714 0.3449524
#[2,] 0.5544931 0.5809524 0.5811429 0.5705714 0.5620952
#[3,] 0.6981590 0.7178095 0.7145714 0.7017143 0.6940000
#> std_matrix
#[,1]      [,2]      [,3]      [,4]      [,5]
#[1,] 0.1459909 0.1475876 0.1489316 0.1341528 0.1374432
#[2,] 0.1971464 0.1939395 0.1995780 0.2054911 0.2100444
#[3,] 0.2062441 0.1909087 0.1982182 0.2043444 0.2072791



source("./hmm.R")

input_file_folder = "../datasets/train_test_sets_size_v6_SP/csv/"
users <- c("pjones", "aaamosbi", "edbrowne", "fdallen", "bird", "keiserjm", "rkavent", "wfszewc", "mikencs", "rkavent", "LAS", "MargaretSilliman", "Sean", "awhairst", "cemcarter", "chris", "richard", "tmadelsp", "tommy", "wmoxbury", "wpobletts")

training_sizes <- c(100, 500, 1000, 1500, 2000)

test_repeat <- 5
rm_query_in_predicted_apps <- FALSE

mean_matrix <- matrix(c(0), nrow=3, ncol=length(training_sizes))
std_matrix <- matrix(c(0), nrow=3, ncol=length(training_sizes))

day_i = 0

for(training_size in training_sizes)
{
  print(training_size)
  day_i = day_i + 1
  test_results_accuracy <- matrix(c(0), nrow=3, ncol=(test_repeat*length(users)))
  result_i = 0
  
  for(user in users)
  {
    print(user)
    for(test_i in 1:test_repeat)
    {
      result_i = result_i + 1
      
      file = paste(input_file_folder, training_size, "/", user, "-", test_i, ".csv", sep="")
      #print(file)
      
      top_accuracy = matrix(c(0), nrow=3, ncol=1)
      
      dat_orgin <- read.csv(file, header=TRUE)
      dat_orgin[,2] <- user
      attach(dat_orgin)
      
      len_train = as.numeric(strsplit(colnames(dat_orgin)[1], "X")[[1]][2])
      len_test = as.numeric(strsplit(colnames(dat_orgin)[2], "X")[[1]][2])
      #cat("len_train =", len_train, ", len_test =", len_test, "\n")
      
      colnames(dat_orgin) <- c("AppName", "UserId")
      dat <- dat_orgin
      
      detach(dat_orgin)
      attach(dat)
      
      # eyeball the data:
      head(dat)
      sort( table(AppName) )
      table(UserId)
      
      # define observations to model:
      cond <- (UserId==user)
      ( obs <- as.character(AppName[cond]) )
      symbols <- unique(obs)
      y <- sapply(obs, function(str){ which(symbols==str) })
      ( nvis <- length(symbols) ) # visible states
      
      
      #######################################################
      # 2. SWEET POTATO data
      
      # N.B. GO BACK AND CHECK y IS CORRECTLY DEFINED...
      
      # define the state space:
      nhid <- 4
      states <- as.character(1:nhid)
      
      # run Baum-Welch on the first 'init' events:
      #init <- 11000
      init <- len_train
      param <- baum.welch(y[1:init], nhid, nvis, maxiters=500)
      q <- param$q # q = initial state prior
      P <- param$P # P = transition probabilities
      F <- param$F # F = emission probabilities
      S <- param$S # S = marginal state distribution for each symbol
      
      # state posteriors under this model:
      post <- forward.backward(y[1:init], nhid, q,P,F)
      
      # visualise:
      #range <- 900:1000
      #mosaicplot(post[range,], color=1:nhid, main=user)
      # for(i in range) cat(i,':', sprintf("%s",obs[i]),'\n')
      #plot(post[range,1], type='n')
      #for(i in 1:nhid) points(post[range,i], type='l', col=i)
      
      # let's try to interpret the states...
      #app.dat <- data.frame(S)
      #app.dat[,1] <- sapply(S[,1], function(i){ as.character(symbols[i]) })
      #names(app.dat) <- c("app","freq",
      #                    sapply(1:nhid, function(i){ sprintf("s%d",i) }))
      #attach(app.dat)
      
      # eyeball the app groups:
      #cond <- (freq>10) 
      #for(i in 1:nhid) app.dat[,i+2] <- round(app.dat[,i+2], 3)
      #app.dat[cond,][order(s1[cond]),]
      
      #detach(app.dat)
      
      ########################################################################
      # 3. Prediction using the fitted HMM
      
      k <- len_test
      p <- post[init,]
      for(i in (init+1):(init+k)){
        
        query_app <- attributes(y[(i-1)])[[1]]
        target_app <- attributes(y[i])[[1]]
        
        # this state prior:
        p <- t(P) %*% p; p <- p/sum(p) 
        # predicted distribution at time i:
        v <- t(F) %*% p 
        
        # Find top 4
        predicted_apps <- c(0,0,0,0)
        for(j in 1:4)
        {
          max_p <- max(v)
          max_i <- match(max_p, v)
          predicted_apps[j] <- symbols[max_i]
          v[max_i] <- -1
        }
        
        #print(predicted_apps)
        
        if(rm_query_in_predicted_apps == TRUE)
        {
          query_app_i <- match(query_app, predicted_apps)
          if(is.na(query_app_i) != TRUE)
          {
            predicted_apps <- predicted_apps[(-query_app_i)]
          }
        }
        
        #print(query_app)
        #print(target_app)
        #print(predicted_apps)
        
        top1 = predicted_apps[1]
        top2 = predicted_apps[2]
        top3 = predicted_apps[3]
        
        if(top1 == target_app)
        {
          top_accuracy[1,1] = top_accuracy[1,1] + 1
          top_accuracy[2,1] = top_accuracy[2,1] + 1
          top_accuracy[3,1] = top_accuracy[3,1] + 1
        }
        else if(top2 == target_app)
        {
          top_accuracy[2,1] = top_accuracy[2,1] + 1
          top_accuracy[3,1] = top_accuracy[3,1] + 1
        }
        else if(top3 == target_app)
        {
          top_accuracy[3,1] = top_accuracy[3,1] + 1
        }
        
        
        
        
        
        #col <- rep("black", length(v)); col[y[i]]<-"red"
        #plot(v, type='h', col=col, ylab="", 
        #     xlab="Application",
        #     main=sprintf("%s: prediction %d", user, i - init))
        
        # skip if y[i] not seen before:
        #if(sum(F[,y[i]])==0) break
        
        # this state posterior:
        #p <- F[,y[i]] * p; p <- p/sum(p)
      }
      
      detach(dat)
      
      top_accuracy = top_accuracy / len_test
  
      test_results_accuracy[,result_i] = top_accuracy[,1]
      
    }
  }
  
  # Means
  mean_matrix[1,day_i] = mean(test_results_accuracy[1,])
  mean_matrix[2,day_i] = mean(test_results_accuracy[2,])
  mean_matrix[3,day_i] = mean(test_results_accuracy[3,])
  
  #Standard Deviations
  std_matrix[1,day_i] = sd(test_results_accuracy[1,])
  std_matrix[2,day_i] = sd(test_results_accuracy[2,])
  std_matrix[3,day_i] = sd(test_results_accuracy[3,])
  
  #print(training_size)
  print(mean_matrix)
}