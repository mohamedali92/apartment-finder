import requests
from bs4 import BeautifulSoup


# Email Settings

smtp_server = 'email-smtp.us-west-2.amazonaws.com'
smtp_username = 'AKIAJOHYW36LMJJHE4RA'
smtp_password = 'Aj0uTg5fxjYW3wIRm3QhP37KElOjAyGaN+45Dyv8mivq'
smtp_port = '587'
smtp_do_tls = True

s = smtplib.SMTP(host=smtp_server,port=smtp_port,timeout=10)
s.starttls()
s.ehlo()
s.login(smtp_username, smtp_password)
# Scraper Settings
area = "vancouver"
subArea = "rch"
baseUrl = "https://" + area + ".craigslist.ca"

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


def sendEmail():
