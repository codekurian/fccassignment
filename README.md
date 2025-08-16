# Dice Game Data Processing Application

## Project Overview

This project involves building a data processing application for a fictional game app development company's "Dice Game" app. The app has been publicly available since 2024, supporting both limited free-to-play and unlimited subscription-based play, accessible via browser and mobile app.

**Objective**: Use 2024 data to forecast expectations for 2025, identify areas of performance/underperformance, and glean user behavioral characteristics.

## Assignment Requirements

### Core Tasks
1. **Data Model Analysis**: Analyze the source data model to understand collected data
2. **Data Processing Application Development**: 
   - Use `pyspark`, `pandas`, or another Python-based data processing framework
   - Process and transform data into a local "data warehouse" or "data lake"
   - Structure using either Data Vault 2.0 or Star Schema (Dimensional) patterns
   - Output to local files (CSV or Parquet)
3. **Quality Assurance**: Implement unit tests and data quality validations
4. **Insight Generation**: Derive 2-3 key insights for 2025 planning

### Expected Insights Examples
- Number of play sessions: Online vs. Mobile App
- Registered users' payment choices: One-time payment vs. subscription
- Total gross revenue generated from the app

## What Needs to be Built

### Core Components

1. **Data Processing Engine**
   - CSV data ingestion and validation
   - Data transformation and cleaning
   - Error handling and logging




4. **Game Session Analytics**
   - Play session tracking (Browser vs Mobile)
   - Session status monitoring (Completed, Aborted, Timeout)
   - Score tracking and analysis
   - Performance metrics calculation

5. **Reporting and Analytics Dashboard**
   - User engagement metrics
   - Revenue analytics
   - Platform usage statistics
   - Custom report generation

## Data Model Overview

Based on the Entity-Relationship Diagram (ERD), the database schema consists of the following entities:

### Core Entities

#### User Management
- **`user`**: Basic user information (user_id, ip_address, social_media_handle, email)
- **`user_registration`**: Extended user profiles (user_registration_id, user_id, username, email, first_name, last_name)

#### Payment & Subscription
- **`user_payment_detail`**: Payment method information (payment_detail_id, payment_method_code, payment_method_value, payment_method_expiry)
- **`payment_frequency`**: Payment frequency codes (payment_frequency_code, english_description, french_description)
- **`plan`**: Subscription plans (plan_id, payment_frequency_code, cost_amount)
- **`user_plan`**: User subscription management (user_registration_id, payment_detail_id, plan_id, start_date, end_date)

#### Game Sessions
- **`user_play_session`**: Game session tracking (play_session_id, user_id, start_datetime, end_datetime, channel_code, status_code, total_score)
- **`play_session_channel_code`**: Channel types (play_session_channel_code, english_description, french_description)
- **`play_session_status_code`**: Session statuses (play_session_status_code, english_description, french_description)

### Key Relationships
- **User → Play Sessions**: One-to-many (users can have multiple play sessions)
- **User → User Registration**: One-to-one (each user has one registration record)
- **User Registration → User Plans**: One-to-many (users can have multiple plans over time)
- **Plan → User Plans**: One-to-many (plans can be subscribed to by multiple users)
- **Payment Detail → User Plans**: One-to-many (payment methods can be used for multiple plans)
- **Channel Code → Play Sessions**: One-to-many (channel codes apply to multiple sessions)
- **Status Code → Play Sessions**: One-to-many (status codes apply to multiple sessions)




## Development Stages (2-Hour Assignment)

### Stage 1: Data Loading & Validation (30 minutes)
**Goal**: Load all CSV data and perform basic validation

#### Tasks:
- [ ] Set up Python environment with pandas/pyspark
- [ ] Load all CSV files from assignment_docs/
- [ ] Perform basic data validation (check for nulls, data types, relationships)
- [ ] Create data quality summary report

#### Deliverables:
- Working data loading script
- Data validation summary
- Basic data quality report

#### Success Criteria:
- All CSV files load without errors
- Data relationships are validated
- No critical data quality issues found

---

### Stage 2: Data Processing & Transformation (45 minutes)
**Goal**: Transform data into forecasting-ready format

#### Tasks:
- [ ] Choose Data Vault 2.0 or Star Schema approach
- [ ] Create data transformation pipeline
- [ ] Generate forecasting datasets (CSV files)
- [ ] Implement basic ETL processes

#### Deliverables:
- Transformed data in CSV format
- Data processing pipeline
- Forecasting-ready datasets

#### Success Criteria:
- Data transformations complete successfully
- Output files are properly formatted
- Data integrity maintained

---

### Stage 3: Analytics & Insights (30 minutes)
**Goal**: Generate required insights and forecasting data

#### Tasks:
- [ ] Calculate play sessions by channel (Browser vs Mobile)
- [ ] Analyze payment choices (One-time vs Subscription)
- [ ] Calculate total gross revenue
- [ ] Generate forecasting CSV files

