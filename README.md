# VisaFriendly Job Scraper

## 📌 Overview
This project is a **job data pipeline** that extracts **Data Engineer** job postings from:
- **Google Jobs API** (via SerpAPI)
- **LinkedIn Web Scraping** (via Selenium)

It cleans, structures, and stores the data in **CSV files** and load into **PostgreSQL**.

## 🚀 How It Works
### 1️⃣ **Extract**
- **`google_job_scraper.py`** → Uses SerpAPI to extract Google job postings.
- **`linkedin_job_scraper.py`** → Uses Selenium to scrape job listings from LinkedIn.

### 2️⃣ **Transform**
- Removes **duplicates**.
- Ensures **data consistency**.
- Converts **posting times** into readable formats.

### 3️⃣ **Load**
- Stores the cleaned data in:
  - `google_jobs.csv`
  - `linkedin_jobs.csv`
  - `cleaned_google_jobs.csv`
  - `cleaned_linkedin_jobs.csv`
- Load Data into PostgreSQL Database
    
### 4️⃣ **Automate Execution with a Cron Job**
To run the scraper daily, add a cron job:

```sh
crontab -e
```

Add the following line to schedule the script every day at midnight:

```sh
0 0 * * * /usr/bin/python3 /path/to/linkedin_job_scraper.py
0 0 * * * /usr/bin/python3 /path/to/google_job_scraper.py
```

## AWS Cloud-Based Scraping Workflow
For a more scalable and automated solution, the job scraping process can be deployed using AWS services. The following workflow is implemented:

![AWS Job Scraper Workflow](AWS%20Job%20Scraper%20diagram.png)

### Architecture
1. **EventBridge:** Triggers the scraping process daily.
2. **AWS Lambda:** Executes the job scraping script (Google Jobs & LinkedIn scraping) and stores the extracted data in an S3 bucket.
3. **S3 Bucket:** Stores the CSV files containing job postings.
4. **AWS Glue:** Crawls the CSV files and prepares the data for analysis.
5. **Amazon Athena:** Queries and analyzes the crawled job postings.

### Steps to Deploy on AWS
1. **Create an S3 Bucket** to store scraped job postings.
2. **Deploy the Scraping Script in AWS Lambda:**
   - Convert the local Python scripts into a Lambda-compatible format.
   - Package required dependencies in a Lambda Layer.
3. **Set Up EventBridge to Trigger the Lambda Function:**
   - Configure a rule to invoke Lambda daily.
4. **Use AWS Glue to Crawl Data:**
   - Set up an AWS Glue Crawler to process CSV files in S3.
5. **Analyze Data with Amazon Athena:**
   - Create an Athena table to run SQL queries on job postings.
