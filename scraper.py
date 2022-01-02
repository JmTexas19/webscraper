# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:37:33 2018

@author: DazedFury
"""
# Here, we're just importing both Beautiful Soup and the Requests library
from typing import List
from bs4 import BeautifulSoup
import cfscrape
import cloudscraper
import time

# returns a CloudflareScraper instance
scraper = cloudscraper.create_scraper()  

#URL and textfile
text_file = open("Output.html", "w", encoding='UTF-8')
completeURL = 'https://hostednovel.com/17321/novel/legend-of-the-great-sage/lgs-chapter-1'

# Array for storing URL's
URLArray = []

while(completeURL != None):
    # this is the url that we've already determined is safe and legal to scrape from.
    page_link = completeURL
    
    # here, we fetch the content from the url, using the requests library
    page_response = scraper.get(page_link)
    
    #we use the html parser to parse the url content and store it in a variable.
    page_content = BeautifulSoup(page_response.content, "html.parser")
    page_content.prettify    

    #If delay is necessary
    while(page_content.find('h1', text='Too Many Requests') is not None):
        time.sleep(5) 
        # this is the url that we've already determined is safe and legal to scrape from.
        page_link = completeURL
        
        # here, we fetch the content from the url, using the requests library
        page_response = scraper.get(page_link)
        
        #we use the html parser to parse the url content and store it in a variable.
        page_content = BeautifulSoup(page_response.content, "html.parser")
        page_content.prettify   

    ##################################################################################################
    
    #Get ARTICLEl
    article = page_content.find('div', {'id' : 'chapter'})

    #Get CHAPTER
    chapter = page_content.find('h1', {'class' : 'mb-4'})

    # GET LINK
    nextURL = page_content.find_all('a')

    #Multiple Links
    for url in nextURL:
        if('Next' in url.text):
            nextURL = url
            break
        else:
            nextURL = ''
    
    ##################################################################################################

    #Write Chapter
    text_file.write('<h1>' + chapter.get_text() + '</h1>')
    print("Writing: " + chapter.get_text())

    #--[Optional] In case header changes
    #if(chapter == None):
    #   chapter = page_content.find('h3')
    #text_file.write('<h3>' + chapter.get_text() + '</h3>')
    #print("Writing " + chapter.get_text())
    #--
    
    #Write Article
    text_file.write(str(article))

    #Next Link
    if(nextURL != None):
        nextURL = nextURL.get('href')
    else:
        #No Chapters left... Break. :(
        break

    # Not Necessary unless multiple buttons.
    #partURLArr = page_content.find_all('a', {'class' : 'btn next_page'})
    #for i in range(len(partURLArr)):
    #    if(i == len(partURLArr) - 1):
    #        partURL = partURLArr[i].get('href')
            
    #Add partURL to array for tracking
    if(nextURL in URLArray):
        completeURL = None 
    else:
        URLArray.append(nextURL)
        completeURL = nextURL

        #If nextURL is only half of what you need.
        #completeURL = "https://rainingtl.org" + nextURL  
    
    #FORMAT
    text_file.write("<p style=\"page-break-after: always;\">&nbsp;</p>")
    text_file.write("\n\n")
    
#Close Text File
text_file.close()