#### Deliverables:
- Analytics results
- Forecasting CSV files
- Key insights summary

#### Success Criteria:
- All required metrics calculated correctly
- Forecasting files generated
- Insights are clear and actionable

---

### Stage 4: Quality Check & Documentation (15 minutes)
**Goal**: Final validation and documentation

#### Tasks:
- [ ] Run final data quality checks
- [ ] Verify all requirements are met
- [ ] Create brief documentation
- [ ] Prepare submission package

#### Deliverables:
- Final validation report
- Documentation
- Complete submission package

#### Success Criteria:
- All assignment requirements met
- Code is functional and clean
- Documentation is clear

---

## Assignment Requirements Checklist

### Core Requirements
- [ ] **Data Model Analysis**: Understand the ERD and CSV data structure
- [ ] **Data Processing Application**: Use Python (pandas/pyspark) to process data
- [ ] **Data Warehouse/Lake**: Implement Data Vault 2.0 or Star Schema patterns
- [ ] **Output Format**: Generate CSV or Parquet files locally
- [ ] **Quality Assurance**: Basic data validation and error handling
- [ ] **Insight Generation**: 2-3 key insights for 2025 planning

### Expected Deliverables
- [ ] **Forecasting CSV Files**: Processed data ready for 2025 analysis
- [ ] **Play Sessions Analysis**: Browser vs Mobile breakdown
- [ ] **Payment Analysis**: One-time vs Subscription patterns
- [ ] **Revenue Calculation**: Total gross revenue from the app
- [ ] **Working Code**: Functional Python application
- [ ] **Documentation**: Brief explanation of approach and findings

### Evaluation Focus (2-Hour Assignment)
- **Functionality (50%)**: Does the code run and produce correct results?
- **Code Quality (30%)**: Is the code well-organized and readable?
- **Extensibility (10%)**: Could the code be easily enhanced?
- **Insights (10%)**: Are the insights valuable for 2025 planning?

## Technology Stack (2-Hour Assignment)

### Required Technologies
- **Language**: Python with pandas (primary choice for 2-hour assignment)
- **Data Storage**: Local CSV files (simplest approach for time constraint)
- **Data Architecture**: Simple Star Schema (easier to implement quickly)

### Recommended Approach
- **Data Processing**: pandas for data manipulation and analysis
- **Data Validation**: Basic pandas validation (null checks, data types)
- **Output**: CSV files for forecasting data
- **Documentation**: Simple README or comments in code

### Quick Setup
```bash
pip install pandas numpy matplotlib seaborn
```

## Quality Assurance (2-Hour Assignment)

### Basic Testing Strategy
- **Data Validation**: Check for nulls, data types, and basic relationships
- **Output Verification**: Ensure CSV files are generated correctly
- **Basic Error Handling**: Handle common data loading issues

### Code Quality (Quick)
- **Readable Code**: Clear variable names and comments
- **Basic Documentation**: Comments explaining key steps
- **Simple Structure**: Logical flow from data loading to output

### Time-Saving Tips
- Focus on functionality over perfect code structure
- Use pandas built-in validation methods
- Keep documentation concise but clear

## Success Metrics (2-Hour Assignment)

### Technical Metrics
- All CSV files load without errors
- Data transformations complete successfully
- Output files are properly formatted
- Code runs without crashes

### Business Metrics
- Play sessions by channel calculated correctly
- Payment analysis provides clear insights
- Revenue calculation is accurate
- Forecasting data is ready for 2025 analysis

### Time Management
- Complete within 2 hours
- All core requirements met
- Basic documentation included

## Getting Started (Interviewer Instructions)

### Quick Setup (2 minutes)
1. **Clone/Download the repository**
   ```bash
   git clone <repository-url>
   cd fccassignment
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   This will automatically:
   - Install all required Python packages
   - Create output directories
   - Verify data files are present

3. **Run the main application**
   ```bash
   python main.py
   ```
   This will execute all 4 stages automatically and generate all required outputs.

### Alternative Manual Setup
If you prefer manual setup:
```bash
# Install dependencies
pip install -r requirements.txt

# Run individual stages
python data_loader.py          # Stage 1
python data_processor.py       # Stage 2  
python analytics_engine.py     # Stage 3
python quality_checker.py      # Stage 4
```

### Expected Output
After running `python main.py`, you should see:
- **Console output**: Progress through all 4 stages
- **Output files**: Generated in the `output/` directory
- **Log file**: `execution.log` with detailed execution information

### Troubleshooting
- **Python not found**: Use `py main.py` instead of `python main.py`
- **Package errors**: Run `python setup.py` to reinstall dependencies
- **Data errors**: Ensure `assignment_docs/` folder contains all CSV files

## Contributing

Please read the contributing guidelines and ensure all code follows the established patterns and quality standards.

## License

[Specify your license here]

---

*This README will be updated as the project progresses through each development stage.* 