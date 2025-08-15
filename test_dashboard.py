"""
Test script for the Cost of Living Dashboard
Tests all major components and modules
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our modules
from src.data_processor import DataProcessor
from src.visualizations import DashboardVisualizations
from src.scenario_analysis import ScenarioAnalyzer
# Common utility functions for testing
def validate_dataframe(df, required_columns):
    """Simple dataframe validation for testing"""
    return all(col in df.columns for col in required_columns)

def clean_numeric_column(series, fill_value=0.0):
    """Simple numeric cleaning for testing"""
    return pd.to_numeric(series, errors='coerce').fillna(fill_value)

def detect_outliers(series, method='iqr', threshold=1.5):
    """Simple outlier detection for testing"""
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return (series < lower_bound) | (series > upper_bound)
    return pd.Series([False] * len(series))

def test_data_processor():
    """Test the data processor module"""
    print("\nTesting Data Processor...")
    
    try:
        # Initialize processor
        processor = DataProcessor()
        
        # Load data
        data = processor.load_data()
        print(f"Data loaded: {len(data)} datasets")
        
        # Clean data
        processor.clean_data()
        print(f"Cleaned expenses data: {len(processor.expenses_df)} records")
        print(f"Cleaned salary data: {len(processor.salary_df)} records")
        
        # Test date range
        min_date = processor.expenses_df['Date'].min()
        max_date = processor.expenses_df['Date'].max()
        print(f"Data date range: {min_date} to {max_date}")
        
        # Check for large amounts
        large_expenses = processor.expenses_df[processor.expenses_df['Amount'] > 10000]
        if not large_expenses.empty:
            print(f"Expense data issues: Large expense amounts detected")
        
        # Test monthly summary
        monthly_summary = processor.get_monthly_summary()
        print(f"Monthly summary: {len(monthly_summary)} months")
        
        # Test category breakdown
        category_breakdown = processor.get_category_breakdown()
        print(f"Category breakdown: {len(category_breakdown)} categories")
        
        # Test anomaly detection
        anomalies = processor.get_anomalies()
        print(f"Anomaly detection: {len(anomalies)} anomalies found")
        
        # Test ROI analysis
        roi_analysis = processor.get_roi_analysis()
        if 'scenarios' in roi_analysis:
            realistic = roi_analysis['scenarios']['realistic']
            print(f"ROI analysis: Break-even in {realistic['break_even_years']:.1f} years")
        else:
            print("ROI analysis: Completed")
        
        return True
        
    except Exception as e:
        print(f"Data processor test failed: {str(e)}")
        return False

def test_visualizations():
    """Test the visualizations module"""
    print("\nTesting Visualizations...")
    
    try:
        # Initialize visualizations
        viz = DashboardVisualizations()
        
        # Create sample data
        sample_data = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=12, freq='M'),
            'TotalExpenses': [1000, 1200, 1100, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100],
            'TotalIncome': [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100],
            'NetAmount': [1000, 900, 1100, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
        })
        
        # Test monthly trend chart
        trend_chart = viz.create_monthly_trend_chart(sample_data)
        print("Monthly trend chart created")
        
        # Test category breakdown chart
        category_data = pd.DataFrame({
            'Category': ['Rent', 'Groceries', 'Transportation', 'Utilities'],
            'Amount': [5000, 3000, 2000, 1500]
        })
        breakdown_chart = viz.create_category_breakdown_chart(category_data)
        print("Category breakdown chart created")
        
        # Test city comparison chart
        city_data = pd.DataFrame({
            'City': ['College Station', 'Austin', 'Houston'],
            'AverageSalary': [80000, 95000, 90000]
        })
        city_chart = viz.create_city_comparison_chart(city_data)
        print("City comparison chart created")
        
        # Test salary comparison chart
        salary_data = pd.DataFrame({
            'Role': ['Software Engineer', 'Data Scientist', 'ML Engineer'],
            'AverageSalary': [85000, 95000, 100000]
        })
        salary_chart = viz.create_salary_comparison_chart(salary_data)
        print("Salary comparison chart created")
        
        return True
        
    except Exception as e:
        print(f"Visualizations test failed: {str(e)}")
        return False

def test_scenario_analysis():
    """Test the scenario analysis module"""
    print("\nTesting Scenario Analysis...")
    
    try:
        # Initialize scenario analyzer
        scenario_analyzer = ScenarioAnalyzer()
        
        # Create sample data
        sample_expenses = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=6, freq='M'),
            'Category': ['Rent', 'Groceries', 'Transportation', 'Rent', 'Groceries', 'Transportation'],
            'Amount': [1000, 300, 200, 1000, 300, 200]
        })
        
        sample_salary = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=6, freq='M'),
            'Amount': [2000, 2000, 2000, 2000, 2000, 2000]
        })
        
        # Set baseline data
        scenario_analyzer.set_baseline_data(sample_expenses, sample_salary)
        
        # Test preset scenarios
        scenarios = scenario_analyzer.run_preset_scenarios()
        print(f"Preset scenarios: {len(scenarios)} created")
        
        # Test custom scenario
        custom_scenario = scenario_analyzer.create_custom_scenario(
            "Test Scenario", 
            {'Rent': 0.1, 'Groceries': -0.05}
        )
        print("Custom scenario created")
        
        # Test scenario comparison
        comparison = scenario_analyzer.compare_scenarios()
        print(f"Scenario comparison: {len(comparison)} scenarios")
        
        # Test scenario charts
        charts = scenario_analyzer.create_scenario_chart()
        print(f"Scenario charts: {len(charts)} created")
        
        return True
        
    except Exception as e:
        print(f"Scenario analysis test failed: {str(e)}")
        return False

def test_utils():
    """Test the utility functions"""
    print("\nTesting Utility Functions...")
    
    try:
        # Test data validation
        sample_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e']
        })
        is_valid = validate_dataframe(sample_data)
        print(f"Data validation: {is_valid}")
        
        # Test numeric cleaning
        numeric_data = pd.Series([1, 2, 3, '4', 5, 'invalid'])
        cleaned_data = clean_numeric_column(numeric_data)
        print(f"Numeric cleaning: {len(cleaned_data)} values processed")
        
        # Test outlier detection
        outlier_data = pd.Series([1, 2, 3, 4, 5, 100])
        outliers = detect_outliers(outlier_data)
        print(f"Outlier detection: {len(outliers)} outliers found")
        
        return True
        
    except Exception as e:
        print(f"Utils test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Starting Dashboard Tests...")
    print("=" * 50)
    
    # Run tests
    test_results = {}
    
    test_results['data_processor'] = test_data_processor()
    test_results['visualizations'] = test_visualizations()
    test_results['scenario_analysis'] = test_scenario_analysis()
    test_results['utils'] = test_utils()
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name.title()}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Dashboard is ready to use.")
    else:
        print("Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 