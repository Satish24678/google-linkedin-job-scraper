from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("start-maximized")

service = Service("D:\Desktop\Satish\Job Scrapper\.venv\Scripts\chromedriver.exe")  # Update with your ChromeDriver path
driver = webdriver.Chrome(service=service, options=chrome_options)

# LinkedIn job search URL
job_url = "https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=India"
driver.get(job_url)

# Wait for the page to load
time.sleep(5)

# ✅ Scroll down to load more jobs
for _ in range(10):  # Scroll multiple times
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(3)

# ✅ Extract job details
job_listings = []
jobs = driver.find_elements(By.XPATH, '//*[@id = "main-content"]/section[2]/ul/li')

for job in jobs:
    title = job.find_element(By.CLASS_NAME, "base-search-card__title").text
    company = job.find_element(By.CLASS_NAME, 'hidden-nested-link').text
    location = job.find_element(By.CLASS_NAME, "job-search-card__location").text
    time_element = job.find_element(By.TAG_NAME, "time")  # Find the <time> tag
    job_posting_date = time_element.get_attribute("datetime") if time_element else "Not Available"
    job_url = job.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")

    if job_url != "Not Available":
        driver.execute_script(f"window.open('{job_url}', 'new_window')")
        driver.switch_to.window(driver.window_handles[1])  # Switch to new tab
        time.sleep(3)  # Wait for the page to load

        job_description = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup").text

        driver.close()  # Close the new taG
        driver.switch_to.window(driver.window_handles[0])
    else:
        job_description = "Not Available"

    if "data engineer" in title.lower():
        job_listings.append({
            "Job Title": title.strip(),
            "Company": company.strip(),
            "Location": location.strip(),
            "Job Description": job_description.strip,  # Shorten description
            "Job URL": job_url,
            "Job Posting Date": job_posting_time.strip()
        })

# Close the browser
driver.quit()

# Convert to DataFrame and save to CSV
df = pd.DataFrame(job_listings)
df.to_csv("linkedin_jobs.csv", index=False)


# =========================================================================

# Load the dataset
import pandas as pd
from datetime import datetime, timedelta
df = pd.read_csv("linkedin_jobs.csv")

# 1. Rename columns for consistency
df.columns = df.columns.str.replace(" ", "_").str.lower()

# ✅ 1. Remove Duplicates (based on 'Job Title', 'Company', and 'Location')
df.drop_duplicates(subset=["job_title", "company", "location"], keep="first", inplace=True)

# ✅ 2. Handle Missing Values (Replace NaN with 'N/A')
df.fillna("N/A", inplace=True)

# 3. Clean 'location' column to remove extra text
df['location'] = df['location'].str.replace(r"\s*\(\+\d+ other\)", "", regex=True)

# 5. Shorten long job descriptions for readability
df['job_description'] = df['job_description'].str[:100] + "..."  # Keep only first 100 characters

# 7. Reset index after cleaning
df.reset_index(drop=True, inplace=True)

# ✅ 5. Save Cleaned Data to a New CSV
df.to_csv("cleaned_google_jobs.csv", index=False)

# =====================================================================

from sqlalchemy import create_engine

# Database connection details
DB_USER = "postgres"
DB_PASSWORD = "*******"
DB_HOST = "[::1]"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "Jobs"

# Create SQLAlchemy Engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Store data in PostgreSQL
df.to_sql("jobs", engine, if_exists="append", index=False)

print("✅ Data successfully stored in PostgreSQL!")
