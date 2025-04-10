import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_alumni_data(url):
    """
    Extract alumni information from the BRAC University CSE website
    """
    try:
        logger.info("Starting data extraction from alumni page")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lists to store alumni information
        names = []
        graduation_years = []
        current_positions = []
        employers = []
        
        # Find all alumni cards
        alumni_cards = soup.select('div.relative.fac-card')
        
        for card in alumni_cards:
            # Extract name
            name_elem = card.select_one('p.text-sm.font-semibold.text-center.text-black.normal-case.md\\:text-\\[1rem\\]')
            name = name_elem.get_text(strip=True) if name_elem else None
            
            # Extract graduation year (assuming it's in the first text-slate-500 paragraph)
            year_elem = card.select_one('p.text-xs.text-center.md\\:text-sm.text-slate-500')
            year = year_elem.get_text(strip=True) if year_elem else None
            
            # Extract current position (assuming it's in the text-sky-600 paragraph)
            position_elem = card.select_one('p.text-xs.font-semibold.text-center.md\\:text-base.text-sky-600')
            position = position_elem.get_text(strip=True) if position_elem else None
            
            # Extract employer (assuming it's in the text-slate-700 paragraph)
            employer_elem = card.select_one('p.text-xs.font-medium.text-center.md\\:text-sm.text-slate-700')
            employer = employer_elem.get_text(strip=True) if employer_elem else None
            
            if name:  # Only add if we have at least a name
                names.append(name)
                graduation_years.append(year)
                current_positions.append(position)
                employers.append(employer)

        logger.info(f"Successfully extracted data for {len(names)} alumni members")
        return names, graduation_years, current_positions, employers

    except requests.RequestException as e:
        logger.error(f"Connection error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        raise

def transform_data(names, graduation_years, current_positions, employers):
    """Transform and clean the extracted data"""
    try:
        logger.info("Starting data transformation")
        
        # Create DataFrame with proper string conversion
        df = pd.DataFrame({
            'Name': names,
            'Graduation_Year': [str(year) if year else "N/A" for year in graduation_years],
            'Current_Position': [str(pos) if pos else "N/A" for pos in current_positions],
            'Employer': [str(emp) if emp else "N/A" for emp in employers]
        })

        # Data cleaning
        df = df.dropna(subset=['Name'])  # Keep rows with at least a name
        df = df.drop_duplicates()
        
        # Clean year data
        df['Graduation_Year'] = df['Graduation_Year'].str.extract(r'(\d{4})')[0]  # Extract 4-digit years
        
        logger.info(f"Transformed data shape: {df.shape}")
        return df

    except Exception as e:
        logger.error(f"Transformation error: {str(e)}")
        raise

def load_data(df, output_file):
    """Save data to CSV and Excel"""
    try:
        logger.info(f"Saving data to {output_file}")
        
        df.to_csv(output_file, index=False)
        df.to_excel(output_file.replace('.csv', '.xlsx'), index=False)
        
        logger.info("Data saved successfully")

    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise

def main():
    """Main ETL pipeline for alumni data"""
    url = "https://cse.sds.bracu.ac.bd/alumni_list"
    output_file = f"alumni_data_{datetime.now().strftime('%Y%m%d')}.csv"
    
    try:
        names, years, positions, employers = extract_alumni_data(url)
        df = transform_data(names, years, positions, employers)
        load_data(df, output_file)
        logger.info("Alumni ETL process completed successfully")
        
    except Exception as e:
        logger.error(f"Alumni ETL process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()