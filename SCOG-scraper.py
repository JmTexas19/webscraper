# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:37:33 2018

@author: DazedFury
"""
# Here, we're just importing both Beautiful Soup and the Requests library
from bs4 import BeautifulSoup
import cfscrape
import cloudscraper

# returns a CloudflareScraper instance
scraper = cloudscraper.create_scraper() 

#URL and textfile
text_file = open("Output.html", "w", encoding='UTF-8')
completeURL = 'https://www.wuxiaworld.com/novel/the-second-coming-of-gluttony/scog-chapter-1'

#Array for storing URL's
URLArray = []

while(completeURL != None):
    # this is the url that we've already determined is safe and legal to scrape from.
    page_link = completeURL
    
    # here, we fetch the content from the url, using the requests library
    page_response = scraper.get(page_link)
    
    #we use the html parser to parse the url content and store it in a variable.
    page_content = BeautifulSoup(page_response.content, "html.parser")
    page_content.prettify    

    #ARTICLE
    article = page_content.find('div', {'class' : 'section'})
    
    #HEADER
    #Get Block Header is in
    caption = page_content.find('div', {'class' : 'caption clearfix'})
    #Get Chapter
    chapter = caption.find('h4', {'class' : ''})
    text_file.write(str(chapter))

    #Get Chapter From URL
    #chapter = completeURL[63:len(completeURL)
    #text_file.write('<h4>' + chapter + '</h4>')

    print("Writing " + str(chapter))

    #No <p>
    #text_file.write(str(article))

    #Find and print all text with tag p
    paragraphs = article.find_all('p')
    for i in range(len(paragraphs)):
        text_file.write(str(paragraphs[i]))

    #Find link to next chapter
    # nextURLHTML = page_content.find('a', {'class' : 'btn btn-link'})
    # if(nextURLHTML != None):
    #     nextURL = nextURLHTML.get('href')
    # else:
    #     #No Chapters left... Break. :(
    #     break
    

    # Not Necessary unless multiple buttons.
    nextURLArr = page_content.find_all('a', {'class' : 'btn btn-link'})
    for i in range(len(nextURLArr)):
        if(i == len(nextURLArr) - 1):
            nextURL = nextURLArr[i].get('href')
            
    #Add partURL to array for tracking
    if(nextURL in URLArray):
        completeURL = None
    else:
        URLArray.append(nextURL)
        completeURL = nextURL

        #If nextURL is only half of what you need.
        completeURL = "https://www.wuxiaworld.com" + nextURL    
    
    #FORMAT
    text_file.write("<p style=\"page-break-after: always;\">&nbsp;</p>")
    text_file.write("\n\n")

#Close Text File
text_file.close()
