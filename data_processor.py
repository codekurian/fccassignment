"""
Data Processing and Transformation Script
Stage 2: Create Star Schema and transform data for analytics
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, dataframes):
        self.dataframes = dataframes
        self.star_schema_data = {}
        self.output_dir = Path("output/star_schema")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_star_schema(self):
        """Create Star Schema data warehouse"""
        logger.info("Creating Star Schema data warehouse...")
        
        # Create dimension tables
        self._create_user_dimension()
        self._create_time_dimension()
        self._create_channel_dimension()
        self._create_status_dimension()
        self._create_plan_dimension()
        self._create_payment_dimension()
        
        # Create fact tables
        self._create_play_session_facts()
        self._create_user_plan_facts()
        self._create_payment_facts()
        
        logger.info("Star Schema creation completed!")
        
    def _create_user_dimension(self):
        """Create user dimension table"""
        logger.info("Creating user dimension...")
        
        user_df = self.dataframes['user']
        user_reg_df = self.dataframes['user_registration']
        
        # Merge user and registration data
        user_dim = user_df.merge(
            user_reg_df, 
            on='user_id', 
            how='left',
            suffixes=('_user', '_reg')
        )
        
        # Add derived fields
        user_dim['is_registered'] = user_dim['user_registration_id'].notna()
        user_dim['registration_date'] = pd.to_datetime('2024-01-01')  # Placeholder
        
        # Clean up columns - prefer registration email if available
        user_dim['email'] = user_dim['email_reg'].fillna(user_dim['email_user'])
        
        user_dim = user_dim[[
            'user_id', 'ip_address', 'social_media_handle', 'email',
            'username', 'first_name', 'last_name', 'is_registered',
            'registration_date'
        ]]
        
        self.star_schema_data['user_dimension'] = user_dim
        user_dim.to_csv(self.output_dir / 'user_dimension.csv', index=False)
        logger.info(f"User dimension created: {len(user_dim)} rows")
        
    def _create_time_dimension(self):
        """Create time dimension table"""
        logger.info("Creating time dimension...")
        
        # Get all unique dates from play sessions
        play_sessions = self.dataframes['user_play_session']
        start_dates = pd.to_datetime(play_sessions['start_datetime']).dt.date
        end_dates = pd.to_datetime(play_sessions['end_datetime']).dt.date
        
        all_dates = pd.concat([start_dates, end_dates]).unique()
        date_range = pd.date_range(min(all_dates), max(all_dates), freq='D')
        
        time_dim = pd.DataFrame({
            'date_id': date_range.strftime('%Y%m%d').astype(int),
            'date': date_range,
            'year': date_range.year,
            'month': date_range.month,
            'day': date_range.day,
            'day_of_week': date_range.dayofweek,
            'quarter': date_range.quarter,
            'is_weekend': date_range.dayofweek.isin([5, 6])
        })
        
        self.star_schema_data['time_dimension'] = time_dim
        time_dim.to_csv(self.output_dir / 'time_dimension.csv', index=False)
        logger.info(f"Time dimension created: {len(time_dim)} rows")
        
    def _create_channel_dimension(self):
        """Create channel dimension table"""
        logger.info("Creating channel dimension...")
        
        channel_dim = self.dataframes['channel_code'].copy()
        channel_dim.columns = ['channel_id', 'channel_name', 'channel_name_fr']
        
        self.star_schema_data['channel_dimension'] = channel_dim
        channel_dim.to_csv(self.output_dir / 'channel_dimension.csv', index=False)
        logger.info(f"Channel dimension created: {len(channel_dim)} rows")
        
    def _create_status_dimension(self):
        """Create status dimension table"""
        logger.info("Creating status dimension...")
        
        status_dim = self.dataframes['status_code'].copy()
        status_dim.columns = ['status_id', 'status_name', 'status_name_fr']
        
        self.star_schema_data['status_dimension'] = status_dim
        status_dim.to_csv(self.output_dir / 'status_dimension.csv', index=False)
        logger.info(f"Status dimension created: {len(status_dim)} rows")
        
    def _create_plan_dimension(self):
        """Create plan dimension table"""
        logger.info("Creating plan dimension...")
        
        plan_df = self.dataframes['plan']
        freq_df = self.dataframes['plan_payment_frequency']
        
        plan_dim = plan_df.merge(
            freq_df, 
            on='payment_frequency_code', 
            how='left'
        )
        
        plan_dim.columns = [
            'plan_id', 'payment_frequency_code', 'cost_amount',
            'frequency_name', 'frequency_name_fr'
        ]
        
        self.star_schema_data['plan_dimension'] = plan_dim
        plan_dim.to_csv(self.output_dir / 'plan_dimension.csv', index=False)
        logger.info(f"Plan dimension created: {len(plan_dim)} rows")
        
    def _create_payment_dimension(self):
        """Create payment dimension table"""
        logger.info("Creating payment dimension...")
        
        payment_dim = self.dataframes['user_payment_detail'].copy()
        payment_dim.columns = [
            'payment_detail_id', 'payment_method_code', 
            'payment_method_value', 'payment_method_expiry'
        ]
        
        self.star_schema_data['payment_dimension'] = payment_dim
        payment_dim.to_csv(self.output_dir / 'payment_dimension.csv', index=False)
        logger.info(f"Payment dimension created: {len(payment_dim)} rows")
        
    def _create_play_session_facts(self):
        """Create play session fact table"""
        logger.info("Creating play session facts...")
        
        sessions = self.dataframes['user_play_session'].copy()
        
        # Add time dimensions
        sessions['start_date'] = pd.to_datetime(sessions['start_datetime']).dt.date
        sessions['end_date'] = pd.to_datetime(sessions['end_datetime']).dt.date
        sessions['date_id'] = sessions['start_date'].astype(str).str.replace('-', '').astype(int)
        
        # Calculate session duration
        sessions['session_duration_minutes'] = (
            pd.to_datetime(sessions['end_datetime']) - 
            pd.to_datetime(sessions['start_datetime'])
        ).dt.total_seconds() / 60
        
        # Create fact table
        session_facts = sessions[[
            'play_session_id', 'user_id', 'date_id', 'channel_code', 
            'status_code', 'total_score', 'session_duration_minutes'
        ]]
        
        session_facts.columns = [
            'session_id', 'user_id', 'date_id', 'channel_id', 
            'status_id', 'score', 'duration_minutes'
        ]
        
        self.star_schema_data['play_session_facts'] = session_facts
        session_facts.to_csv(self.output_dir / 'play_session_facts.csv', index=False)
        logger.info(f"Play session facts created: {len(session_facts)} rows")
        
    def _create_user_plan_facts(self):
        """Create user plan fact table"""
        logger.info("Creating user plan facts...")
        
        user_plans = self.dataframes['user_plan'].copy()
        user_reg = self.dataframes['user_registration']
        
        # Get user_id from registration
        plan_facts = user_plans.merge(
            user_reg[['user_registration_id', 'user_id']], 
            on='user_registration_id', 
            how='left'
        )
        
        # Add time dimensions
        plan_facts['start_date'] = pd.to_datetime(plan_facts['start_date']).dt.date
        
        # Handle placeholder end dates (9999-01-01) - treat as active subscriptions
        end_dates = pd.to_datetime(plan_facts['end_date'], errors='coerce')
        plan_facts['end_date'] = end_dates.dt.date
        
        # For placeholder dates, use current date or reasonable end date
        placeholder_mask = plan_facts['end_date'].isna()
        if placeholder_mask.any():
            plan_facts.loc[placeholder_mask, 'end_date'] = pd.to_datetime('2024-12-31').date()
        
        plan_facts['date_id'] = plan_facts['start_date'].astype(str).str.replace('-', '').astype(int)
        
        # Calculate plan duration
        plan_facts['plan_duration_days'] = (
            pd.to_datetime(plan_facts['end_date']) - 
            pd.to_datetime(plan_facts['start_date'])
        ).dt.days
        
        plan_facts = plan_facts[[
            'user_registration_id', 'user_id', 'plan_id', 'payment_detail_id',
            'date_id', 'plan_duration_days'
        ]]
        
        self.star_schema_data['user_plan_facts'] = plan_facts
        plan_facts.to_csv(self.output_dir / 'user_plan_facts.csv', index=False)
        logger.info(f"User plan facts created: {len(plan_facts)} rows")
        
    def _create_payment_facts(self):
        """Create payment fact table"""
        logger.info("Creating payment facts...")
        
        # This would typically include payment transactions
        # For now, we'll create a simple payment fact table
        payment_facts = self.dataframes['user_plan'].copy()
        
        # Add plan cost information
        plans = self.dataframes['plan']
        payment_facts = payment_facts.merge(
            plans[['plan_id', 'cost_amount']], 
            on='plan_id', 
            how='left'
        )
        
        payment_facts['payment_date'] = pd.to_datetime(payment_facts['start_date']).dt.date
        payment_facts['date_id'] = payment_facts['payment_date'].astype(str).str.replace('-', '').astype(int)
        
        payment_facts = payment_facts[[
            'user_registration_id', 'payment_detail_id', 'plan_id',
            'date_id', 'cost_amount'
        ]]
        
        self.star_schema_data['payment_facts'] = payment_facts
        payment_facts.to_csv(self.output_dir / 'payment_facts.csv', index=False)
        logger.info(f"Payment facts created: {len(payment_facts)} rows")
        
    def generate_analytics_datasets(self):
        """Generate analytics datasets for insights"""
        logger.info("Generating analytics datasets...")
        
        analytics_dir = Path("output/analytics")
        analytics_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate play sessions by channel
        self._generate_play_sessions_by_channel(analytics_dir)
        
        # Generate user payment analysis
        self._generate_user_payment_analysis(analytics_dir)
        
        # Generate revenue analysis
        self._generate_revenue_analysis(analytics_dir)
        
        logger.info("Analytics datasets generated!")
        
    def _generate_play_sessions_by_channel(self, output_dir):
        """Generate play sessions analysis by channel"""
        session_facts = self.star_schema_data['play_session_facts']
        channel_dim = self.star_schema_data['channel_dimension']
        
        # Merge with channel dimension
        sessions_by_channel = session_facts.merge(
            channel_dim, 
            left_on='channel_id', 
            right_on='channel_id', 
            how='left'
        )
        
        # Aggregate by channel
        channel_analysis = sessions_by_channel.groupby('channel_name').agg({
            'session_id': 'count',
            'score': ['sum', 'mean', 'median'],
            'duration_minutes': ['sum', 'mean', 'median']
        }).round(2)
        
        channel_analysis.columns = [
            'total_sessions', 'total_score', 'avg_score', 'median_score',
            'total_duration_minutes', 'avg_duration_minutes', 'median_duration_minutes'
        ]
        
        channel_analysis.to_csv(output_dir / 'play_sessions_by_channel.csv')
        logger.info("Play sessions by channel analysis generated")
        
    def _generate_user_payment_analysis(self, output_dir):
        """Generate user payment choice analysis"""
        user_plans = self.star_schema_data['user_plan_facts']
        plan_dim = self.star_schema_data['plan_dimension']
        
        # Merge with plan dimension
        payment_analysis = user_plans.merge(
            plan_dim, 
            on='plan_id', 
            how='left'
        )
        
        # Aggregate by payment frequency
        payment_choice_analysis = payment_analysis.groupby('frequency_name').agg({
            'user_id': 'count',
            'cost_amount': ['sum', 'mean'],
            'plan_duration_days': ['mean', 'median']
        }).round(2)
        
        payment_choice_analysis.columns = [
            'total_users', 'total_revenue', 'avg_cost',
            'avg_duration_days', 'median_duration_days'
        ]
        
        payment_choice_analysis.to_csv(output_dir / 'user_payment_analysis.csv')
        logger.info("User payment analysis generated")
        
    def _generate_revenue_analysis(self, output_dir):
        """Generate revenue analysis"""
        payment_facts = self.star_schema_data['payment_facts']
        time_dim = self.star_schema_data['time_dimension']
        
        # Merge with time dimension
        revenue_analysis = payment_facts.merge(
            time_dim, 
            on='date_id', 
            how='left'
        )
        
        # Monthly revenue
        monthly_revenue = revenue_analysis.groupby(['year', 'month']).agg({
            'cost_amount': 'sum',
            'user_registration_id': 'count'
        }).round(2)
        
        monthly_revenue.columns = ['total_revenue', 'total_transactions']
        monthly_revenue.to_csv(output_dir / 'monthly_revenue.csv')
        
        # Quarterly revenue
        quarterly_revenue = revenue_analysis.groupby(['year', 'quarter']).agg({
            'cost_amount': 'sum',
            'user_registration_id': 'count'
        }).round(2)
        
        quarterly_revenue.columns = ['total_revenue', 'total_transactions']
        quarterly_revenue.to_csv(output_dir / 'quarterly_revenue.csv')
        
        logger.info("Revenue analysis generated")

def main():
    """Main function to run Stage 2"""
    logger.info("Starting Stage 2: Data Processing & Transformation")
    
    # This would typically be called from main.py with loaded dataframes
    # For standalone testing, we'll load the data
    from data_loader import DataLoader
    
    loader = DataLoader()
    dataframes = loader.load_all_csv_files()
    
    processor = DataProcessor(dataframes)
    processor.create_star_schema()
    processor.generate_analytics_datasets()
    
    logger.info("Stage 2 completed successfully!")
    return processor.star_schema_data

if __name__ == "__main__":
    star_schema_data = main() 