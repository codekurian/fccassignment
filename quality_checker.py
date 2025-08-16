"""
Quality Check and Documentation Script
Stage 4: Perform final quality checks and generate comprehensive reports
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QualityChecker:
    def __init__(self):
        self.output_dir = Path("output/reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.quality_results = {}
        
    def run_quality_checks(self):
        """Run comprehensive quality checks on all outputs"""
        logger.info("Running quality checks...")
        
        # Check data integrity
        self._check_data_integrity()
        
        # Check output completeness
        self._check_output_completeness()
        
        # Check data quality metrics
        self._check_data_quality_metrics()
        
        # Check business logic validation
        self._check_business_logic()
        
        logger.info("Quality checks completed!")
        
    def _check_data_integrity(self):
        """Check data integrity across all outputs"""
        logger.info("Checking data integrity...")
        
        integrity_checks = {
            'star_schema_files': self._check_star_schema_integrity(),
            'analytics_files': self._check_analytics_integrity(),
            'forecasting_files': self._check_forecasting_integrity()
        }
        
        self.quality_results['data_integrity'] = integrity_checks
        
        # Overall integrity score
        total_checks = sum(len(checks) for checks in integrity_checks.values())
        passed_checks = sum(
            sum(1 for check in checks.values() if check['status'] == 'PASS')
            for checks in integrity_checks.values()
        )
        
        integrity_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        self.quality_results['integrity_score'] = integrity_score
        logger.info(f"Data integrity score: {integrity_score:.1f}%")
        
    def _check_star_schema_integrity(self):
        """Check Star Schema data integrity"""
        star_schema_dir = Path("output/star_schema")
        checks = {}
        
        expected_files = [
            'user_dimension.csv',
            'time_dimension.csv', 
            'channel_dimension.csv',
            'status_dimension.csv',
            'plan_dimension.csv',
            'payment_dimension.csv',
            'play_session_facts.csv',
            'user_plan_facts.csv',
            'payment_facts.csv'
        ]
        
        for file_name in expected_files:
            file_path = star_schema_dir / file_name
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    checks[file_name] = {
                        'status': 'PASS',
                        'rows': len(df),
                        'columns': len(df.columns),
                        'nulls': df.isnull().sum().sum(),
                        'duplicates': df.duplicated().sum()
                    }
                except Exception as e:
                    checks[file_name] = {
                        'status': 'FAIL',
                        'error': str(e)
                    }
            else:
                checks[file_name] = {
                    'status': 'FAIL',
                    'error': 'File not found'
                }
        
        return checks
        
    def _check_analytics_integrity(self):
        """Check analytics data integrity"""
        analytics_dir = Path("output/analytics")
        checks = {}
        
        expected_files = [
            'play_sessions_by_channel.csv',
            'user_payment_analysis.csv',
            'monthly_revenue.csv',
            'quarterly_revenue.csv'
        ]
        
        for file_name in expected_files:
            file_path = analytics_dir / file_name
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    checks[file_name] = {
                        'status': 'PASS',
                        'rows': len(df),
                        'columns': len(df.columns),
                        'nulls': df.isnull().sum().sum()
                    }
                except Exception as e:
                    checks[file_name] = {
                        'status': 'FAIL',
                        'error': str(e)
                    }
            else:
                checks[file_name] = {
                    'status': 'FAIL',
                    'error': 'File not found'
                }
        
        return checks
        
    def _check_forecasting_integrity(self):
        """Check forecasting data integrity"""
        forecasting_dir = Path("output/forecasting")
        checks = {}
        
        expected_files = [
            'user_projection_2025.csv',
            'revenue_projection_2025.csv',
            'session_projection_2025.csv',
            'forecasting_insights.txt'
        ]
        
        for file_name in expected_files:
            file_path = forecasting_dir / file_name
            if file_path.exists():
                try:
                    if file_name.endswith('.csv'):
                        df = pd.read_csv(file_path)
                        checks[file_name] = {
                            'status': 'PASS',
                            'rows': len(df),
                            'columns': len(df.columns),
                            'nulls': df.isnull().sum().sum()
                        }
                    else:
                        # Text file
                        with open(file_path, 'r') as f:
                            content = f.read()
                        checks[file_name] = {
                            'status': 'PASS',
                            'size_bytes': len(content),
                            'lines': len(content.split('\n'))
                        }
                except Exception as e:
                    checks[file_name] = {
                        'status': 'FAIL',
                        'error': str(e)
                    }
            else:
                checks[file_name] = {
                    'status': 'FAIL',
                    'error': 'File not found'
                }
        
        return checks
        
    def _check_output_completeness(self):
        """Check if all required outputs are generated"""
        logger.info("Checking output completeness...")
        
        completeness_checks = {
            'star_schema_complete': self._check_star_schema_completeness(),
            'analytics_complete': self._check_analytics_completeness(),
            'forecasting_complete': self._check_forecasting_completeness()
        }
        
        self.quality_results['completeness'] = completeness_checks
        
        # Overall completeness score
        total_checks = len(completeness_checks)
        passed_checks = sum(1 for check in completeness_checks.values() if check['status'] == 'PASS')
        completeness_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        self.quality_results['completeness_score'] = completeness_score
        logger.info(f"Output completeness score: {completeness_score:.1f}%")
        
    def _check_star_schema_completeness(self):
        """Check if Star Schema is complete"""
        star_schema_dir = Path("output/star_schema")
        required_files = [
            'user_dimension.csv',
            'time_dimension.csv',
            'channel_dimension.csv',
            'status_dimension.csv',
            'plan_dimension.csv',
            'payment_dimension.csv',
            'play_session_facts.csv',
            'user_plan_facts.csv',
            'payment_facts.csv'
        ]
        
        missing_files = []
        for file_name in required_files:
            if not (star_schema_dir / file_name).exists():
                missing_files.append(file_name)
        
        if missing_files:
            return {
                'status': 'FAIL',
                'missing_files': missing_files
            }
        else:
            return {
                'status': 'PASS',
                'message': 'All Star Schema files present'
            }
            
    def _check_analytics_completeness(self):
        """Check if analytics outputs are complete"""
        analytics_dir = Path("output/analytics")
        required_files = [
            'play_sessions_by_channel.csv',
            'user_payment_analysis.csv',
            'monthly_revenue.csv',
            'quarterly_revenue.csv'
        ]
        
        missing_files = []
        for file_name in required_files:
            if not (analytics_dir / file_name).exists():
                missing_files.append(file_name)
        
        if missing_files:
            return {
                'status': 'FAIL',
                'missing_files': missing_files
            }
        else:
            return {
                'status': 'PASS',
                'message': 'All analytics files present'
            }
            
    def _check_forecasting_completeness(self):
        """Check if forecasting outputs are complete"""
        forecasting_dir = Path("output/forecasting")
        required_files = [
            'user_projection_2025.csv',
            'revenue_projection_2025.csv',
            'session_projection_2025.csv',
            'forecasting_insights.txt'
        ]
        
        missing_files = []
        for file_name in required_files:
            if not (forecasting_dir / file_name).exists():
                missing_files.append(file_name)
        
        if missing_files:
            return {
                'status': 'FAIL',
                'missing_files': missing_files
            }
        else:
            return {
                'status': 'PASS',
                'message': 'All forecasting files present'
            }
            
    def _check_data_quality_metrics(self):
        """Check data quality metrics"""
        logger.info("Checking data quality metrics...")
        
        quality_metrics = {
            'null_values': self._check_null_values(),
            'data_types': self._check_data_types(),
            'value_ranges': self._check_value_ranges(),
            'business_rules': self._check_business_rules()
        }
        
        self.quality_results['data_quality'] = quality_metrics
        
    def _check_null_values(self):
        """Check for unexpected null values"""
        checks = {}
        
        # Check key dimension tables
        key_files = [
            ('output/star_schema/user_dimension.csv', 'user_id'),
            ('output/star_schema/channel_dimension.csv', 'channel_id'),
            ('output/star_schema/plan_dimension.csv', 'plan_id')
        ]
        
        for file_path, key_column in key_files:
            if Path(file_path).exists():
                df = pd.read_csv(file_path)
                null_count = df[key_column].isnull().sum()
                checks[file_path] = {
                    'status': 'PASS' if null_count == 0 else 'FAIL',
                    'null_count': null_count
                }
        
        return checks
        
    def _check_data_types(self):
        """Check data types are appropriate"""
        checks = {}
        
        # Check numeric columns are numeric
        numeric_files = [
            ('output/star_schema/play_session_facts.csv', ['score', 'duration_minutes']),
            ('output/star_schema/payment_facts.csv', ['cost_amount'])
        ]
        
        for file_path, numeric_columns in numeric_files:
            if Path(file_path).exists():
                df = pd.read_csv(file_path)
                all_numeric = all(pd.api.types.is_numeric_dtype(df[col]) for col in numeric_columns)
                checks[file_path] = {
                    'status': 'PASS' if all_numeric else 'FAIL',
                    'columns_checked': numeric_columns
                }
        
        return checks
        
    def _check_value_ranges(self):
        """Check value ranges are reasonable"""
        checks = {}
        
        # Check score ranges
        if Path('output/star_schema/play_session_facts.csv').exists():
            df = pd.read_csv('output/star_schema/play_session_facts.csv')
            score_range = df['score'].describe()
            checks['score_range'] = {
                'status': 'PASS' if score_range['min'] >= 0 else 'FAIL',
                'min': score_range['min'],
                'max': score_range['max'],
                'mean': score_range['mean']
            }
        
        # Check duration ranges
        if Path('output/star_schema/play_session_facts.csv').exists():
            df = pd.read_csv('output/star_schema/play_session_facts.csv')
            duration_range = df['duration_minutes'].describe()
            checks['duration_range'] = {
                'status': 'PASS' if duration_range['min'] >= 0 else 'FAIL',
                'min': duration_range['min'],
                'max': duration_range['max'],
                'mean': duration_range['mean']
            }
        
        return checks
        
    def _check_business_rules(self):
        """Check business logic rules"""
        checks = {}
        
        # Check that all sessions have valid users
        if Path('output/star_schema/play_session_facts.csv').exists():
            session_df = pd.read_csv('output/star_schema/play_session_facts.csv')
            user_df = pd.read_csv('output/star_schema/user_dimension.csv')
            
            valid_users = set(user_df['user_id'])
            session_users = set(session_df['user_id'])
            invalid_sessions = session_users - valid_users
            
            checks['session_user_validity'] = {
                'status': 'PASS' if len(invalid_sessions) == 0 else 'FAIL',
                'invalid_sessions': len(invalid_sessions)
            }
        
        return checks
        
    def _check_business_logic(self):
        """Check business logic validation"""
        logger.info("Checking business logic...")
        
        business_checks = {
            'revenue_consistency': self._check_revenue_consistency(),
            'user_consistency': self._check_user_consistency(),
            'session_consistency': self._check_session_consistency()
        }
        
        self.quality_results['business_logic'] = business_checks
        
    def _check_revenue_consistency(self):
        """Check revenue calculations are consistent"""
        checks = {}
        
        # Check that total revenue matches across different aggregations
        if Path('output/analytics/monthly_revenue.csv').exists():
            monthly_df = pd.read_csv('output/analytics/monthly_revenue.csv')
            total_revenue = monthly_df['total_revenue'].sum()
            
            if Path('output/star_schema/payment_facts.csv').exists():
                payment_df = pd.read_csv('output/star_schema/payment_facts.csv')
                payment_total = payment_df['cost_amount'].sum()
                
                # Allow for small rounding differences
                difference = abs(total_revenue - payment_total)
                checks['revenue_consistency'] = {
                    'status': 'PASS' if difference < 1.0 else 'FAIL',
                    'difference': difference
                }
        
        return checks
        
    def _check_user_consistency(self):
        """Check user counts are consistent"""
        checks = {}
        
        # Check user counts across different files
        if Path('output/star_schema/user_dimension.csv').exists():
            user_df = pd.read_csv('output/star_schema/user_dimension.csv')
            total_users = len(user_df)
            
            if Path('output/star_schema/play_session_facts.csv').exists():
                session_df = pd.read_csv('output/star_schema/play_session_facts.csv')
                unique_session_users = session_df['user_id'].nunique()
                
                checks['user_session_consistency'] = {
                    'status': 'PASS' if unique_session_users <= total_users else 'FAIL',
                    'total_users': total_users,
                    'session_users': unique_session_users
                }
        
        return checks
        
    def _check_session_consistency(self):
        """Check session data consistency"""
        checks = {}
        
        # Check that session durations are positive
        if Path('output/star_schema/play_session_facts.csv').exists():
            session_df = pd.read_csv('output/star_schema/play_session_facts.csv')
            negative_durations = (session_df['duration_minutes'] < 0).sum()
            
            checks['session_duration_consistency'] = {
                'status': 'PASS' if negative_durations == 0 else 'FAIL',
                'negative_durations': negative_durations
            }
        
        return checks
        
    def generate_final_report(self):
        """Generate comprehensive final report"""
        logger.info("Generating final quality report...")
        
        # Calculate overall quality score
        integrity_score = self.quality_results.get('integrity_score', 0)
        completeness_score = self.quality_results.get('completeness_score', 0)
        
        # Weighted overall score
        overall_score = (integrity_score * 0.6) + (completeness_score * 0.4)
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': overall_score,
            'integrity_score': integrity_score,
            'completeness_score': completeness_score,
            'quality_results': self.quality_results,
            'summary': self._generate_summary()
        }
        
        # Save detailed report
        with open(self.output_dir / 'quality_report.json', 'w') as f:
            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy_types(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return obj
            
            # Convert the report recursively
            def convert_dict(d):
                if isinstance(d, dict):
                    return {k: convert_dict(v) for k, v in d.items()}
                elif isinstance(d, list):
                    return [convert_dict(v) for v in d]
                else:
                    return convert_numpy_types(d)
            
            converted_report = convert_dict(report)
            json.dump(converted_report, f, indent=2)
        
        # Save human-readable summary
        self._save_human_readable_report(report)
        
        logger.info(f"Final quality report generated. Overall score: {overall_score:.1f}%")
        return report
        
    def _generate_summary(self):
        """Generate executive summary"""
        summary = {
            'total_files_checked': 0,
            'files_passed': 0,
            'files_failed': 0,
            'critical_issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Count files and issues
        for check_type, checks in self.quality_results.items():
            if isinstance(checks, dict) and 'status' not in checks:
                for check_name, check_result in checks.items():
                    if isinstance(check_result, dict) and 'status' in check_result:
                        summary['total_files_checked'] += 1
                        if check_result['status'] == 'PASS':
                            summary['files_passed'] += 1
                        else:
                            summary['files_failed'] += 1
                            if 'error' in check_result:
                                summary['critical_issues'].append(f"{check_name}: {check_result['error']}")
        
        # Add recommendations
        if summary['files_failed'] > 0:
            summary['recommendations'].append("Review failed quality checks and fix data issues")
        else:
            summary['recommendations'].append("All quality checks passed - data is ready for analysis")
        
        summary['recommendations'].extend([
            "Validate business logic with stakeholders",
            "Perform user acceptance testing on generated insights",
            "Monitor data quality metrics in production"
        ])
        
        return summary
        
    def _save_human_readable_report(self, report):
        """Save human-readable quality report"""
        with open(self.output_dir / 'quality_summary.txt', 'w') as f:
            f.write("QUALITY ASSURANCE REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Report Generated: {report['timestamp']}\n")
            f.write(f"Overall Quality Score: {report['overall_score']:.1f}%\n")
            f.write(f"Data Integrity Score: {report['integrity_score']:.1f}%\n")
            f.write(f"Output Completeness Score: {report['completeness_score']:.1f}%\n\n")
            
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 20 + "\n")
            summary = report['summary']
            f.write(f"Total Files Checked: {summary['total_files_checked']}\n")
            f.write(f"Files Passed: {summary['files_passed']}\n")
            f.write(f"Files Failed: {summary['files_failed']}\n\n")
            
            if summary['critical_issues']:
                f.write("CRITICAL ISSUES:\n")
                for issue in summary['critical_issues']:
                    f.write(f"  - {issue}\n")
                f.write("\n")
            
            if summary['warnings']:
                f.write("WARNINGS:\n")
                for warning in summary['warnings']:
                    f.write(f"  - {warning}\n")
                f.write("\n")
            
            f.write("RECOMMENDATIONS:\n")
            for rec in summary['recommendations']:
                f.write(f"  - {rec}\n")

def main():
    """Main function to run Stage 4"""
    logger.info("Starting Stage 4: Quality Check & Documentation")
    
    checker = QualityChecker()
    checker.run_quality_checks()
    report = checker.generate_final_report()
    
    logger.info("Stage 4 completed successfully!")
    return report

if __name__ == "__main__":
    report = main() 