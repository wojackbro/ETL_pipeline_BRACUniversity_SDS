# BRAC University CSE Data Scraping Project

## Overview
This project scrapes and processes faculty and alumni data from BRAC University's Computer Science & Engineering (CSE) department website. It implements a complete ETL pipeline to extract, transform, and load structured academic data into CSV/Excel files and SQLite databases.

## Key Components

### 1. Faculty Data Extraction (`etl.py`)
- **Extraction**: Scrapes faculty profiles including names, designations, positions, and emails
- **Transformation**: Cleans data (handles missing values, normalizes emails, removes duplicates)
- **Loading**: Saves to timestamped CSV/Excel files
- **Features**:
  - Robust error handling with logging
  - CSS selector-based scraping
  - User-agent spoofing to avoid blocking

### 2. Alumni Data Pipeline (`alumni_former_scraping.py`)
- **Extraction**: Gathers alumni names, graduation years, current positions, and employers
- **Transformation**: 
  - Extracts 4-digit graduation years using regex
  - Standardizes missing data as "N/A"
- **Loading**: Outputs to timestamped CSV/Excel
- **Special Handling**: 
  - Deduplication logic
  - Year data validation

### 3. University API ETL (`script.ipynb`)
- **Extraction**: Fetches US university data from public API with retry logic
- **Transformation**: Normalizes JSON to pandas DataFrame
- **Loading**: Stores in SQLite database
- **Advanced Features**:
  - Exponential backoff for API requests
  - Chunked response handling
  - Connection pooling

## Technical Stack
- **Python Libraries**:
  - BeautifulSoup (HTML parsing)
  - Requests (HTTP client)
  - Pandas (data manipulation)
  - SQLAlchemy (database ORM)
- **Infrastructure**:
  - Jupyter Notebook for interactive development
  - SQLite for lightweight data storage

## Data Flow
```mermaid
graph LR
    A[Website/API] -->|Extract| B(Raw HTML/JSON)
    B -->|Transform| C(Pandas DataFrames)
    C -->|Load| D[CSV/Excel/SQLite]
```

## Usage
1. Install dependencies:
   ```bash
   pip install requests beautifulsoup4 pandas sqlalchemy
   ```

2. Run faculty scraper:
   ```bash
   python etl.py
   ```

3. Run alumni scraper:
   ```bash
   python alumni_former_scraping.py
   ```

4. Execute notebook for API ETL:
   ```bash
   jupyter notebook script.ipynb
   ```

## Output Samples
- `faculty_data_YYYYMMDD.csv` - Current faculty roster
- `alumni_data_YYYYMMDD.xlsx` - Alumni career tracking
- `universities.sqlite` - Normalized US university data

## Error Handling
- Comprehensive logging (timestamped errors/warnings)
- Retry mechanisms for failed requests
- Data validation during transformation

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/your-repo-link)  
*Note: Replace with actual repository link*