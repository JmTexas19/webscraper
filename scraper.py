# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:37:33 2018

@author: DazedFury
"""
# Here, we're just importing both Beautiful Soup and the Requests library
from bs4 import BeautifulSoup
import cfscrape

# returns a CloudflareScraper instance
scraper = cfscrape.create_scraper()  

#URL and textfile
text_file = open("Output.html", "w", encoding='UTF-8')
completeURL = 'https://boxnovel.com/novel/transcending-the-nine-heavens/chapter-989/'

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
    
    #Get Chapter
    chapter = page_content.find('h2', {'class' : 'text-center'})

    #In case header changes
    if(chapter == None):
        chapter = page_content.find('h3')

    text_file.write('<h3>' + chapter.get_text() + '</h3>')
    print("Writing " + chapter.get_text())
    
    #Get Article
    article = page_content.find('div', {'class' : 'entry-content'})

    #Find and print all text with tag p
    paragraphs = article.find_all('p')
    for i in range(len(paragraphs)):
        text_file.write(str(paragraphs[i]))

    #Find link to next chapter
    nextURLHTML = page_content.find('a', {'class' : 'btn next_page'})
    if(nextURLHTML != None):
        nextURL = nextURLHTML.get('href')
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
        # completeURL = "https://novelplanet.com" + nextURL    
    
    #FORMAT
    text_file.write("<p style=\"page-break-after: always;\">&nbsp;</p>")
    text_file.write("\n\n")
    
#Close Text File
text_file.close()
