#!/bin/bash
# Generate event corpus for PS598
# PJ 2015-11-29

# Download all events from skylr (for PS598)
curl -H "Content-Type: application/json" -H "AuthToken: 79e0eb5ad4c0a4ceff6889dc6e8fd3ec188219db7a8a7e63d04a0730c2f9f0c9" -d '{"type":"find","query":{"data.ProjId":"journaling-chrome"}}' https://las-skylr-dev-token.oscar.ncsu.edu/api/data/document/query > tmp-chrome-all

# For simple formatted output (one record per line) and filtered for PS598 users
cat tmp-chrome-all | jq -c . | sed -e 's/},{/}\n{/g' | egrep -f ps598-users/USERS > tmp-chrome-ps598

# Summary of PS598 domains
#less tmp-chrome-all | jq -c . | sed -e 's/},{/}\n{/g' | egrep -f ps598-users/USERS | jq '.data.WebURL' | cut -d'/' -f3 | sed -e 's/www.//' | sed -e 's/\"//g' | sort | uniq -c | sort -nr |  less

# Summary of prompting options
# less tmp-chrome-all | jq -c . | sed -e 's/},{/}\n{/g' | egrep -f ps598-users/USERS | jq '.data.TriggerOptions.page_time.time_on_page' | sort | uniq -c | sort -nr | less

# Extract JSON fields we care about using jq
cat tmp-chrome-ps598 | jq '.data.EvtTime' -c > tmp-chrome-EvtTime.txt
cat tmp-chrome-ps598 | jq '.data.UserId' -c > tmp-chrome-UserId.txt
cat tmp-chrome-ps598 | jq '.data.TaskName' -c | sed -e 's/,/_/g' > tmp-chrome-TaskName.txt
cat tmp-chrome-ps598 | jq '.data.WebURL' -c > tmp-chrome-WebURL.txt

# For future - when goal options are available in production
#cat tmp-chrome-all | jq '.data[].data.Trigger' -c | sort | uniq
#cat tmp-chrome-all | jq '.data[].data.GoalPicked' -c | sort | uniq

# Rejoin in a single csv file and sort by time
# Can also paste using a tab character here!
paste -d, tmp-chrome-EvtTime.txt tmp-chrome-UserId.txt tmp-chrome-TaskName.txt tmp-chrome-WebURL.txt | sed -e 's/\"//g' > tmp-chrome-ps598-joined.csv

cat tmp-chrome-ps598-joined.csv | grep -vi irrelevant > tmp-chrome-ps598-joined-relevant.csv

# Make TaskName field consistent
#cat tmp-all-sorted.csv | sed -e 's/))((/_/g' | sed -e 's/((//' | sed -e 's/))//' | sed -e 's/,/_/g' | sed -e 's/\[//' | sed -e 's/\]//' | sed -e 's/pjones_//' > tmp-all-sorted-cleaned.csv

# Summarize user events by prompting options group
#cat tmp-chrome-ps598-joined.csv | egrep -f ps598-users/USERS-70s | grep -vi null | cut -d',' -f2 | sort | uniq -c | sort -nr
#cat tmp-chrome-ps598-joined.csv | egrep -f ps598-users/USERS-70s-50 | grep -vi null | cut -d',' -f2 | sort | uniq -c | sort -nr

# Separate components to create dictionaries
cat tmp-chrome-ps598-joined-relevant.csv | cut -d',' -f3 | cut -d'_' -f2 > tmp-http-only-stage.csv
cat tmp-chrome-ps598-joined-relevant.csv | cut -d',' -f3 | cut -d'_' -f3 | sed -e 's/\]//' > tmp-http-only-subtask.csv
cat tmp-chrome-ps598-joined-relevant.csv | cut -d',' -f4 > tmp-http-only-url.csv
# Extra group category for PS598 class
cat tmp-chrome-ps598-joined-relevant.csv | cut -d',' -f2 | sed -e 's/marosema/ISIS/' | sed -e 's/hfpardue/DRONES/' | sed -e 's/kcnoonan/IRAN/' | sed -e 's/cmmaris/ISIS/' | sed -e 's/dakrantz/ISIS/' | sed -e 's/mhall/IRAN/' | sed -e 's/lsgreen3/IRAN/' | sed -e 's/ajgoswic/DRONES/' | sed -e 's/djgedmin/DRONES/' | sed -e 's/dlflemin/DRONES/' > tmp-http-only-group.csv

# Recombine with URLs
paste -d',' tmp-http-only-url.csv tmp-http-only-stage.csv | sort | uniq > tmp-http-url-stage.csv
paste -d',' tmp-http-only-url.csv tmp-http-only-subtask.csv | sort | uniq > tmp-http-url-subtask.csv
paste -d',' tmp-http-only-url.csv tmp-http-only-group.csv | sort | uniq > tmp-http-url-group.csv

# Create list of URLs for running through Diffbot
cat tmp-http-only-url.csv | sort | uniq > tmp-urls-ps598-relevant.txt

# NOW NEED TO RUN run-URL-processing.sh IN PrepareURLCorpus TO CREATE urls-in-corpus.csv DICTIONARY!

# Create final dictionaries
#cat tmp-http-url-stage.csv | sed -e 's/\//_/g' | sed -e 's/\,/\.txt,/' | sed -e 's/http:__//' | sed -e 's/https:__//' | egrep -f ../PrepareURLCorpus/urls-in-corpus.csv > tmp-http-url-stage-dict.csv
#cat tmp-http-url-subtask.csv | sed -e 's/\//_/g' | sed -e 's/\,/\.txt,/' | sed -e 's/http:__//' | sed -e 's/https:__//' | egrep -f ../PrepareURLCorpus/urls-in-corpus.csv > tmp-http-url-subtask-dict.csv
#cat tmp-http-url-group.csv | sed -e 's/\//_/g' | sed -e 's/\,/\.txt,/' | sed -e 's/http:__//' | sed -e 's/https:__//' | egrep -f ../PrepareURLCorpus/urls-in-corpus.csv > tmp-http-url-group-dict.csv

