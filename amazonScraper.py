from asyncio import WriteTransport
import csv
from inspect import Attribute
from re import U
from random import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions

#used this tutorial for some web scraping basics: https://www.youtube.com/watch?v=HiOtQMcI5wg
#also used this website for basic web scraping fundmentals using BeautifulSoup: https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/



# Web Driver, includes path to chrome web driver executable for chrome 102
driver = webdriver.Chrome('/Users/chrisalhadate/Desktop/CSCI-169/AmazonWebScraper/chromedriver')  

#generate search url
def generateSearchURL(search_string, page):
    template_url = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"
    search_string = search_string.replace(" ","+") #replace all spaces in search_term with +
    baseURL = template_url.format(search_string) #insert newly formatted string into {} in templateURL
    searchURL = baseURL + "&page={}"
    if (page==1): 
        return baseURL
    else: 
        return searchURL.format(page) #insert page # other than into correct portion of searchURL

url = generateSearchURL("4k camera", 1)
driver.get(url) # go to search url on amazon.com



def scapeCardData(card): #Data extraction from each product
    
    a_tag = card.h2.a
    description = a_tag.text.strip() #strip descripton from card
    url = "https://www.amazon.com" + a_tag.get("href") #amazon url + prduct path = prodcut url

    try: #use except from selenium to catch errors if a product does not contain one of the fields
        price_section = card.find("span", "a-price")
        price = price_section.find("span", "a-offscreen").text #extract price text
    except AttributeError: 
        return
    
    try: #use except from selenium to catch errors if a product does not contain one of the fields
        rating = card.i.text #rating info in "i" HTML element
        review_count = card.find("span", {"class": "a-size-base", "dir": "auto"}).text #review count elem
    except AttributeError: #set attributs as empty strings
        rating = ""
        review_count = ""

    #return object containing all scraped fields
    cardData = (description, price, rating, review_count, url) 
    return cardData


#Begin data extraction using BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser") #parse HTML of search url
#find all HTML elems with div={data-component-type: "s-search-result"}
results = soup.find_all("div", {"data-component-type": "s-search-result"}) 
records = [] # will store all data extracted using scrapeCardData

#populate records with item data using ScrapeCardData
for item in results: 
    record = scapeCardData(item)
    if(record): #only append if record isn't empty
        records.append(record)

#write results to CSV file
with open("results.csv", "w", newline="", encoding="utf-8") as fileParams:
    writer = csv.writer(fileParams)
    writer.writerow({"Description:", "Price:", "Rating:", "Review Count:", "Link:"})#write file headings
    for row in records: #write each record on its own row
      writer.writerow(row)
