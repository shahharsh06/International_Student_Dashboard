"""
Data processing module for the Cost of Living Dashboard
Handles loading, cleaning, and transforming CSV data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys
import os
import warnings

# Suppress FutureWarning for pandas datetime operations
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')
warnings.filterwarnings('ignore', category=FutureWarning, module='_plotly_utils')
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    DATA_PATHS, DEFAULT_DATE_RANGE, CATEGORY_COLORS,
    validate_date_range, validate_amount, format_currency
)


class DataProcessor:
    """
    Main data processing class for handling expense and salary data
    """
    
    def __init__(self):
        """Initialize the data processor"""
        self.expenses_df = None
        self.salary_df = None
        self.city_costs_df = None
        self.salary_data_df = None
        self.processed_data = {}
        
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all data files and return as dictionary
        
        Returns:
            Dict containing all dataframes
        """
        try:
            # Load expense data
            self.expenses_df = pd.read_csv(DATA_PATHS['expenses'])
            self.expenses_df['Date'] = pd.to_datetime(self.expenses_df['Date'])
            
            # Load salary data
            self.salary_df = pd.read_csv(DATA_PATHS['salary'])
            self.salary_df['Date'] = pd.to_datetime(self.salary_df['Date'])
            
            # Load city costs and salary data
            self.city_costs_df = pd.read_csv(DATA_PATHS['city_costs'])
            self.salary_data_df = pd.read_csv(DATA_PATHS['salary_data'])
            
            return {
                'expenses': self.expenses_df,
                'salary': self.salary_df,
                'city_costs': self.city_costs_df,
                'salary_data': self.salary_data_df
            }
            
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def clean_data(self) -> None:
        """Clean and validate the loaded data"""
        if self.expenses_df is None or self.salary_df is None:
            raise ValueError("Data must be loaded before cleaning")
        
        # Clean expenses data
        self._clean_expenses_data()
        
        # Clean salary data
        self._clean_salary_data()
        
        # Validate data integrity
        self._validate_data_integrity()
    
    def _clean_expenses_data(self) -> None:
        """Clean and process expenses data"""
        # Remove duplicates
        self.expenses_df = self.expenses_df.drop_duplicates()
        
        # Handle missing values
        self.expenses_df['Amount'] = self.expenses_df['Amount'].fillna(0)
        self.expenses_df['Category'] = self.expenses_df['Category'].fillna('Miscellaneous')
        self.expenses_df['PaymentType'] = self.expenses_df['PaymentType'].fillna('Unknown')
        
        # Validate amounts
        self.expenses_df = self.expenses_df[self.expenses_df['Amount'] >= 0]
        
        # Add derived columns
        self.expenses_df['Year'] = self.expenses_df['Date'].dt.year
        self.expenses_df['Month'] = self.expenses_df['Date'].dt.month
        self.expenses_df['YearMonth'] = self.expenses_df['Date'].dt.to_period('M').astype(str)
        self.expenses_df['DayOfWeek'] = self.expenses_df['Date'].dt.day_name()
        
        # Categorize expenses
        self.expenses_df['CategoryGroup'] = self._categorize_expenses(self.expenses_df['Category'])
        
        print(f"✅ Cleaned expenses data: {len(self.expenses_df)} records")
    
    def _clean_salary_data(self) -> None:
        """Clean and process salary data"""
        # Remove duplicates
        self.salary_df = self.salary_df.drop_duplicates()
        
        # Handle missing values
        self.salary_df['Amount'] = self.salary_df['Amount'].fillna(0)
        
        # Validate amounts
        self.salary_df = self.salary_df[self.salary_df['Amount'] >= 0]
        
        # Add derived columns
        self.salary_df['Year'] = self.salary_df['Date'].dt.year
        self.salary_df['Month'] = self.salary_df['Date'].dt.month
        self.salary_df['YearMonth'] = self.salary_df['Date'].dt.to_period('M').astype(str)
        
        print(f"✅ Cleaned salary data: {len(self.salary_df)} records")
    
    def _categorize_expenses(self, categories: pd.Series) -> pd.Series:
        """Categorize expenses into broader groups"""
        category_mapping = {
            'Rent': 'Housing',
            'Groceries': 'Food',
            'Restaurants': 'Food',
            'Tuition': 'Education',
            'Mobile_Recharge': 'Utilities',
            'Gas': 'Transportation',
            'Travel': 'Transportation',
            'Car_Insurance': 'Transportation',
            'Shopping': 'Personal',
            'Books': 'Education',
            'Utilities': 'Utilities'
        }
        
        return categories.map(lambda x: category_mapping.get(x, 'Other'))
    
    def _validate_data_integrity(self) -> None:
        """Validate data integrity and consistency"""
        # Check date ranges
        min_date = min(self.expenses_df['Date'].min(), self.salary_df['Date'].min())
        max_date = max(self.expenses_df['Date'].max(), self.salary_df['Date'].max())
        
        print(f"Data date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
        
        # Check for data quality issues
        expense_issues = []
        salary_issues = []
        
        # Check for extreme values (adjusted for realistic tuition and housing costs)
        if self.expenses_df['Amount'].max() > 50000:
            expense_issues.append("Extremely large expense amounts detected")
        
        if self.salary_df['Amount'].max() > 10000:
            salary_issues.append("Large salary amounts detected")
        
        # Check for missing categories
        if self.expenses_df['Category'].isnull().sum() > 0:
            expense_issues.append("Missing categories found")
        
        if len(expense_issues) > 0:
            print(f"Expense data issues: {', '.join(expense_issues)}")
        
        if len(salary_issues) > 0:
            print(f"Salary data issues: {', '.join(salary_issues)}")
    
    def get_monthly_summary(self, start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
        """
        Generate monthly summary of expenses and income
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            DataFrame with monthly summaries
        """
        if start_date is None:
            start_date = self.expenses_df['Date'].min()
        if end_date is None:
            end_date = self.expenses_df['Date'].max()
        
        # Filter data by date range
        expenses_filtered = self.expenses_df[
            (self.expenses_df['Date'] >= start_date) &
            (self.expenses_df['Date'] <= end_date)
        ]
        
        salary_filtered = self.salary_df[
            (self.salary_df['Date'] >= start_date) &
            (self.salary_df['Date'] <= end_date)
        ]
        
        # Group by month
        monthly_expenses = expenses_filtered.groupby(expenses_filtered['Date'].dt.to_period('M'))['Amount'].sum()
        monthly_income = salary_filtered.groupby(salary_filtered['Date'].dt.to_period('M'))['Amount'].sum()
        
        # Create summary DataFrame
        summary_df = pd.DataFrame({
            'TotalExpenses': monthly_expenses,
            'TotalIncome': monthly_income
        }).fillna(0)
        
        summary_df['NetAmount'] = summary_df['TotalIncome'] - summary_df['TotalExpenses']
        summary_df['CumulativeNet'] = summary_df['NetAmount'].cumsum()
        
        # Ensure 'YearMonth' is a column (not just the index)
        summary_df = summary_df.reset_index()
        # Rename the first column to 'YearMonth' regardless of its current name
        if summary_df.columns[0] != 'YearMonth':
            summary_df = summary_df.rename(columns={summary_df.columns[0]: 'YearMonth'})
        
        # Convert Period objects to strings to avoid plotly warnings
        summary_df['YearMonth'] = summary_df['YearMonth'].astype(str)
        
        return summary_df
    
    def get_category_breakdown(self, start_date: datetime = None, end_date: datetime = None, filtered_data: pd.DataFrame = None) -> pd.DataFrame:
        """
        Get expense breakdown by category
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            filtered_data: Pre-filtered data (if provided, use this instead of full dataset)
            
        Returns:
            DataFrame with category breakdown
        """
        if filtered_data is not None:
            # Use the filtered data directly
            expenses_filtered = filtered_data
        else:
            # Use full dataset with date filtering
            if start_date is None:
                start_date = self.expenses_df['Date'].min()
            if end_date is None:
                end_date = self.expenses_df['Date'].max()
            
            # Filter data by date range
            expenses_filtered = self.expenses_df[
                (self.expenses_df['Date'] >= start_date) &
                (self.expenses_df['Date'] <= end_date)
            ]
        
        # Group by category
        category_breakdown = expenses_filtered.groupby('Category')['Amount'].agg(['sum', 'count']).reset_index()
        category_breakdown.columns = ['Category', 'Amount', 'Count']
        
        return category_breakdown.sort_values('Amount', ascending=False)
    
    def get_anomalies(self, threshold: float = 2.0) -> pd.DataFrame:
        """
        Detect spending anomalies using statistical methods
        
        Args:
            threshold: Number of standard deviations for anomaly detection
            
        Returns:
            DataFrame with detected anomalies
        """
        # Calculate statistics by category
        category_stats = self.expenses_df.groupby('Category')['Amount'].agg(['mean', 'std']).reset_index()
        
        # Merge with original data
        expenses_with_stats = self.expenses_df.merge(category_stats, on='Category', suffixes=('', '_stats'))
        
        # Calculate z-score
        expenses_with_stats['z_score'] = (
            (expenses_with_stats['Amount'] - expenses_with_stats['mean']) / 
            expenses_with_stats['std']
        )
        
        # Identify anomalies
        anomalies = expenses_with_stats[
            (expenses_with_stats['z_score'].abs() > threshold) &
            (expenses_with_stats['Amount'] > 0)
        ].copy()
        
        # Select relevant columns
        anomalies = anomalies[['Date', 'Category', 'Amount', 'PaymentType', 'City']]
        
        return anomalies.sort_values('Amount', ascending=False)
    
    def get_roi_analysis(self) -> Dict:
        """
        Calculate realistic ROI analysis for degree investment
        
        Returns:
            Dictionary with ROI metrics and scenarios
        """
        # Calculate total degree cost from actual expenses
        total_expenses = self.expenses_df['Amount'].sum()
        
        # Calculate actual salary data for reference
        actual_salary_total = self.salary_df['Amount'].sum()
        actual_salary_months = len(self.salary_df['Date'].dt.to_period('M').unique())
        actual_monthly_salary = actual_salary_total / actual_salary_months if actual_salary_months > 0 else 0
        actual_annual_salary = actual_monthly_salary * 12
        
        # Load and analyze salary_data.csv for realistic salary ranges
        try:
            salary_data = pd.read_csv('data/salary_data.csv')
            
            # Calculate salary statistics across all cities and roles
            all_salaries = salary_data['AverageSalary'].values
            
            # Calculate salary ranges dynamically
            conservative_salary = float(np.min(all_salaries))  # Lowest salary in dataset
            realistic_salary = float(np.median(all_salaries))  # Median salary in dataset
            optimistic_salary = float(np.max(all_salaries))    # Highest salary in dataset
            
            # Get city-specific statistics if available
            city_salary_stats = salary_data.groupby('City')['AverageSalary'].agg(['min', 'median', 'max']).round(0)
            
            # Get role-specific statistics if available
            role_salary_stats = salary_data.groupby('Role')['AverageSalary'].agg(['min', 'median', 'max']).round(0)
            
            print(f"Salary ranges from dataset: Conservative=${conservative_salary:,.0f}, Realistic=${realistic_salary:,.0f}, Optimistic=${optimistic_salary:,.0f}")
            
        except Exception as e:
            print(f"Warning: Could not load salary_data.csv, using fallback values: {e}")
            # Fallback values if salary_data.csv is not available
            conservative_salary = 60000
            realistic_salary = 85000
            optimistic_salary = 120000
            city_salary_stats = pd.DataFrame()
            role_salary_stats = pd.DataFrame()
        
        # Calculate city-specific target salaries based on actual data
        city_salaries = self.salary_df.groupby('City')['Amount'].sum()
        city_months = self.salary_df.groupby('City')['Date'].apply(lambda x: x.dt.to_period('M').nunique())
        city_monthly_salaries = city_salaries / city_months
        city_annual_salaries = city_monthly_salaries * 12
        
        # Realistic scenarios based on actual salary data
        scenarios = {
            'conservative': {
                'annual_salary': conservative_salary,
                'job_search_months': 6,
                'savings_rate': 0.15,  # 15% savings
                'description': f'Conservative estimate with 6-month job search (Lowest salary: ${conservative_salary:,.0f})'
            },
            'realistic': {
                'annual_salary': realistic_salary,
                'job_search_months': 3,
                'savings_rate': 0.25,  # 25% savings
                'description': f'Realistic estimate with 3-month job search (Median salary: ${realistic_salary:,.0f})'
            },
            'optimistic': {
                'annual_salary': optimistic_salary,
                'job_search_months': 1,
                'savings_rate': 0.35,  # 35% savings
                'description': f'Optimistic estimate with quick job placement (Highest salary: ${optimistic_salary:,.0f})'
            }
        }
        
        # Calculate ROI for each scenario
        roi_results = {}
        for scenario_name, scenario in scenarios.items():
            annual_salary = scenario['annual_salary']
            job_search_months = scenario['job_search_months']
            savings_rate = scenario['savings_rate']
            
            # Calculate break-even time (accounting for job search)
            monthly_salary = annual_salary / 12
            monthly_savings = monthly_salary * savings_rate
            
            # Break-even calculation: how many months to recover degree cost
            if monthly_savings > 0:
                break_even_months = total_expenses / monthly_savings
                break_even_years = (break_even_months + job_search_months) / 12
            else:
                break_even_years = float('inf')
            
            # ROI percentage
            if total_expenses > 0:
                roi_percentage = ((annual_salary - total_expenses) / total_expenses) * 100
            else:
                roi_percentage = 0
            
            roi_results[scenario_name] = {
                'annual_salary': annual_salary,
                'monthly_salary': monthly_salary,
                'monthly_savings': monthly_savings,
                'break_even_years': break_even_years,
                'break_even_months': break_even_months if monthly_savings > 0 else float('inf'),
                'roi_percentage': roi_percentage,
                'job_search_months': job_search_months,
                'savings_rate': savings_rate,
                'description': scenario['description']
            }
        
        return {
            'total_degree_cost': total_expenses,
            'actual_annual_salary': actual_annual_salary,
            'actual_monthly_salary': actual_monthly_salary,
            'city_salaries': city_annual_salaries.to_dict(),
            'salary_ranges': {
                'conservative': conservative_salary,
                'realistic': realistic_salary,
                'optimistic': optimistic_salary
            },
            'city_salary_stats': city_salary_stats.to_dict() if not city_salary_stats.empty else {},
            'role_salary_stats': role_salary_stats.to_dict() if not role_salary_stats.empty else {},
            'scenarios': roi_results,
            'break_even_years': roi_results['realistic']['break_even_years'],  # Add for test compatibility
            'data_points': {
                'total_expenses': total_expenses,
                'actual_salary_total': actual_salary_total,
                'actual_salary_months': actual_salary_months,
                'city_breakdown': city_salaries.to_dict(),
                'dataset_salaries': all_salaries.tolist() if 'all_salaries' in locals() else []
            }
        }

def main():
    """Test the data processor"""
    processor = DataProcessor()
    
    try:
        # Load and clean data
        data = processor.load_data()
        processor.clean_data()
        
        # Test monthly summary
        monthly_summary = processor.get_monthly_summary()
        print(f"✅ Monthly summary created: {len(monthly_summary)} months")
        
        # Test category breakdown
        category_breakdown = processor.get_category_breakdown()
        print(f"✅ Category breakdown created: {len(category_breakdown)} categories")
        
        # Test anomaly detection
        anomalies = processor.get_anomalies()
        print(f"✅ Anomaly detection completed: {len(anomalies)} anomalies found")
        
        # Test ROI analysis
        roi_analysis = processor.get_roi_analysis()
        print(f"✅ ROI analysis completed: Break-even in {roi_analysis['break_even_years']:.1f} years")
        
    except Exception as e:
        print(f"❌ Error in data processing: {str(e)}")


if __name__ == "__main__":
    main() 