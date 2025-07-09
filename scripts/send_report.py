#!/usr/bin/env python3
"""
Entrypoint 3: Report Delivery
Aggregates plots into a PDF report and sends it via email or Telegram.
"""

import sys
import json
from pathlib import Path

from taxitakeoff.data.models import CleanedFlightData
from taxitakeoff.data.cleaner import FlightDataCleaner
from taxitakeoff.reports.pdf_generator import PDFReportGenerator
from taxitakeoff.reports.delivery import create_delivery_service
from taxitakeoff.config.settings import get_settings


def load_plot_metadata():
    """Load plot metadata and cleaned data"""
    settings = get_settings()
    metadata_file = Path(settings.plots_output_dir) / "plots_metadata.json"
    
    if not metadata_file.exists():
        raise FileNotFoundError("No plot metadata found. Run generate_plots.py first.")
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    return metadata


def main():
    """Main entry point for report delivery"""
    settings = get_settings()
    
    # Parse command line arguments
    delivery_method = sys.argv[1] if len(sys.argv) > 1 else "email"
    
    if delivery_method not in ["email", "telegram"]:
        print("Usage: python send_report.py [email|telegram]")
        sys.exit(1)
    
    print(f"Preparing report for delivery via {delivery_method}...")
    
    try:
        # Load plot metadata
        metadata = load_plot_metadata()
        plot_filepaths = metadata['filepaths']
        
        print(f"Found {len(plot_filepaths)} plots to include in report")
        
        # Create flight data object for report generation
        # Note: This is a simplified version - in a real implementation,
        # you might want to reconstruct the CleanedFlightData object
        flight_summary = metadata['flight_data_summary']
        
        # Generate PDF report
        print("Generating PDF report...")
        pdf_generator = PDFReportGenerator(settings.reports_output_dir)
        
        # For now, we'll create a mock CleanedFlightData object
        # In a real implementation, you'd reconstruct it from saved data
        import pandas as pd
        from taxitakeoff.data.models import CleanedFlightData
        
        mock_df = pd.DataFrame({
            'flight_count': [flight_summary['flight_count']],
            'date_range': [flight_summary['date_range']],
            'destinations': [flight_summary['destinations']],
            'countries': [flight_summary['countries']]
        })
        mock_cleaned_data = CleanedFlightData.from_dataframe(mock_df)
        
        pdf_filepath = pdf_generator.generate_report(
            mock_cleaned_data,
            plot_filepaths,
            "Flight Analysis Report"
        )
        
        print(f"PDF report generated: {pdf_filepath}")
        
        # Send report
        print(f"Sending report via {delivery_method}...")
        delivery_service = create_delivery_service()
        
        subject = f"Flight Analysis Report - {metadata['generated_at']}"
        message = f"""
Flight Analysis Report

Summary:
- Total flights: {flight_summary['flight_count']}
- Date range: {flight_summary['date_range'][0]} to {flight_summary['date_range'][1]}
- Unique destinations: {len(flight_summary['destinations'])}
- Unique countries: {len(flight_summary['countries'])}

Generated plots:
{chr(10).join(f'- {plot["title"]}' for plot in metadata['plots'])}

Report generated at: {metadata['generated_at']}
        """.strip()
        
        success = delivery_service.send_report(
            delivery_method,
            pdf_filepath,
            subject,
            message
        )
        
        if success:
            print(f"Report sent successfully via {delivery_method}!")
        else:
            print(f"Failed to send report via {delivery_method}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error sending report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()