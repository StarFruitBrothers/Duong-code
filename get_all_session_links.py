import os
import json
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html

JSON_FOLDER = 'data'
LINKS_JSON_FILE = 'job_links.json'

SESSIONS_URL = "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"


def run():
    # Set up the driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(SESSIONS_URL)
    driver.maximize_window()
    sleep(2)
    for _ in range(6):
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        sleep(3)
    data = get_links(driver)
    print(f'- Num records: {len(data)}')
    output_links_to_file(data)
    driver.close()


# Get all links
def get_links(driver):
    root = html.fromstring(driver.page_source)
    result_nodes = root.xpath('//ul[@class="jobs-search__results-list"]/li')
    result = []
    for result_node in result_nodes:
        job_link = result_node.xpath("string(./div/a/@href)")
        job_title = result_node.xpath("string(./div/a)").strip()
        job_location = result_node.xpath("string(.//span[@class='job-search-card__location'])").strip()
        print(job_location)
        result.append({
            "LINK": job_link,
            "TITLE": job_title,
            "LOCATION": job_location
        })
    return result


# Write data to json files to avoid re rerunning the script multiple times
def output_links_to_file(data):
    filepath = os.path.abspath(f"./{JSON_FOLDER}/{LINKS_JSON_FILE}")
    print(filepath)
    with open(filepath, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    run()
