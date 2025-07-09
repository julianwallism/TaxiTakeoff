# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TaxiTakeoff is a modular Python data analysis project that fetches, processes, and visualizes flight departure data from AENA (Spanish airport operator). The project follows a clean architecture with separate modules for data handling, visualization, and reporting. The system is designed around three main workflows: data fetching, plot generation, and report delivery.

## Key Architecture

- **Modular Design**: Code is organized into separate modules under `src/`
- **Repository Pattern**: `src/repository/aena_flights_repository.py` handles data fetching from AENA API
- **Data Layer**: `src/data/` contains data models (`models.py`) and cleaning logic (`cleaner.py`)
- **Visualization Layer**: `src/visualization/` provides extensible plotting system with base classes and registry
- **Reports Layer**: `src/reports/` handles PDF generation and delivery (placeholder implementations)
- **Configuration**: `src/config/settings.py` manages application settings with environment variable support

## Dependencies & Environment

- **Package Manager**: Uses `uv` (modern Python package manager)
- **Python Version**: Requires Python >=3.12
- **Key Dependencies**: pandas, matplotlib, requests, airportsdata, pycountry, fastparquet, pyarrow

## Common Commands

```bash
# Install dependencies
uv sync

# Run the three main workflows:
# 1. Fetch flight data
uv run python scripts/fetch_data.py [AIRPORT_CODE]

# 2. Generate plots from fetched data
uv run python scripts/generate_plots.py [AIRPORT_CODE]

# 3. Send report (placeholder implementation)
uv run python scripts/send_report.py [email|telegram]

# Or use the console scripts:
uv run fetch-data PMI
uv run generate-plots PMI
uv run send-report email
```

## Data Flow

1. **Data Fetching** (`scripts/fetch_data.py`):
   - Uses `AenaFlightsRepository` to fetch raw flight data from AENA API
   - Returns `RawFlightData` objects containing pandas DataFrames
   - Saves data to `data/raw/{AIRPORT_CODE}/` with timestamp in Parquet format
   - Creates `data/raw/{AIRPORT_CODE}/latest.json` reference file for easy access

2. **Plot Generation** (`scripts/generate_plots.py`):
   - Accepts IATA airport code as command line argument (or uses default)
   - Loads latest raw data from `data/raw/{AIRPORT_CODE}/latest.json`
   - Warns if data is older than 1 day (yellow warning message)
   - Applies `FlightDataCleaner` to process and enrich data into `CleanedFlightData` objects
   - Generates all registered plots using `PlotRegistry`
   - Saves plots to `output/plots/{AIRPORT_CODE}/` with metadata in `plots_metadata.json`

3. **Report Delivery** (`scripts/send_report.py`):
   - Reads plot metadata from `output/plots/{AIRPORT_CODE}/plots_metadata.json`
   - Generates PDF report using `PDFReportGenerator` (placeholder implementation)
   - Delivers via email or Telegram using `DeliveryService` (placeholder implementation)

## Current Plot Types

The system currently implements 4 plot types in `src/visualization/time_plots.py`:

1. **DailyDeparturePlot** - Departures per day (bar chart)
2. **HourlyDeparturePlot** - Departures per hour of day (bar chart)
3. **FifteenMinuteDeparturePlot** - Departures every 15 minutes for next 48 hours (bar chart)
4. **WeeklyDeparturePlot** - Departures per day of the week (bar chart)

## Adding New Plots

To add a new plot type:

1. Create a new class in `src/visualization/time_plots.py` (or create a new file)
2. Inherit from `BasePlot` and implement required methods
3. Register the plot in `src/visualization/plot_registry.py`

Example:
```python
class NewPlot(BasePlot):
    @property
    def plot_name(self) -> str:
        return "new_plot"
    
    @property
    def plot_title(self) -> str:
        return "New Plot Title"
    
    def _generate_plot(self, data: CleanedFlightData) -> None:
        # Implementation here
        df = data.data
        # Use matplotlib to create your plot
```

Then add it to the registry in `src/visualization/plot_registry.py`:
```python
self._plots: List[Type[BasePlot]] = [
    DailyDeparturePlot,
    HourlyDeparturePlot,
    FifteenMinuteDeparturePlot,
    WeeklyDeparturePlot,
    NewPlot  # Add here
]
```

## Data Models

- **RawFlightData**: Wrapper around pandas DataFrame for data from AENA API
- **CleanedFlightData**: Enhanced data with country names, datetime parsing, and derived fields
- **FlightDataCleaner**: Handles data cleaning and enrichment (country lookup, datetime parsing)

## Configuration

- Default settings in `src/config/settings.py`
- Environment variable support for all configurations
- Key settings:
  - `DEFAULT_AIRPORT_CODE`: Default airport (PMI)
  - `PLOTS_OUTPUT_DIR`: Where to save plots (output/plots)
  - `REPORTS_OUTPUT_DIR`: Where to save reports (output/reports)
  - Email/Telegram credentials (placeholders for future implementation)

## Current Implementation Status

- ✅ **Data Fetching**: Fully implemented with AENA API integration
- ✅ **Data Cleaning**: Complete with country enrichment and datetime parsing
- ✅ **Visualization**: Extensible plotting system with 4 implemented plot types
- ⚠️ **PDF Generation**: Placeholder implementation (creates text files)
- ⚠️ **Email/Telegram Delivery**: Placeholder implementation (prints to console)

## File Structure

```
TaxiTakeoff/
├── src/
│   ├── data/
│   │   ├── models.py           # RawFlightData, CleanedFlightData
│   │   └── cleaner.py          # FlightDataCleaner
│   ├── repository/
│   │   └── aena_flights_repository.py  # AenaFlightsRepository
│   ├── visualization/
│   │   ├── base_plot.py        # BasePlot abstract class
│   │   ├── time_plots.py       # 4 concrete plot implementations
│   │   └── plot_registry.py    # PlotRegistry for managing plots
│   ├── reports/
│   │   ├── pdf_generator.py    # PDFReportGenerator (placeholder)
│   │   └── delivery.py         # Email/Telegram delivery (placeholder)
│   └── config/
│       └── settings.py         # Application settings
├── scripts/
│   ├── fetch_data.py           # Entrypoint 1: Data fetching
│   ├── generate_plots.py       # Entrypoint 2: Plot generation
│   └── send_report.py          # Entrypoint 3: Report delivery
├── data/
│   ├── raw/
│   │   └── {AIRPORT_CODE}/     # Raw flight data (Parquet files)
│   └── processed/              # (Reserved for future use)
├── output/
│   ├── plots/
│   │   └── {AIRPORT_CODE}/     # Generated plot images
│   └── reports/                # Generated PDF reports
└── pyproject.toml              # Project configuration with console scripts
```

## Legacy Files

- `main.py`: Old monolithic implementation (can be removed)
- `repository/`: Empty directory (old location, can be removed)