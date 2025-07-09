#!/usr/bin/env python3
"""
Entrypoint 2: Plot Generation
Reads raw data, cleans it, and generates all registered plots.
"""

import json
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

from taxitakeoff.data.models import RawFlightData
from taxitakeoff.data.cleaner import FlightDataCleaner
from taxitakeoff.visualization.plot_registry import plot_registry
from taxitakeoff.config.settings import get_settings


def load_latest_data_for_airport(airport_code: str) -> RawFlightData:
    """Load the latest raw data file for a specific airport"""
    latest_file = Path("data/raw") / airport_code / "latest.json"
    
    if not latest_file.exists():
        raise FileNotFoundError(f"No data found for airport {airport_code}. Run fetch_data.py {airport_code} first.")
    
    with open(latest_file, 'r') as f:
        latest_info = json.load(f)
    
    # Check if data is older than 1 day
    fetched_at = datetime.fromisoformat(latest_info['fetched_at'])
    if datetime.now() - fetched_at > timedelta(days=1):
        print(f"\033[93mWarning: Data is {(datetime.now() - fetched_at).days} days old. Consider running fetch_data.py {airport_code} for updated data.\033[0m")
    
    data_file = Path(latest_info['latest_file'])
    
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    # Load parquet file
    df = pd.read_parquet(data_file)
    
    return RawFlightData.from_dataframe(df)


def main():
    """Main entry point for plot generation"""
    settings = get_settings()
    
    # Get airport code from command line or use default
    airport_code = sys.argv[1] if len(sys.argv) > 1 else settings.default_airport_code
    
    print(f"Loading flight data for airport: {airport_code}")
    
    try:
        # Load raw data
        raw_data = load_latest_data_for_airport(airport_code)
        print(f"Loaded {len(raw_data.data)} flight records")
        
        # Clean data
        print("Cleaning and enriching data...")
        cleaner = FlightDataCleaner()
        cleaned_data = cleaner.clean_data(raw_data)
        
        print(f"Cleaned data: {cleaned_data.get_flight_count()} flights")
        print(f"Date range: {cleaned_data.get_date_range()}")
        print(f"Destinations: {len(cleaned_data.get_destinations())} unique")
        print(f"Countries: {len(cleaned_data.get_countries())} unique")
        
        # Generate all plots
        print("Generating plots...")
        # Create airport-specific output directory
        airport_output_dir = Path(settings.plots_output_dir) / airport_code
        airport_output_dir.mkdir(parents=True, exist_ok=True)
        
        plots = plot_registry.create_all_plots(str(airport_output_dir))
        
        generated_plots = []
        for plot in plots:
            print(f"  Generating {plot.plot_title}...")
            filepath = plot.generate(cleaned_data)
            generated_plots.append(filepath)
            print(f"    Saved to: {filepath}")
        
        # Save plot metadata
        metadata = {
            'generated_at': pd.Timestamp.now().isoformat(),
            'flight_data_summary': {
                'flight_count': cleaned_data.get_flight_count(),
                'date_range': [str(d) for d in cleaned_data.get_date_range()],
                'destinations': cleaned_data.get_destinations(),
                'countries': cleaned_data.get_countries()
            },
            'plots': [plot.get_metadata() for plot in plots],
            'filepaths': generated_plots
        }
        
        metadata_file = airport_output_dir / "plots_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nGenerated {len(generated_plots)} plots successfully!")
        print(f"Metadata saved to: {metadata_file}")
        
    except Exception as e:
        print(f"Error generating plots: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()