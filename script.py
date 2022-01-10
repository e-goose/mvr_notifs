# crontab to regularly run script, check to see if there is a new post on mvrunning.com

# 1. Have file mvr_history.txt to store both the left and right column html of the website
# 2. Every time script is run, read in left and right column and write to mvr_new.txt
# 3. run "diff mvr_history.txt mvr_new.txt"
#       if there's no difference, do nothing
# 4. If there is a difference, email me and copy contents from mvr_new.txt to mvr_history.txt

import filecmp
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method
import os 

oldFile = os.environ.get("OLD_FILE")
newFile = os.environ.get("NEW_FILE")

# read in html content from mvrunning.com
import requests
from bs4 import BeautifulSoup
 
 
# Making a GET request
r = requests.get('https://www.mvrunning.com/', headers={"User-Agent": "XY"})
 
# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
 
leftCol = str(soup.find("div", id="left"))
rightCol = str(soup.find("div", id='right'))
siteText = leftCol + rightCol


# write to newFile
def writeToFile(file, txt):
    fileWriter = open(file, "w")
    fileWriter.write(txt)
    fileWriter.close()

writeToFile(newFile, siteText)

  
# shallow comparison
result = filecmp.cmp(newFile, oldFile)

# deep comparison
result = filecmp.cmp(newFile, oldFile, shallow=False)

# notify me
import smtplib, ssl

def notify():
    port = 465  # For SSL
    smtp_server = 'smtp.googlemail.com'
    sender_email = os.environ.get("EMAIL")  # Enter your address
    receiver_email = os.environ.get("RECIPIENT")  # Enter receiver address
    password = os.environ.get("PASSWORD")
    message = """\
    Subject: New mvrunning.com post!!

    This message is sent from Python ;)."""

    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)



# notify me and write to mvr_history.txt if different
if (result == False):

    # email me
    notify()

    # write to mvr_history.txt
    writeToFile(oldFile, siteText)