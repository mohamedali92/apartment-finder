import requests
from bs4 import BeautifulSoup
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Specify Area and SubArea
numberOfScrapes = 0
area = "vancouver"
subArea = "rch"
baseUrl = "https://" + area + ".craigslist.ca"

#Add users to be notified
users = [{"name": "", "email": ""}]

#Supply SMTP settings
smtpServer = ''
smtpUsername = ''
smtpPassword = ''
smtpPort = '587'
smtpTls = True

#Specify Sender
sender = ""

#Time in Seconds
timeBetweenScrapes = 3600

def generateHtmlForListing(listings):
    htmlString = ''
    for listing in listings:
        htmlString += '<h1>' + listing["title"] + '</h1>'
        htmlString += '<a href="' + listing["url"] + '"> Check out listing!</a>'
    return htmlString

def sendEmails(users, listings):
    s = smtplib.SMTP(
        host=smtpServer,
        port=smtpPort,
        timeout=10
    )
    s.starttls()
    s.ehlo()
    s.login(smtpUsername, smtpPassword)
    
    htmlForListings = generateHtmlForListing(listings)
    userEmails = [user["email"] for user in users]
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "New Listings Found"
    msg['From'] = sender
    msg['To'] = ", ".join(userEmails)
    msg.attach(MIMEText(htmlForListings, 'html'))
    
    s.sendmail(sender, userEmails, msg.as_string())
    s.quit()

def lookForListings():
    
    #Modify URL based on required critera
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
        
        if len(listings) > 0:
            sendEmails(users, listings)

while True:
    lookForListings()
    numberOfScrapes += 1
    print("Scrape: ", numberOfScrapes)
    time.sleep(3600)


