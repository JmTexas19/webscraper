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
text_file = open("Output.txt", "w", encoding='UTF-8')
completeURL = 'https://novelplanet.com/Novel/To-Be-a-Power-in-the-Shadows/c1-5?id=332838'

while(completeURL != None):
    # this is the url that we've already determined is safe and legal to scrape from.
    page_link = completeURL
    
    # here, we fetch the content from the url, using the requests library
    page_response = scraper.get(page_link)
    
    #we use the html parser to parse the url content and store it in a variable.
    page_content = BeautifulSoup(page_response.content, "html.parser")
    page_content.prettify    
    
    #Get Chapter
    chapter = page_content.find('h4').get_text()
    text_file.write(chapter + "\n")
    print("Writing " + chapter)
    
    #Find and print all text with tag p
    paragraphs = page_content.find_all('p')
    for i in range(len(paragraphs)):
        text_file.write(paragraphs[i].get_text())

    #Find link to next chapter
    partURLArr = page_content.find_all('a', {'class' : 'button small'})
    for i in range(len(partURLArr)):
        if(i == len(partURLArr) - 1):
            partURL = partURLArr[i].get('href')
    
    completeURL = "https://novelplanet.com" + partURL
    
    #FORMAT
    print("\n\n")
    
#Close Text File
text_file.close()


