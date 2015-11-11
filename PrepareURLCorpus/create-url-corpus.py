#----------------------------------
# Script to create a corpus of text
# files from URLs using Diffbot,
# jusText and newspaper.
# PJ/SL August 14, 2015
#-----------------------------------

# For exceptions and sleep
import sys
import time

# For newspaper
from newspaper import Article
from urlparse import urlparse
#from newspaper import fulltext

# For justext
import urllib2
import justext

# For diffbot
import diffbot
from json import dumps

# --------------------
# Process with diffbot
# --------------------

#with open('urls-test.txt','r') as urls:
with open('urls.txt','r') as urls:
        for url in urls:
                try:
                        print "---> Processing URL with diffbot: ", url
			parsedurl=urlparse(url)
                        domain=parsedurl.netloc
                        newpath=parsedurl.path.replace('/','_').strip()
                        #filename="corpus-test-diffbot/"+domain+newpath+".txt"
                        filename="corpus-diffbot/"+domain+newpath+".txt"
                        file = open(filename, "w")
    			#json_result = dumps(diffbot.article(url, token='f3472e9233ba4070833dfffb0fb97660'))
    			json_result = dumps(diffbot.article(url, token='bcc855fd71b859791b2202d8297da1e3')) # new LAS token 11/2015
			file.write(json_result)
    			outfile.close()
		except:
                        print "**** ERROR processing URL with diffbot: ", url, sys.exc_info()[0]
		time.sleep(1)
'''
# --------------------
# Process with jusText
# --------------------
#with open('urls-test.txt','r') as urls:
with open('urls.txt','r') as urls:
        for url in urls:
                try:
			print "---> Processing URL with jusText: ", url
			page = urllib2.urlopen(url).read()
			parsedurl=urlparse(url)
                        domain=parsedurl.netloc
                        newpath=parsedurl.path.replace('/','_').strip()
                        #filename="corpus-test-justext/"+domain+newpath+".txt"
                        filename="corpus-justext/"+domain+newpath+".txt"
			file = open(filename, "w")
			paragraphs = justext.justext(page, justext.get_stoplist('English'))
			for paragraph in paragraphs:
#    				if paragraph['class'] == 'good':
        				file.write(paragraph.text+" ")
			file.close()
		except:
                        print "**** ERROR processing URL with jusText: ", url, sys.exc_info()[0]

# ----------------------
# Process with newspaper
# ----------------------
with open('urls.txt','r') as urls:
	for url in urls:
    		try:
			#url = urls.readline().strip()
			print "---> Processing URL: ", url
    			article=Article(url)
    			article.download()
    			article.parse()
    			#article.nlp()

        		# Create a suitable output filename and write to the file
			parsedurl=urlparse(url)
			domain=parsedurl.netloc
			newpath=parsedurl.path.replace('/','_').strip()
			filename="corpus-newspaper/"+domain+newpath+".txt"
			file = open(filename, "w")
			file.write(article.text)
			file.close()
    			#print article.authors
    			#print article.publish_date
    			print article.text
    		except:
			print "**** ERROR processing URL: ", url

    #print article.keywords
    #print article.summary
    #print article.movies
    #print article.top_image
    #html=request.get(...).text
    #text=fulltext(html)
'''
