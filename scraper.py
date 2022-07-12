# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:37:33 2018

@author: DazedFury
"""
# Here, we're just importing both Beautiful Soup and the Requests library
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cloudscraper

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\\Users\\jmtex\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)

#URL and textfile
text_file = open("Output.html", "w", encoding='UTF-8')
completeURL = 'https://www.lightnovelpub.com/novel/the-regressed-demon-lord-is-kind-11072357/1234-chapter-1'

# Array for storing URL's
URLArray = []

# Login (Optional)
time.sleep(1)
driver.get('https://www.lightnovelpub.com/account/logingoogle')

scraper = cloudscraper.create_scraper()
for cookie in driver.get_cookies():
    c = {cookie['name']: cookie['value']}
    scraper.cookies.update(c)

driver.close()

while(completeURL != None):
    # this is the url that we've already determined is safe and legal to scrape from.
    page_link = completeURL
    
    # here, we fetch the content from the url, using the requests library
    page_response = scraper.get(page_link)
    
    #we use the html parser to parse the url content and store it in a variable.
    page_content = BeautifulSoup(page_response.content, "html.parser")
    page_content.prettify   

    ##################################################################################################
    
    #Get ARTICLE
    article = page_content.find('div', {'id':'chapter-container'})

    #Get CHAPTER
    chapter = page_content.find('span', {'class':'chapter-title'})

    # GET LINK
    nextURL = page_content.find('a', {'class':'nextchap'})

    #Multiple Links
    # for url in nextURL:
    #     if(url.text == 'Next Chapter'):
    #         nextURL = url
    #         break
    
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
        completeURL = "https://www.lightnovelpub.com" + nextURL  
    
    #FORMAT
    text_file.write("<p style=\"page-break-after: always;\">&nbsp;</p>")
    text_file.write("\n\n")
    
#Close Text File
text_file.close()
