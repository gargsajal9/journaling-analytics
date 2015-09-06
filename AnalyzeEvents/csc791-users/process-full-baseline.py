# Simple analysis script for CSC791 journaling event data
# Calculates full baseline for dumb (assume no change) goal
# detection at various time in the future.
# Possible we don't care about this too much - will be impossible
# to guess accurately too far in the future but is needed
# for a fairer baseline (next event is 'too easy').

# Paul Jones August 9th, 2015

from __future__ import division
import csv

# Function to calculate F1 score given two lists
def F1_score(tags,predicted):

        #print tags
        #print predicted 

	#tags=set(tags)
	#predicted=set(predicted)

    	#tp = len(tags & predicted) # this doesn't work elementwise
        tp = len([i for i, j in zip(tags,predicted) if ((i == 1) & (j == 1))]) # Elementwise comparison preserving order
	fp = len([i for i, j in zip(tags,predicted) if ((i == 0) & (j == 1))])
	tn = len([i for i, j in zip(tags,predicted) if ((i == 0) & (j == 0))])
	fn = len([i for i, j in zip(tags,predicted) if ((i == 1) & (j == 0))])
	
	#fp = len(predicted) - tp 
	#fn = len(tags) - tp

	print "tp=%d, fp=%d, tn=%d, fn=%d, " % (tp, fp, tn, fn),

    	if (tp==0 & fp==0):
		precision=float(0)
	else:
       		precision=float(tp)/(tp+fp)
       	
	recall=float(tp)/(tp+fn)
	accuracy=float(tp+tn)/(tp+tn+fp+fn)
        #f1=2*((precision*recall)/(precision+recall))
	beta=1.00

	if ((precision<0.001) & (recall<0.001)):
		fbeta=float(0)
	else:
        	fbeta=(1+(beta*beta))*((precision*recall)/(((beta*beta)*precision)+recall))
   
	print "precision=%f, recall=%f, %f, beta=%f, " % (precision, recall, accuracy, beta),
        return fbeta

# Calculate prediction accuracy with many different values of ts_future
# 0s, 1s, 10s, 100s, 1000s (20 mins), 10000s (3 hours), 100000s (1 day), 1000000s (10 days)
for ts_future in [0,1000,10000,100000,1000000,10000000,100000000,1000000000]:

	# Initialize counters
	total_right=0
	total_wrong=0
	total_samefile=0
	total_difffile=0
	total_accuracy=0

	# Top 9 users with the most data (>500 events)
	users = ['cmoon2','drmedd','kbansal','pjones','pmahish','sdharenb','mschaudh','shsu3','smransho']

	# Iterate over users list
	for user in users:

		with open(user+".csv", "r") as f:

			times = []
			users = []
			goals = []
			files = []

			reader = csv.reader(f, delimiter='\t')

			for event in reader:
				times.append(int(event[0]))
				users.append(event[1])
				goals.append(event[2])
				files.append(event[3])

			# Baseline prediction - use current goal to predict next goal
			# - iterate over time list: find first event after ts_future has elapsed
			# - has file changed? if so, has the goal also changed?
			# - if yes, prediction would have been wrong; if not, prediction was right
			# - if file hasn't changed, go to next event after ts_future

			right=0;
			wrong=0;
			samefile=0;
			difffile=0;

			# Iterate over all events for that user, not just the first!
			# Index i is the start event; j is the next event after ts_future
			for i, start_ts in enumerate(times):
				for j, ts in enumerate(times[i::]): # only from index i to the end
					if (ts-start_ts)>ts_future: # ts_future has elapsed
						if files[j+i] != files[i]: # File has changed
							difffile=difffile+1
							if goals[j+i] != goals[i]: # Goal has also changed
								wrong=wrong+1
								break	# Break out of for loop (go to next event for this user and ts_future)
							else:
								right=right+1
								break
						else:
							samefile=samefile+1 # and go back round the for loop

		# End processing file for this user
		if (right==0 & wrong==0):
			accuracy=0
		else:
			accuracy=right/(right+wrong) # Accuracy for this user

		print "User=%s, Right=%d, Wrong=%d, Accuracy=%f, Samefile=%d, DiffFile=%d" % (user,right,wrong,accuracy,samefile,difffile)

		# Accumulate totals before moving to next user
		total_right=total_right+right
		total_wrong=total_wrong+wrong
		total_samefile=total_samefile+samefile
		total_difffile=total_difffile+difffile
		total_accuracy=total_accuracy+accuracy

	# End processing users for this ts_future
	overall_accuracy=total_right/(total_right+total_wrong)
	#print "TotalRight=%d, TotalWrong=%d, OverallAccuracy=%f, TotalSameFile=%d, TotalDiffFile=%d" % (total_right, total_wrong, total_accuracy, total_samefile, total_difffile)

	print "ts_future=%fs, overall_accuracy=%f, average_accuracy=%f" % (ts_future/1000, overall_accuracy, total_accuracy/9)
	print "----"
