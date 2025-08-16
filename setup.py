"""
Setup script for Dice Game Data Processing Application
Automatically installs dependencies and prepares the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def create_output_directories():
    """Create output directories"""
    print("📁 Creating output directories...")
    directories = [
        "output",
        "output/star_schema",
        "output/analytics", 
        "output/forecasting",
        "output/reports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created: {directory}")
    
    print("✅ Output directories created successfully!")

def verify_data_files():
    """Verify that data files exist"""
    print("📊 Verifying data files...")
    data_dir = Path("assignment_docs")
    
    if not data_dir.exists():
        print("❌ Error: assignment_docs directory not found!")
        print("   Please ensure the assignment_docs folder is in the project root.")
        return False
    
    csv_files = list(data_dir.glob("*.csv"))
    if len(csv_files) == 0:
        print("❌ Error: No CSV files found in assignment_docs directory!")
        return False
    
    print(f"✅ Found {len(csv_files)} CSV files in assignment_docs/")
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("SETUP: Dice Game Data Processing Application")
    print("=" * 60)
    
    # Step 1: Install requirements
    if not install_requirements():
        return False
    
    # Step 2: Create output directories
    create_output_directories()
    
    # Step 3: Verify data files
    if not verify_data_files():
        return False
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n🚀 Ready to run the application!")
    print("   Execute: python main.py")
    print("\n📖 For more information, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 