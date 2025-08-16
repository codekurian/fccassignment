"""
Data Loading and Validation Script
Stage 1: Load all CSV data and perform basic validation
"""

import pandas as pd
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, data_dir="assignment_docs"):
        self.data_dir = Path(data_dir)
        self.dataframes = {}
        self.validation_results = {}
        
    def load_all_csv_files(self):
        """Load all CSV files from the assignment_docs directory"""
        logger.info("Starting to load CSV files...")
        
        csv_files = list(self.data_dir.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files")
        
        for csv_file in csv_files:
            try:
                df_name = csv_file.stem  # Get filename without extension
                logger.info(f"Loading {csv_file.name}...")
                
                # Load CSV file
                df = pd.read_csv(csv_file)
                self.dataframes[df_name] = df
                
                logger.info(f"Successfully loaded {csv_file.name} with {len(df)} rows and {len(df.columns)} columns")
                
            except Exception as e:
                logger.error(f"Error loading {csv_file.name}: {str(e)}")
                raise
        
        return self.dataframes
    
    def validate_data(self):
        """Perform basic data validation on all loaded dataframes"""
        logger.info("Starting data validation...")
        
        for df_name, df in self.dataframes.items():
            logger.info(f"Validating {df_name}...")
            
            validation_result = {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'null_counts': df.isnull().sum().to_dict(),
                'data_types': df.dtypes.to_dict(),
                'duplicate_rows': df.duplicated().sum(),
                'memory_usage': df.memory_usage(deep=True).sum()
            }
            
            self.validation_results[df_name] = validation_result
            
            logger.info(f"Validation complete for {df_name}")
        
        return self.validation_results
    
    def check_data_relationships(self):
        """Check basic relationships between tables"""
        logger.info("Checking data relationships...")
        
        relationships = {}
        
        # Check user relationships
        if 'user' in self.dataframes and 'user_registration' in self.dataframes:
            user_ids = set(self.dataframes['user']['user_id'])
            reg_user_ids = set(self.dataframes['user_registration']['user_id'])
            
            relationships['user_registration'] = {
                'users_in_registration': len(user_ids.intersection(reg_user_ids)),
                'users_only_in_user': len(user_ids - reg_user_ids),
                'users_only_in_registration': len(reg_user_ids - user_ids)
            }
        
        # Check play session relationships
        if 'user_play_session' in self.dataframes and 'user' in self.dataframes:
            session_user_ids = set(self.dataframes['user_play_session']['user_id'])
            user_ids = set(self.dataframes['user']['user_id'])
            
            relationships['play_sessions'] = {
                'sessions_with_valid_users': len(session_user_ids.intersection(user_ids)),
                'sessions_without_users': len(session_user_ids - user_ids)
            }
        
        # Check plan relationships
        if 'user_plan' in self.dataframes and 'plan' in self.dataframes:
            plan_ids = set(self.dataframes['plan']['plan_id'])
            user_plan_ids = set(self.dataframes['user_plan']['plan_id'])
            
            relationships['user_plans'] = {
                'valid_plan_references': len(user_plan_ids.intersection(plan_ids)),
                'invalid_plan_references': len(user_plan_ids - plan_ids)
            }
        
        return relationships
    
    def generate_validation_report(self):
        """Generate a comprehensive validation report"""
        logger.info("Generating validation report...")
        
        report = {
            'summary': {
                'total_files_loaded': len(self.dataframes),
                'files_loaded': list(self.dataframes.keys())
            },
            'validation_results': self.validation_results,
            'relationships': self.check_data_relationships()
        }
        
        return report
    
    def print_validation_summary(self):
        """Print a summary of validation results"""
        print("\n" + "="*50)
        print("DATA VALIDATION SUMMARY")
        print("="*50)
        
        print(f"\nFiles Loaded: {len(self.dataframes)}")
        for df_name in self.dataframes.keys():
            print(f"  - {df_name}")
        
        print(f"\nData Quality Check:")
        for df_name, result in self.validation_results.items():
            print(f"\n{df_name.upper()}:")
            print(f"  Rows: {result['total_rows']:,}")
            print(f"  Columns: {result['total_columns']}")
            print(f"  Duplicates: {result['duplicate_rows']}")
            
            # Check for null values
            null_cols = [col for col, count in result['null_counts'].items() if count > 0]
            if null_cols:
                print(f"  Columns with nulls: {len(null_cols)}")
                for col in null_cols[:3]:  # Show first 3
                    print(f"    - {col}: {result['null_counts'][col]} nulls")
                if len(null_cols) > 3:
                    print(f"    ... and {len(null_cols) - 3} more")
            else:
                print(f"  No null values found")

def main():
    """Main function to run Stage 1"""
    logger.info("Starting Stage 1: Data Loading & Validation")
    
    # Initialize data loader
    loader = DataLoader()
    
    try:
        # Load all CSV files
        dataframes = loader.load_all_csv_files()
        
        # Validate data
        validation_results = loader.validate_data()
        
        # Generate and print report
        report = loader.generate_validation_report()
        loader.print_validation_summary()
        
        logger.info("Stage 1 completed successfully!")
        
        return dataframes, validation_results
        
    except Exception as e:
        logger.error(f"Stage 1 failed: {str(e)}")
        raise

if __name__ == "__main__":
    dataframes, validation_results = main() 