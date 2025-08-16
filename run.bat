@echo off
echo ========================================
echo Dice Game Data Processing Application
echo 2-Hour Interview Assignment
echo ========================================
echo.

echo Setting up environment...
python setup.py
if %errorlevel% neq 0 (
    echo Setup failed! Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Running main application...
python main.py
if %errorlevel% neq 0 (
    echo Application failed! Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Application completed successfully!
echo Check the output/ directory for generated files.
pause 