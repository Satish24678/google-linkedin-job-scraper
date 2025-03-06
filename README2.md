# Job Scraper

## Overview
This project extracts Data Engineering job postings from multiple sources, processes the data, and stores it efficiently. The extracted job listings can be saved in a CSV file or loaded into a PostgreSQL database for querying.

## Data Sources
The scraper collects job postings from:
1. **Google Jobs API (via SerpAPI)** – Fetches job listings from Google Jobs.
2. **LinkedIn Scraper** – Extracts job postings directly from LinkedIn.

## Extracted Fields
- Job Title
- Company
- Location
- Job Description
- Job URL
- Job Posting Time

## Technologies Used
- Python for scripting
- **SerpAPI** for Google Jobs extraction
- **Selenium & BeautifulSoup** for LinkedIn scraping
- **Pandas** for data cleaning and structuring
- **PostgreSQL** for storing job postings
- **AWS Services (Optional)** for cloud-based automation
- **Cron Job** for scheduling daily execution

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- PostgreSQL (for database storage)
- ChromeDriver (for Selenium)
- Required Python libraries:

```sh
pip install selenium beautifulsoup4 pandas psycopg2 requests
```

## Usage
### 1. Run Scraper Locally
Execute the scripts to extract job listings:

```sh
python google_job_scraper.py
python linkedin_job_scraper.py
```

### 2. Store Cleaned Data in PostgreSQL
The extracted and cleaned data is inserted into a PostgreSQL database.

#### **Setup PostgreSQL Database**
1. Create a PostgreSQL database and table:

```sql
CREATE DATABASE job_scraper;

CREATE TABLE job_listings (
    id SERIAL PRIMARY KEY,
    job_title TEXT,
    company TEXT,
    location TEXT,
    job_description TEXT,
    job_url TEXT,
    job_posting_time TIMESTAMP
);
```

2. Update `database_config.py` with PostgreSQL credentials.

3. Modify the script to insert data into the database:

```python
import psycopg2

def insert_into_db(data):
    connection = psycopg2.connect(
        dbname="job_scraper",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()
    for job in data:
        cursor.execute("""
            INSERT INTO job_listings (job_title, company, location, job_description, job_url, job_posting_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (job['title'], job['company'], job['location'], job['description'], job['url'], job['posting_time']))
    connection.commit()
    cursor.close()
    connection.close()
```

### 3. Automate Execution with a Cron Job
To run the scraper daily, add a cron job:

```sh
crontab -e
```

Add the following line to schedule the script every day at midnight:

```sh
0 0 * * * /usr/bin/python3 /path/to/linkedin_job_scraper.py
0 0 * * * /usr/bin/python3 /path/to/google_job_scraper.py
```

## Cloud-based Job Scraping with AWS
To automate job scraping on AWS, the architecture follows this workflow:

1. **Amazon EventBridge** triggers a Lambda function daily.
2. **AWS Lambda** runs the scraper code and stores the CSV file in **Amazon S3**.
3. **AWS Glue** crawls the CSV file and catalogs it.
4. **Amazon Athena** queries the cleaned job data for analysis.

### AWS Setup:
1. Create an **EventBridge Rule** to trigger the Lambda function.
2. Deploy the job scraper script inside an **AWS Lambda function**.
3. Configure **Lambda** to save the extracted data as a CSV file in **S3**.
4. Set up an **AWS Glue Crawler** to crawl the S3 bucket and create a catalog.
5. Use **Amazon Athena** to query the job listings.

## Querying Data from PostgreSQL
Once data is stored in PostgreSQL, use the following SQL query to retrieve job listings:

```sql
SELECT * FROM job_listings WHERE location = 'India' ORDER BY job_posting_time DESC;
```

## Conclusion
This project extracts, cleans, and stores job postings, enabling efficient querying either via a CSV file or a PostgreSQL database. With AWS automation, job data can be processed seamlessly at scale.

