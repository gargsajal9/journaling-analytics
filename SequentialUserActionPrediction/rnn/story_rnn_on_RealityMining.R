
#> mean_matrix
#[,1]      [,2]      [,3]      [,4]      [,5]
#[1,] 0.4648571 0.5024286 0.5161667 0.5176429 0.5204286
#[2,] 0.6435000 0.6865952 0.6972619 0.7007143 0.7019762
#[3,] 0.7423095 0.7854286 0.7944762 0.7978333 0.7970000
#> std_matrix
#[,1]       [,2]       [,3]       [,4]       [,5]
#[1,] 0.1080384 0.09632288 0.09273526 0.09113402 0.09353981
#[2,] 0.1213523 0.09877569 0.09584135 0.09342062 0.09787064
#[3,] 0.1195702 0.09737636 0.09143492 0.09130881 0.09781162


library(RSNNS)



#######################################################
# 0. Statement of the problem



options(warn=-1)

input_file_folder = "../datasets/train_test_sets_size_v6_RM/csv/"
#users <- c('25', '20', '21', '22', '23', '4', '8', '57', '53', '52', '81', '102', '100', '38', '36', '67', '93', '12', '49', '40', '41', '75', '70')
users <- c('25', '26', '27', '20', '21', '22', '23', '28', '4', '8', '58', '55', '54', '57', '56', '51', '50', '53', '52', '89', '82', '83', '81', '86', '87', '84', '85', '102', '100', '101', '106', '39', '38', '33', '32', '31', '30', '37', '36', '35', '34', '60', '61', '62', '63', '64', '65', '67', '68', '69', '6', '99', '91', '90', '93', '94', '97', '96', '11', '10', '13', '12', '15', '17', '16', '19', '18', '49', '46', '44', '42', '40', '41', '5', '9', '77', '76', '75', '74', '73', '71', '70', '79', '78')
  
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
    #print(training_size)
    print(user)
    for(test_i in 1:test_repeat)
    {
      result_i = result_i + 1
      
      file = paste(input_file_folder, training_size, "/", user, "-", test_i, ".csv", sep="")
      #print(file)
      
      #outputfile <- paste("/Users/shitiansshen/Documents/NCSU/LAS/result/RNN/RNN-output-",user,"-",test_i,".txt",sep="")
      #outputfile <- paste("./",user,"-",test_i,".txt",sep="")
      #file.create(outputfile)
      
      top_accuracy = matrix(c(0), nrow=3, ncol=1)
      
      #file <- "./SP_events.csv"
      #file <- "./train_30d_test_7d_sets/csv_userid_app_time/pjones-1.csv"
      dat_orgin <- read.csv(file, header=TRUE)
      dat_orgin[,2] <- user
      #dat <- dat[,-3]
      #print(dat)
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
      
      
      
      #plot(spinglass.community(g), g, main=user)
      
      # PROBLEM: to what extent can we predict a users' movement in app/domain-space?
      # PREVIEW PLOTS...
      
      
      ########################################################################
      # 4. RNNs instead of HMMs
      
      range <- 1:(len_train - 1)
      n <- len_test - 1
      test <- (len_train):(len_train+len_test-1)
      range_test <-1:len_test
      
      # training data:
      x.train <- obs[range]
      y.train <- obs[range + 1]
      features.train <- decodeClassLabels(c(x.train, symbols))[range,]
      targets.train <- decodeClassLabels(c(y.train, symbols))[range,]
      
      # test sequence:
      x.test <- obs[test]
      y.test <- obs[test + 1]
      features.test <- decodeClassLabels(c(x.test, symbols))[range_test,]
      targets.test <- decodeClassLabels(c(y.test, symbols))[range_test,]
      target_app_index <- attributes(targets.test)[[2]][2]
      target_app_index <- target_app_index[[1]]
      
      # fit model (choose number of hidden units):
      nhidden <- 4
      model <- elman(features.train, 
                     targets.train, 
                     size= c(nhidden), 
                     learnFuncParams=c(0.1), 
                     maxit=500,
                     linOut=FALSE)
      #plotIterativeError(model)
      
      predictions <- predict(model, features.test)
      predictions <- predictions/rowSums(predictions)
      
      num_query_apps <- dim(predictions)[1]
      
      for(i in 1:num_query_apps){
        #print(file)
        #print(i)
        v <- predictions[i,]
        #j <- which(targets.test[i,]==1)
        #print(j)
        query_app = x.test[i]
        target_app = y.test[i]
        #print(query_app)
        #print(target_app)
        
        order = order(predictions[i,],decreasing=TRUE)
        #cat("Target App =", symbols[j], "\n")
        #cat("Top1 =", symbols[order[1]], "\n")
        #cat("Top2 =", symbols[order[2]], "\n")
        #cat("Top3 =", symbols[order[3]], "\n")
        
        #match("Safari", target_app_index)
        
        #output_order <- order[1:6]
        predicted_apps <- target_app_index[order]
        query_app_i <- match(query_app, predicted_apps)
        
        #predicted_apps <- symbols[output_order]
        #if(i==1)
        #{
        #  previous_app <- symbols[which(targets.train[(len_train),]==1)]
        #}
        #else{
        #  previous_app <- symbols[which(targets.test[(i-1),]==1)]
        #}
        
        # check wether the predicted app is the same as the previous one
        #for(m in (1:length(predicted_apps))){
        #  if(predicted_apps[m] == previous_app){
        #    predicted_apps <- predicted_apps[-m]
        #    break
        #  }
        #}
        
        # store prediction in to txt file, top-5
        #predicted_apps <- predicted_apps[1:5]
        
        
        # Remove query app in the predicted apps for Sweet Potato prediction
        if(rm_query_in_predicted_apps == TRUE)
        {
          predicted_apps = predicted_apps[(-query_app_i)]
        }
        
        
        #print(predicted_apps)
        
        #cat(predicted_apps, file=outputfile,sep=",", append=TRUE);
        #cat("\n", file=outputfile, append=TRUE);
        
        #target_app = target_app_index[j]
        #print(target_app)
        top1 = predicted_apps[1]
        top2 = predicted_apps[2]
        top3 = predicted_apps[3]
        
        if((top1 == target_app) && (is.na(top1) == FALSE) && (is.na(target_app) == FALSE))
        {
          top_accuracy[1,1] = top_accuracy[1,1] + 1
          top_accuracy[2,1] = top_accuracy[2,1] + 1
          top_accuracy[3,1] = top_accuracy[3,1] + 1
        }
        else if((top2 == target_app) && (is.na(top2) == FALSE) && (is.na(target_app) == FALSE))
        {
          top_accuracy[2,1] = top_accuracy[2,1] + 1
          top_accuracy[3,1] = top_accuracy[3,1] + 1
        }
        else if((top3 == target_app) && (is.na(top3) == FALSE) && (is.na(target_app) == FALSE))
        {
          top_accuracy[3,1] = top_accuracy[3,1] + 1
        }
        
        
        #col <- rep("black", length(v)); col[j] <-"red"
        #plot(v, type='h', col=col, ylab="", 
        #   xlab="Application",
        #   main=sprintf("%s: prediction %d", user, i))
      }
      
      detach(dat)
      
      #print(top_accuracy)
      top_accuracy = top_accuracy / num_query_apps
      #print(top_accuracy)
      
      #print(top_accuracy)
      test_results_accuracy[,result_i] = top_accuracy[,1]
      #print(test_results_accuracy[,result_i])
      #print(test_results_accuracy)
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


