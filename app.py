import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://www.reed.co.uk"

JOB_DATA = []

def scrape_jobs(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for job_post in soup.select(".job-result-card"):
        job_title = job_post.select_one(".job-result-heading__title").get_text(strip=True)
        date_posted = job_post.select_one(".job-result-heading__posted-by").get_text(strip=True, separator=" ")
        salary = job_post.select_one(".job-metadata__item--salary").get_text(strip=True)
        location = job_post.select_one(".job-metadata__item--location").get_text(strip=True, separator=", ")
        job_type = job_post.select_one(".job-metadata__item--type").get_text(strip=True, separator=" ")
        description = job_post.select_one(".job-result-description__details").get_text(strip=True, separator=" ")
        job_link = BASE_URL + job_post.find("a")["href"]
        try:
            remote_work = job_post.select_one(".job-metadata__item--remote").get_text(strip=True, separator=" ")
        except: 
            remote_work = None

        JOB_DATA.append((job_title, date_posted, salary, location, job_type, remote_work, job_link, description))

def save_to_csv():
    dataframe = pd.DataFrame(JOB_DATA, columns=["Job Title", "Date/Company", "Salary", "Location", "Job Type", "Metadata", "Link", "Desc"])
    dataframe.to_csv("data/job_data.csv", index=False)

def main():
    print("Scraping in progress. Please wait")
    job_urls = pd.read_csv("data/job_urls.csv")
    for url in job_urls["urls"]:
        scrape_jobs(url)
    save_to_csv()
    print("Scraping complete. Data has been stored in 'data/job_data.csv'. ")

if __name__ == "__main__":
    main()
