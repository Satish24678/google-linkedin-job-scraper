import requests
import pandas as pd
import time

# Your SerpAPI Key
SERPAPI_KEY = "ad251e08cbdb32ff783dbfd7523612e276f3c869e9ea9ca6050be9313ad7f220"

# Define the API Endpoint
SERPAPI_URL = "https://serpapi.com/search"

# Define Initial Parameters for Google Jobs Search
params = {
    "engine": "google_jobs",
    "q": "Data Engineer",  # Job title
    "hl": "en",  # Language
    "location": "India",  # Location
    "api_key": SERPAPI_KEY
}

# List to store job postings
job_listings = []
MAX_JOBS = 100  # ✅ Limit to 100 jobs

while len(job_listings) < MAX_JOBS:
    # Fetch Data from SerpAPI
    response = requests.get(SERPAPI_URL, params=params)
    
    # Check if API request was successful
    if response.status_code == 200:
        data = response.json()
        jobs = data.get("jobs_results", [])

        for job in jobs:
            job_listings.append({
                "Job Title": job.get("title"),
                "Company": job.get("company_name"),
                "Location": job.get("location"),
                "Job Description": job.get("description"),
                "Job URL": job.get("share_link"),
                "Job Posting Time": job.get("detected_extensions", {}).get("posted_at", "N/A")
            })

            # ✅ Stop if we reach 100 jobs
            if len(job_listings) >= MAX_JOBS:
                break

        # Check for next page token
        next_page_token = data.get("serpapi_pagination", {}).get("next_page_token")
        if not next_page_token or len(job_listings) >= MAX_JOBS:
            break  # Exit loop if no more pages or limit reached

        # Update params with next page token
        params["next_page_token"] = next_page_token

        # Wait to avoid rate limits (optional)
        time.sleep(2)
    else:
        print("Error fetching jobs:", response.text)
        break

# Convert to DataFrame and save to CSV
df = pd.DataFrame(job_listings)
df.to_csv("google_jobs.csv", index=False)

print(f"✅ {len(job_listings)} job postings saved to 'google_jobs.csv'")

# ===========================================================

# Load the dataset
import pandas as pd
from datetime import datetime, timedelta
df = pd.read_csv("google_jobs.csv")

# 1. Rename columns for consistency
df.columns = df.columns.str.replace(" ", "_").str.lower()

# 2. Remove Duplicates (based on 'Job Title', 'Company', and 'Location')
df.drop_duplicates(subset=["job_title", "company", "location"], keep="first", inplace=True)

# 3. Handle Missing Values (Replace NaN with 'N/A')
df.fillna("N/A", inplace=True)

# 4. Clean 'location' column to remove extra text
df['location'] = df['location'].str.replace(r"\s*\(\+\d+ other\)", "", regex=True)

# 5. Convert 'job_posting_time' to actual date
current_date = datetime.today()

def convert_posting_time(time_str):
    if "hour" in time_str:
        hours = int(time_str.split()[0])  # Extract number of hours
        return (current_date - timedelta(hours=hours)).date()  # Keep only the date part
    elif "day" in time_str:
        days = int(time_str.split()[0])  # Extract number of days
        return (current_date - timedelta(days=days)).date()  # Keep only the date part
    else:
        return "N/A"  # Handle "Unknown" or missing values

df["job_posting_date"] = df["job_posting_time"].apply(lambda x: convert_posting_time(str(x)))

# 6. Remove 'job_posting_time' column as per request
df.drop(columns=['job_posting_time'], inplace=True, errors='ignore')

# 7. Shorten long job descriptions for readability
df['job_description'] = df['job_description'].str[:100] + "..."  # Keep only first 100 characters

# 8. Reset index after cleaning
df.reset_index(drop=True, inplace=True)

# 9. Save Cleaned Data to a New CSV
df.to_csv("cleaned_google_jobs.csv", index=False)

# =====================================================================

from sqlalchemy import create_engine

# Database connection details
DB_USER = "postgres"
DB_PASSWORD = "***********"
DB_HOST = "[::1]"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = "Jobs"

# Create SQLAlchemy Engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Store data in PostgreSQL
df.to_sql("jobs", engine, if_exists="replace", index=False)

print("✅ Data successfully stored in PostgreSQL!")

