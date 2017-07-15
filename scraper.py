import requests
from bs4 import BeautifulSoup
import yagmail
import time


# Scraper Settings
area = "vancouver"
subArea = "rch"
baseUrl = "https://" + area + ".craigslist.ca"

#users
users = [{"name": "Mohamed", "email": "mohamed.ali@alumni.ubc.ca"},
         {"name": "Nabila", "email": "nabila_emam1234@yahoo.com"},
         {"name": "Hassanein", "email": "hassanin79@hotmail.com"}]
yag = yagmail.SMTP('mohammedali.saisdubai@gmail.com', '16julyfriday')


def generateHtmlForListing(listings):
    htmlString = ''
    for listing in listings:
        htmlString += '<h1>' + listing["title"] + '</h1>'
        htmlString += '<a href="' + listing["url"] + '"> Check out listing!</a>'
    return htmlString

def sendEmails(users, listings):
    htmlForListings = generateHtmlForListing(listings)
    userEmails = [user["email"] for user in users]
    yag.send(to = userEmails, subject = 'New Listings Found', contents = [htmlForListings])

def lookForListings():    
    result = requests.get(
        baseUrl + "/search/" + subArea + "/apa?hasPic=1&postedToday=1&searchNearby=1&min_bedrooms=3&max_bedrooms=3&availabilityMode=0")
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        resultsList = soup.find_all("li", "result-row")
        listings = []
        for result in resultsList:
            listingContent = result.find("a", "result-title hdrlnk")
            listingTitle = listingContent.text
            listingUrl = baseUrl + listingContent.get('href')
            listings.append({"title": listingTitle, "url": listingUrl})
        print (listings)
        print(generateHtmlForListing(listings))
        
        if len(listings) > 0:
            sendEmails(users, listings)

while True:
    lookForListings()
    time.sleep(14400)


