import pandas as pd
import pycountry
from airportsdata import load

from .models import RawFlightData, CleanedFlightData


class FlightDataCleaner:
    """Handles cleaning and enrichment of flight data"""
    
    def __init__(self):
        self.airports = load('IATA')
    
    def get_country_name(self, iata_code: str) -> str:
        """Get country name from IATA airport code"""
        airport = self.airports.get(iata_code.upper())
        if not airport:
            return None
        iso_code = airport['country']
        country = pycountry.countries.get(alpha_2=iso_code)
        return country.name if country else None
    
    def clean_data(self, raw_data: RawFlightData) -> CleanedFlightData:
        """Clean and enrich raw flight data"""
        data = raw_data.data.copy()
        
        # Keep only required columns
        valid_columns = ["fecha", "horaProgramada", "iataOtro"]
        data = data.drop(columns=[col for col in data.columns if col not in valid_columns], errors='ignore')
        
        # Rename columns to English
        data = data.rename(columns={
            "fecha": "date",
            "horaProgramada": "scheduled_time",
            "iataOtro": "destination_code"
        })
        
        # Remove duplicates
        data = data.drop_duplicates().reset_index(drop=True)
        
        # Add country information
        data["destination_country"] = data["destination_code"].apply(self.get_country_name)
        
        # Create datetime column
        data["datetime"] = pd.to_datetime(
            data["date"] + " " + data["scheduled_time"], 
            format="%d/%m/%Y %H:%M:%S"
        )
        
        # Add day of week
        data["day_of_week"] = data["datetime"].dt.day_name()
        
        # Add additional time-based columns for analysis
        data['date_only'] = data['datetime'].dt.date
        data['hour'] = data['datetime'].dt.hour
        
        return CleanedFlightData.from_dataframe(data)