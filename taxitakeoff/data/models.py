from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import pandas as pd


@dataclass
class RawFlightData:
    """Raw flight data from AENA API"""
    data: pd.DataFrame
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'RawFlightData':
        return cls(data=df)


@dataclass
class CleanedFlightData:
    """Cleaned and enriched flight data"""
    data: pd.DataFrame
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'CleanedFlightData':
        return cls(data=df)
    
    def get_date_range(self) -> tuple[datetime, datetime]:
        """Get the date range of the flight data"""
        return self.data['datetime'].min(), self.data['datetime'].max()
    
    def get_flight_count(self) -> int:
        """Get total number of flights"""
        return len(self.data)
    
    def get_destinations(self) -> list[str]:
        """Get unique destination codes"""
        return self.data['destination_code'].unique().tolist()
    
    def get_countries(self) -> list[str]:
        """Get unique destination countries"""
        return self.data['destination_country'].dropna().unique().tolist()