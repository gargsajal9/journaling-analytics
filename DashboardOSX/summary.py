from textteaser import TextTeaser
import requests
import subprocess32
import re
import os

# We use the LexRank algorithm, described here:
# http://www.jair.org/media/1523/live-1523-2354-jair.pdf

tt=TextTeaser()

TIKA_FILENAME='tika-app-1.11.jar'

def getSummary(filename,count):
	response={}
	text=getFileContents(filename)
	if text is None:
		response['summary']=["Summarization of this file type is not yet supported"]
		return response
	result = tt.summarize(title="dummy title just to check how this affects",text=text,count=count)
	response['summary']=result
	return response

def getFileContents(filename):
	#if filename.endswith(".txt"):
	#	with open(filename) as file:
	#		content = file.readlines()
	if filename.split(".")[-1] in ("doc","docx","pdf","ppt","pptx","txt"):
		content=subprocess32.check_output(["java","-jar",TIKA_FILENAME,"-t",filename])
	else:
		return None
	#print content
	#content = [c.replace('\n', '') for c in content if c != '\n']
	#content = " ".join(content)
	#print content
	#print
	content = re.sub(r'[^\x00-\x7F]+',' ', content)
	content = content.decode("ascii", "ignore")
	content = " ".join(content.replace("\n", " ").split())
	#print content
	return content

def downloadTika():
	if os.path.isfile(TIKA_FILENAME):
		return
	else:
		print "Downloading Apache Tika......."
		tikaURL = 'http://apache.claz.org/tika/'+TIKA_FILENAME
		subprocess32.call(['wget',tikaURL])
		if not os.path.isfile(TIKA_FILENAME):
			print "Failed to download Tika. Exiting"
			exit()
		return

if __name__=="__main__":
	#for sent in getSummary("DataManagerhints.pdf",8)['summary']:
	for sent in getSummary("sample.txt",8)['summary']:
		print sent
		print
