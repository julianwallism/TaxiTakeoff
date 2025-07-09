import pandas as pd
import matplotlib.pyplot as plt

from .base_plot import BasePlot
from ..data.models import CleanedFlightData


class DailyDeparturePlot(BasePlot):
    """Plot showing departures per day"""
    
    @property
    def plot_name(self) -> str:
        return "departures_per_day"
    
    @property
    def plot_title(self) -> str:
        return "Departures per Day"
    
    def _generate_plot(self, data: CleanedFlightData) -> None:
        df = data.data
        df['date_only'].value_counts().sort_index().plot(kind='bar')
        plt.xlabel('Date')
        plt.ylabel('Number of Flights')
        plt.xticks(rotation=45)


class HourlyDeparturePlot(BasePlot):
    """Plot showing departures per hour of day"""
    
    @property
    def plot_name(self) -> str:
        return "departures_per_hour"
    
    @property
    def plot_title(self) -> str:
        return "Departures per Hour of Day"
    
    def _generate_plot(self, data: CleanedFlightData) -> None:
        df = data.data
        df['hour'].value_counts().sort_index().plot(kind='bar')
        plt.xlabel('Hour')
        plt.ylabel('Number of Flights')
        plt.xticks(range(24))


class FifteenMinuteDeparturePlot(BasePlot):
    """Plot showing departures every 15 minutes for next 48 hours"""
    
    @property
    def plot_name(self) -> str:
        return "departures_per_15min_48h"
    
    @property
    def plot_title(self) -> str:
        return "Departures Every 15 Minutes (Next 48h)"
    
    def _generate_plot(self, data: CleanedFlightData) -> None:
        df = data.data
        
        # Get 48-hour window
        start_time = df['datetime'].min()
        end_time = start_time + pd.Timedelta(hours=48)
        
        # Filter data within window
        window_data = df[(df['datetime'] >= start_time) & (df['datetime'] <= end_time)]
        
        # Create 15-minute bins
        bins = pd.date_range(start=start_time, end=end_time, freq='15min')
        window_data['time_bin'] = pd.cut(window_data['datetime'], bins=bins)
        
        # Count per bin
        counts = window_data['time_bin'].value_counts().sort_index()
        
        # Plot
        plt.figure(figsize=(15, 5))
        counts.plot(kind='bar', width=1)
        plt.xlabel('Time Interval')
        plt.ylabel('Number of Flights')
        plt.xticks([], [])  # Hide x labels for clarity


class WeeklyDeparturePlot(BasePlot):
    """Plot showing departures per day of the week"""
    
    @property
    def plot_name(self) -> str:
        return "departures_per_day_of_week"
    
    @property
    def plot_title(self) -> str:
        return "Departures per Day of the Week"
    
    def _generate_plot(self, data: CleanedFlightData) -> None:
        df = data.data
        df['day_of_week'].value_counts().sort_index().plot(kind='bar')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Flights')
        plt.xticks(rotation=45)