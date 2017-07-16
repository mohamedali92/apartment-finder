import requests
from bs4 import BeautifulSoup
#import yagmail
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Scraper Settings
numberOfScrapes = 0
area = "vancouver"
subArea = "rch"
baseUrl = "https://" + area + ".craigslist.ca"

#users
# users = [{"name": "Mohamed", "email": "mohamed.ali@alumni.ubc.ca"},
#          {"name": "Nabila", "email": "nabila_emam1234@yahoo.com"},
#          {"name": "Hassanein", "email": "hassanin79@hotmail.com"}]

users = [{"name": "Mohamed", "email": "mohamed.ali@alumni.ubc.ca"}]

#AWS SMTP settings
smtp_server = 'email-smtp.us-west-2.amazonaws.com'
smtp_username = 'AKIAJOHYW36LMJJHE4RA'
smtp_password = 'Aj0uTg5fxjYW3wIRm3QhP37KElOjAyGaN+45Dyv8mivq'
smtp_port = '587'
smtp_do_tls = True




def generateHtmlForListing(listings):
    htmlString = ''
    for listing in listings:
        htmlString += '<h1>' + listing["title"] + '</h1>'
        htmlString += '<a href="' + listing["url"] + '"> Check out listing!</a>'
    return htmlString

def sendEmails(users, listings):
    s = smtplib.SMTP(
        host=smtp_server,
        port=smtp_port,
        timeout=10
    )
    s.starttls()
    s.ehlo()
    s.login(smtp_username, smtp_password)
    me = "mohammedali.saisdubai@gmail.com"
    htmlForListings = generateHtmlForListing(listings)

    userEmails = [user["email"] for user in users]
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "New Listings Found"
    msg['From'] = me
    msg['To'] = ", ".join(userEmails)
    msg.attach(MIMEText(htmlForListings, 'html'))
    
    s.sendmail(me, userEmails, msg.as_string())
    s.quit()
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
        
        if len(listings) > 0:
            sendEmails(users, listings)

while True:
    lookForListings()
    numberOfScrapes += 1
    print("Scrape: ", numberOfScrapes)
    time.sleep(3600)


