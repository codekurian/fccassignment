"""
Dice Game Data Processing Application - Main Execution Script
2-Hour Interview Assignment

This script runs all stages of the data processing pipeline:
1. Data Loading & Validation
2. Data Processing & Transformation  
3. Analytics & Insights Generation
4. Quality Check & Documentation

Usage: python main.py
"""

import sys
import os
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    
    print("=" * 80)
    print("DICE GAME DATA PROCESSING APPLICATION")
    print("2-Hour Interview Assignment")
    print("=" * 80)
    print(f"Execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Stage 1: Data Loading & Validation
        print("🔄 STAGE 1: Data Loading & Validation")
        print("-" * 50)
        
        from data_loader import DataLoader
        loader = DataLoader()
        loader.load_all_csv_files()
        loader.validate_data()
        loader.print_validation_summary()
        
        print("✅ Stage 1 completed successfully!")
        print()
        
        # Stage 2: Data Processing & Transformation
        print("🔄 STAGE 2: Data Processing & Transformation")
        print("-" * 50)
        
        from data_processor import DataProcessor
        processor = DataProcessor(loader.dataframes)
        processor.create_star_schema()
        processor.generate_analytics_datasets()
        
        print("✅ Stage 2 completed successfully!")
        print()
        
        # Stage 3: Analytics & Insights
        print("🔄 STAGE 3: Analytics & Insights Generation")
        print("-" * 50)
        
        from analytics_engine import AnalyticsEngine
        analytics = AnalyticsEngine()
        analytics.generate_insights()
        analytics.create_forecasting_data()
        
        print("✅ Stage 3 completed successfully!")
        print()
        
        # Stage 4: Quality Check & Documentation
        print("🔄 STAGE 4: Quality Check & Documentation")
        print("-" * 50)
        
        from quality_checker import QualityChecker
        checker = QualityChecker()
        checker.run_quality_checks()
        checker.generate_final_report()
        
        print("✅ Stage 4 completed successfully!")
        print()
        
        # Final Summary
        print("=" * 80)
        print("🎉 ALL STAGES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("📁 OUTPUT FILES GENERATED:")
        print("  - output/star_schema/ (Data warehouse tables)")
        print("  - output/analytics/ (Analytics datasets)")
        print("  - output/forecasting/ (Forecasting data)")
        print("  - output/reports/ (Quality reports)")
        print("  - execution.log (Execution log)")
        print()
        print("📊 KEY INSIGHTS:")
        print("  - Play sessions by channel analysis")
        print("  - User payment choice analysis") 
        print("  - Revenue forecasting for 2025")
        print("  - User behavioral characteristics")
        print()
        print(f"⏱️  Total execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        print(f"❌ ERROR: {str(e)}")
        print("Check execution.log for detailed error information.")
        sys.exit(1)

if __name__ == "__main__":
    main() 