import json
from time import sleep
from lxml import html
from selenium import webdriver
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


JSON_FOLDER = "data"
INPUT_LINK_FILE = "job_links.json"
OUTPUT_FILE = "job_details.json"


# Open the link in the driver and get all info
def get_session_info(driver):
    # Open and load JSON file that contains link and some basic info for the session
    f = open('{}\\{}'.format(JSON_FOLDER, INPUT_LINK_FILE))
    infos = json.load(f)
    data = []

    # Loop through all links
    for i in range(len(infos)):
        url = infos[i]["LINK"]
        title = infos[i]["TITLE"]
        location = infos[i]["LOCATION"]
        driver.get(url)
        print(url)
        sleep(5)
        # Get main session data
        session_data = get_session_data(driver.page_source, url, title, location)
        data.append(session_data)
    return data


# Get main session data
def get_session_data(page_source, job_link, title, location):
    root = html.fromstring(page_source)
    job_level = root.xpath("string(.//li[@class='description__job-criteria-item'][1]/span)").strip()
    job_type = root.xpath("string(.//li[@class='description__job-criteria-item'][2]/span)").strip()
    company_link = root.xpath("string(.//span[@class='topcard__flavor']/a/@href)").strip()
    company_name = root.xpath("string(.//span[@class='topcard__flavor']/a)").strip()
    job_details = root.xpath("string(.//div[@class='decorated-job-posting__details'])").strip()

    data = {
        "JOB TITLE": title,
        "JOB TYPE": job_type,
        'JOB LEVEL': job_level,
        'COMPANY': company_name,
        'COMPANY LINK': company_link,
        'LOCATION': location,
        'JOB DETAILS': job_details,
        'JOB LINK': job_link
    }
    print(data)
    return data


# Write data to json files to avoid re rerunning the script multiple times
def output_session_to_file(data):
    filepath = os.path.abspath(f"./{JSON_FOLDER}/{OUTPUT_FILE}")
    with open(filepath, 'w') as f:
        json.dump(data, f)


def run():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    data = get_session_info(driver)
    print(f'- Num records: {len(data)}')
    output_session_to_file(data)
    driver.close()


if __name__ == '__main__':
    run()
