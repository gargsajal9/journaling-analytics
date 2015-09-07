#!/bin/bash

cd corpus-diffbot

for file in `ls`
do 
  cat $file | jq '.objects[].text' >> ../corpus-diffbot-text/$file
  cat $file | jq '.objects[].discussion.posts[].text' >> ../corpus-diffbot-text/$file
done
