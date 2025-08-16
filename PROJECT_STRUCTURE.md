# Project Structure

```
fccassignment/
├── README.md                    # Main documentation
├── PROJECT_STRUCTURE.md         # This file - project overview
├── requirements.txt             # Python dependencies
├── setup.py                     # Automated setup script
├── main.py                      # Main execution script
├── run.bat                      # Windows batch file for easy execution
│
├── assignment_docs/             # Input data files
│   ├── user.csv
│   ├── user_registration.csv
│   ├── user_plan.csv
│   ├── user_payment_detail.csv
│   ├── user_play_session.csv
│   ├── plan.csv
│   ├── status_code.csv
│   ├── channel_code.csv
│   └── plan_payment_frequency.csv
│
├── data_loader.py               # Stage 1: Data loading and validation
├── data_processor.py            # Stage 2: Data processing and transformation
├── analytics_engine.py          # Stage 3: Analytics and insights
├── quality_checker.py           # Stage 4: Quality assurance
│
└── output/                      # Generated output files
    ├── star_schema/             # Data warehouse tables
    ├── analytics/               # Analytics datasets
    ├── forecasting/             # Forecasting data
    └── reports/                 # Quality reports
```

## Quick Start for Interviewer

### Option 1: One-Click Execution (Windows)
```bash
run.bat
```

### Option 2: Command Line
```bash
# Setup
python setup.py

# Run all stages
python main.py
```

### Option 3: Individual Stages
```bash
python data_loader.py          # Stage 1
python data_processor.py       # Stage 2
python analytics_engine.py     # Stage 3
python quality_checker.py      # Stage 4
```

## Key Files Explained

- **`main.py`**: Orchestrates all 4 stages of the pipeline
- **`setup.py`**: Installs dependencies and prepares environment
- **`data_loader.py`**: Loads CSV files and validates data quality
- **`data_processor.py`**: Creates Star Schema and transforms data
- **`analytics_engine.py`**: Generates insights and forecasting data
- **`quality_checker.py`**: Performs final quality checks and reporting

## Expected Output

After successful execution, you'll find:
- **Console output**: Progress through all stages
- **`output/` directory**: All generated CSV files and reports
- **`execution.log`**: Detailed execution log
- **Quality reports**: Data validation and quality metrics 