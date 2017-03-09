from lxml import html
from bs4 import BeautifulSoup
import requests
import urllib3
import re
import csv
import variables

# Imported Variables from Variables.py
Companies = variables.Companies
Terms = variables.Terms
htmlElements = variables.htmlElements


tmpArray = []
uniqueArray = []


def scrapSite(companies, keywords, domElements):
    for company in companies:
        for site in company['urls']:
            print(site)
            page = requests.get(site)
            soup = BeautifulSoup(page.content, "lxml")
            for element in domElements:
                content = soup.body.find_all(element)
                for e in content:
                    text = e.get_text()
                    newText = re.sub('[^a-zA-Z0-9 \n\.]', '', text)
                    text = re.sub('\n', '', newText)
                    finalClean = text.strip()
                    lowerCase = finalClean.lower().split()
                    for keyword in keywords:
                        for i in lowerCase:
                            if keyword in i:
                                tmpArray.append(
                                    [
                                        company['name'],
                                        site,
                                        finalClean
                                    ]
                                )

def uniqueness(array):
    for e in array:
        if e not in uniqueArray:
            uniqueArray.append(e)

def writeResults(array):
    with open('./output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "url", "content"])
        writer.writerows(array)
    f.close()


scrapSite(Companies, Terms, htmlElements)
uniqueness(tmpArray)
writeResults(uniqueArray)
