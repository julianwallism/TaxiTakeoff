import os

import matplotlib.pyplot as plt
import pandas as pd
import pycountry
from airportsdata import load

from repository.aena_flights_repository import AenaFlightsRepository

airports = load('IATA')

def get_country_name(iata_code):
    airport = airports.get(iata_code.upper())
    if not airport:
        return None
    iso_code = airport['country']
    country = pycountry.countries.get(alpha_2=iso_code)
    return country.name if country else None

def create_output_directory(output_dir="output_plots"):
    """Create the output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def get_histogram_per_date(data: pd.DataFrame, output_dir="output_plots"):
    # ----------------------
    # 1. Histogram per date
    # ----------------------
    data['date_only'] = data['datetime'].dt.date

    plt.figure(figsize=(10, 5))
    data['date_only'].value_counts().sort_index().plot(kind='bar')
    plt.title('Departures per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Flights')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/departures_per_day.png")
    plt.close()

def get_histogram_per_hour(data: pd.DataFrame, output_dir="output_plots"):
    # -----------------------
    # 2. Histogram per hour
    # -----------------------
    data['hour'] = data['datetime'].dt.hour

    plt.figure(figsize=(10, 5))
    data['hour'].value_counts().sort_index().plot(kind='bar')
    plt.title('Departures per Hour of Day')
    plt.xlabel('Hour')
    plt.ylabel('Number of Flights')
    plt.xticks(range(24))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/departures_per_hour.png")
    plt.close()

def get_histogram_per_15_min(data: pd.DataFrame, output_dir="output_plots"):
    
    # ------------------------------------------------
    # 3. Histogram per 5-min interval for next 48 hours
    # ------------------------------------------------
    start_time = data['datetime'].min()
    end_time = start_time + pd.Timedelta(hours=48)

    # Filter data in the next 48h window
    window_data = data[(data['datetime'] >= start_time) & (data['datetime'] <= end_time)]

    # Create 5-minute bins
    bins = pd.date_range(start=start_time, end=end_time, freq='15min')
    window_data['time_bin'] = pd.cut(window_data['datetime'], bins=bins)

    # Count per bin
    counts = window_data['time_bin'].value_counts().sort_index()

    # Plot
    plt.figure(figsize=(15, 5))
    counts.plot(kind='bar', width=1)
    plt.title('Departures Every 15 Minutes (Next 48h)')
    plt.xlabel('Time Interval')
    plt.ylabel('Number of Flights')
    plt.xticks([], [])  # Hide x labels for clarity
    plt.tight_layout()
    plt.savefig(f"{output_dir}/departures_per_15min_48h.png")
    plt.close()

def get_histogram_per_day_of_week(data: pd.DataFrame, output_dir="output_plots"):
    # -----------------------------------
    # 4. Histogram per day of the week
    # -----------------------------------
    plt.figure(figsize=(10, 5))
    data['day_of_week'].value_counts().sort_index().plot(kind='bar')
    plt.title('Departures per Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Flights')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/departures_per_day_of_week.png")
    plt.close()


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    valid_columns = ["fecha", "horaProgramada", "iataOtro"]
    data = data.drop(columns=[col for col in data.columns if col not in valid_columns], errors='ignore')

    data = data.rename(columns={
        "fecha": "date",
        "horaProgramada": "scheduled_time",
        "iataOtro": "destination_code"
    })

    data = data.drop_duplicates().reset_index(drop=True)

    data["destination_country"] = data["destination_code"].apply(lambda destination_code: get_country_name(destination_code))

    # Combine date and scheduled_time into a single datetime column
    data["datetime"] = pd.to_datetime(data["date"] + " " + data["scheduled_time"], format="%d/%m/%Y %H:%M:%S")
    
    # Add day of week
    data["day_of_week"] = data["datetime"].dt.day_name()

    return data




def main():
    repo = AenaFlightsRepository()

    data = repo.get_departing_flights("PMI")

    cleaned_data = clean_data(data)

    create_output_directory()
    get_histogram_per_date(cleaned_data)
    get_histogram_per_hour(cleaned_data)
    get_histogram_per_15_min(cleaned_data)
    get_histogram_per_day_of_week(cleaned_data)


if __name__ == '__main__':
    main()