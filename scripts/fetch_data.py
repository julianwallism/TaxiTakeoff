#!/usr/bin/env python3
"""
Entrypoint 1: Data Fetching
Fetches flight data from AENA repository and saves it locally.
"""

import sys
import json
from datetime import datetime
from pathlib import Path

from taxitakeoff.config.settings import get_settings
from taxitakeoff.repository.aena_flights_repository import AenaFlightsRepository


def main():
    """Main entry point for data fetching"""
    settings = get_settings()
    
    # Get airport code from command line or use default
    airport_code = sys.argv[1] if len(sys.argv) > 1 else settings.default_airport_code
    
    print(f"Fetching flight data for airport: {airport_code}")
    
    # Initialize repository
    repo = AenaFlightsRepository()
    
    try:
        # Fetch data
        raw_data = repo.get_departing_flights(airport_code)
        
        # Create output directory for specific airport
        output_dir = Path("data/raw") / airport_code
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save raw data with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flights_{airport_code}_{timestamp}.parquet"
        filepath = output_dir / filename
        
        # Add metadata columns to DataFrame before saving
        df = raw_data.data.copy()
        df['airport_code'] = airport_code
        df['fetched_at'] = datetime.now().isoformat()
        
        # Save DataFrame as parquet
        df.to_parquet(filepath, index=False)
        
        print(f"Data saved to: {filepath}")
        print(f"Records fetched: {len(raw_data.data)}")
        
        # Save latest data link
        latest_file = output_dir / "latest.json"
        with open(latest_file, 'w') as f:
            json.dump({
                'latest_file': str(filepath),
                'airport_code': airport_code,
                'fetched_at': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"Latest data reference saved to: {latest_file}")
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()