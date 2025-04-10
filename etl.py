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

def extract_faculty_data(url):
    """
    Extract faculty information from the BRAC University CSE website
    """
    try:
        logger.info("Starting data extraction from website")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lists to store faculty information
        names = []
        designations = []
        positions = []
        emails = []
        
        # Find all faculty cards
        faculty_cards = soup.select('div.relative.fac-card')
        
        for card in faculty_cards:
            # Extract name
            name_elem = card.select_one('p.text-sm.font-semibold.text-center.text-black.normal-case.md\\:text-\\[1rem\\]')
            name = name_elem.get_text(strip=True) if name_elem else None
            
            # Extract designation (e.g., "Dean")
            designation_elem = card.select_one('p.text-xs.font-semibold.text-center.md\\:text-base.text-sky-600')
            designation = designation_elem.get_text(strip=True) if designation_elem else None
            
            # Extract position (e.g., "Professor")
            position_elem = card.select_one('p.text-xs.font-medium.text-center.md\\:text-sm.text-slate-700')
            position = position_elem.get_text(strip=True) if position_elem else None
            
            # Extract email
            email_elem = card.select_one('p.text-xs.text-center.md\\:text-sm.text-slate-500')
            email = email_elem.get_text(strip=True) if email_elem else None
            
            if name:  # Only add if we have at least a name
                names.append(name)
                designations.append(designation)
                positions.append(position)
                emails.append(email)

        logger.info(f"Successfully extracted data for {len(names)} faculty members")
        return names, designations, positions, emails

    except requests.RequestException as e:
        logger.error(f"Connection error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        raise

def transform_data(names, designations, positions, emails):
    """Transform and clean the extracted data"""
    try:
        logger.info("Starting data transformation")
        
        # Create DataFrame with proper string conversion
        df = pd.DataFrame({
            'Name': names,
            'Designation': designations,
            'Position': positions,
            'Email': [str(email) if email else "N/A" for email in emails]
        })

        # Data cleaning
        df = df.dropna(subset=['Name'])  # Keep rows with at least a name
        df = df.drop_duplicates()
        df['Email'] = df['Email'].str.lower().str.strip()
        
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
    """Main ETL pipeline"""
    url = "https://cse.sds.bracu.ac.bd/faculty_list"
    output_file = f"faculty_data_{datetime.now().strftime('%Y%m%d')}.csv"
    
    try:
        names, designations, positions, emails = extract_faculty_data(url)
        df = transform_data(names, designations, positions, emails)
        load_data(df, output_file)
        logger.info("ETL process completed successfully")
        
    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()