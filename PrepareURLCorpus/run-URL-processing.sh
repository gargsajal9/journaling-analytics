#!/bin/bash
# PJ 2015/11/29

# *** CLEAR THESE DIRECTORIES AND CREATE urls.txt BEFORE RUNNING THIS SCRIPT ***

mkdir corpus-diffbot
mkdir corpus-diffbot-text
mkdir corpus-diffbot-text-1000

# Run Diffbot on urls.txt
echo "*** Creating URL content corpus using Diffbot ***"
python ./create-url-corpus.py

# Extract text from the extracted webpages with JSON parsing
echo "*** Extracting text content from corpus ***"
./extract-text-from-corpus.sh

# Filter for those with >1k of content
echo "*** Filtering for >1k of content ***"
cd corpus-diffbot-text; minsize=1000; pass=0; for file in `ls`; do filesize=$(wc -c <${file}); if [ $filesize -ge $minsize ]; then pass=$((pass+1)); cp $file ../corpus-diffbot-text-1000/; fi; done; echo $pass

# Create a list of URLs in the final corpus for RShiny
ls corpus-diffbot-text-1000 > urls-in-corpus.csv
