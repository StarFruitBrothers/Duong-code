import pandas as pd
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from lxml import html

JSON_FOLDER = "data"
OUTPUT_EXCEL_FOLDER = "output"
JOB_JSON_FILE = "job_details.json"
INPUT_FILE = "Job_details_01-27-2023.xlsx"
OUTPUT_FILE = "Job_details_01-28-2023.xlsx"


# Write to Excel file
def write_to_excel():
    created_at = datetime.now()
    current_time = str(created_at.strftime("%m-%d-%Y"))
    writer = pd.ExcelWriter('{}\\Job_details_{}.xlsx'.format(OUTPUT_EXCEL_FOLDER, current_time), engine='openpyxl')
    data = pd.read_json('{}\\{}'.format(JSON_FOLDER, JOB_JSON_FILE))
    sheet_name = "Jobs"
    # Write to excel and format rows columns and add filter
    data.to_excel(writer, index=False, sheet_name=sheet_name)
    sheet = writer.sheets[sheet_name]
    sheet.auto_filter.ref = sheet.dimensions
    writer.save()


def format_excel_file():
    driver = webdriver.Chrome(ChromeDriverManager().install())

    writer = pd.ExcelWriter('{}\\{}'.format(OUTPUT_EXCEL_FOLDER, OUTPUT_FILE), engine='openpyxl')
    df = pd.read_excel('{}\\{}'.format(OUTPUT_EXCEL_FOLDER, INPUT_FILE), sheet_name="Jobs")
    df["JOB DETAILS"] = df["JOB DETAILS"].apply(lambda x: x.replace("\n", "").replace("\t", "").split("Show more")[0].strip() if not pd.isnull(x) else '')
    for i in range(len(df)):
        # if pd.isnull(df["JOB TYPE"][i]) and df["JOB LEVEL"][i] == "Full-time":
        #     df["JOB TYPE"][i] = "Full-time"
        #     df["JOB LEVEL"][i] = ""
        if pd.isnull(df["JOB DETAILS"][i]) or df["JOB DETAILS"][i] == "":
#        if df["JOB DETAILS"][i].startswith("Direct message the job"):
            driver.get(df["JOB LINK"][i])
            sleep(2)
            root = html.fromstring(driver.page_source)
            job_level = root.xpath("string(.//li[@class='description__job-criteria-item'][1]/span)").strip()
            job_type = root.xpath("string(.//li[@class='description__job-criteria-item'][2]/span)").strip()
            company_link = root.xpath("string(.//span[@class='topcard__flavor']/a/@href)").strip()
            company_name = root.xpath("string(.//span[@class='topcard__flavor']/a)").strip()
            job_details = root.xpath("string(.//div[@class='decorated-job-posting__details'])").strip()
            #import pdb; pdb.set_trace()
            if pd.isnull(df["JOB LEVEL"][i]):
                df["JOB LEVEL"][i] = job_level
            if pd.isnull(df["JOB TYPE"][i]):
                df["JOB TYPE"][i] = job_type
            if pd.isnull(df["COMPANY"][i]):
                df["COMPANY"][i] = company_name
            if pd.isnull(df["COMPANY LINK"][i]):
                df["COMPANY LINK"][i] = company_link
            #if pd.isnull(df["JOB DETAILS"][i]) or df["JOB DETAILS"][i] == "":
            df["JOB DETAILS"][i] = job_details
    df.to_excel(writer, index=False, sheet_name="Jobs")
    sheet = writer.sheets["Jobs"]
    sheet.auto_filter.ref = sheet.dimensions
    writer.save()


if __name__ == '__main__':
    #write_to_excel()
    format_excel_file()

