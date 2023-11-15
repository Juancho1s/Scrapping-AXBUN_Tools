import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver



os.environ["PATH"] += r"C:\SeleniumDrivers\geckodriver.exe"
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

driver.get("https://www.canacintra.net/directorio.php")


categoryIndex = 0
dataStored = {}
"""
{
    "category1": [
        {
            "Name": "...",
            "Address": "...",
            "Phone": "...",
            "Media": [...],
            "Services/Products": [...]
        },
        {
            ...
        }
    ],
    "category2":[
        ...
    ],
    ...
}
"""


wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mbr-gallery-title")))
categories = driver.find_elements(By.CLASS_NAME, "mbr-gallery-title")

# The `for i in categories:` loop is iterating over each element in the `categories` list. Each
# element represents a category on the webpage.
while categoryIndex < len(categories):

    categorieName = categories[categoryIndex].text

    dataStored[categorieName] = []

    categories[categoryIndex].click()

    wait.until(EC.presence_of_element_located((By.ID, "bootstrap-accordion_0")))
    enterprices = driver.find_element(By.ID, "bootstrap-accordion_0")

    enterpricesCard = enterprices.find_elements(By.CLASS_NAME, "card")

    for j in enterpricesCard:
        jWait = WebDriverWait(j, 10)
        
        dataFormat = {
            "Name": "",
            "Address": "",
            "Phone": "",
            "Media": [],
            "Services/Products": "",
        }

        jWait.until(EC.presence_of_element_located((By.CLASS_NAME, "panel-title")))
        j.find_element(By.CLASS_NAME, "panel-title").click()

        jWait.until(EC.((By.ID, "collapse1_3057")))
        enterpriceData = j.find_element(By.CLASS_NAME, "panel-body")

        entData = WebDriverWait(enterpriceData, 10)

        entData.until(EC.presence_of_all_elements_located((By.TAG_NAME, "p")))
        paragraphs = enterpriceData.find_elements(By.TAG_NAME, "p")

        WebDriverWait(paragraphs[0], 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        media = paragraphs[0].find_elements(By.TAG_NAME, "a")

        postText = enterpriceData.text.split("\n")

        dataFormat["Name"] = postText[0]
        dataFormat["Address"] = postText[1]

        entData.until(EC.presence_of_element_located((By.TAG_NAME, "strong")))
        dataFormat["Phone"] = enterpriceData.find_element(By.TAG_NAME, "strong").text

        mediaText = []
        for k in media:
            mediaText.append(k.text)

        dataFormat["Media"] = mediaText

        dataFormat["Services/Products"] = paragraphs[1].text.split("\n")[1]

        dataStored[categorieName].append(dataFormat)

    driver.back()
    categoryIndex += 1
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mbr-gallery-title")))
    categories = driver.find_elements(By.CLASS_NAME, "mbr-gallery-title")
