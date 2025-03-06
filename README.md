# VisaFriendly Job Scraper

## 📌 Overview
This project is a **job data pipeline** that extracts **Data Engineer** job postings from:
- **Google Jobs API** (via SerpAPI)
- **LinkedIn Web Scraping** (via Selenium)

It cleans, structures, and stores the data in **CSV files** and optionally in **PostgreSQL**.

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
  - **Optional:** Stores data in PostgreSQL.

## 🛠️ Installation & Setup
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/visa_friendly_job_scraper.git
cd visa_friendly_job_scraper
