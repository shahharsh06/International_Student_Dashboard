"""
Scenario analysis module for the Cost of Living Dashboard
Handles "what-if" analysis and scenario modeling
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
import warnings
from functools import lru_cache
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import format_currency
from config.design_system import COLORS

# Suppress warnings for performance
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)


class ScenarioAnalyzer:
    """
    Scenario analysis for expense and income modeling
    """
    
    def __init__(self):
        """Initialize the scenario analyzer"""
        self.baseline_expenses = None
        self.baseline_salary = None
        self.scenarios = {}
        
    def set_baseline_data(self, expenses: pd.DataFrame, salary: pd.DataFrame) -> None:
        """
        Set baseline data for scenario analysis
        
        Args:
            expenses: Baseline expenses DataFrame
            salary: Baseline salary DataFrame
        """
        self.baseline_expenses = expenses.copy()
        self.baseline_salary = salary.copy()
        self.scenarios = {}
    
    def get_available_categories(self) -> List[str]:
        """
        Get list of available expense categories
        
        Returns:
            List of category names
        """
        if self.baseline_expenses is None:
            return []
        return sorted(self.baseline_expenses['Category'].unique())
    
    def run_preset_scenarios(self) -> Dict:
        """
        Run predefined scenarios for analysis - OPTIMIZED VERSION
        
        Returns:
            Dictionary with scenario results
        """
        if self.baseline_expenses is None:
            raise ValueError("Baseline data must be set before running scenarios")
        
        start_time = time.time()
        
        # Get available categories from baseline data (cached)
        if not hasattr(self, '_available_categories'):
            self._available_categories = sorted(self.baseline_expenses['Category'].unique())
        
        available_categories = self._available_categories
        print(f"Available categories for scenarios: {available_categories}")
        
        scenarios = {}
        
        # Performance optimization: Batch scenario creation
        scenario_configs = []
        
        # Scenario 1: 10% increase in rent (if rent category exists)
        if 'Rent' in available_categories:
            scenario_configs.append(('rent_increase', 'Rent Increase (10%)', {'Rent': 0.10}, 0.0))
        
        # Scenario 2: 15% decrease in groceries (if groceries category exists)
        if 'Groceries' in available_categories:
            scenario_configs.append(('groceries_decrease', 'Groceries Decrease (15%)', {'Groceries': -0.15}, 0.0))
        
        # Scenario 3: 20% increase in salary
        scenario_configs.append(('salary_increase', 'Salary Increase (20%)', {}, 0.20))
        
        # Scenario 4: Combined scenario (only if both categories exist)
        if 'Rent' in available_categories and 'Groceries' in available_categories:
            scenario_configs.append(('combined', 'Combined (Rent +10%, Groceries -15%, Salary +20%)', {'Rent': 0.10, 'Groceries': -0.15}, 0.20))
        
        # Scenario 5: Tuition increase (if tuition category exists)
        if 'Tuition' in available_categories:
            scenario_configs.append(('tuition_increase', 'Tuition Increase (15%)', {'Tuition': 0.15}, 0.0))
        
        # Scenario 6: Gas price increase (if gas category exists)
        if 'Gas' in available_categories:
            scenario_configs.append(('gas_increase', 'Gas Price Increase (25%)', {'Gas': 0.25}, 0.0))
        
        # Batch create scenarios for better performance
        for scenario_key, scenario_name, expense_adjustments, salary_adjustment in scenario_configs:
            scenarios[scenario_key] = self._create_scenario(scenario_name, expense_adjustments, salary_adjustment)
        
        self.scenarios = scenarios
        
        # Performance logging
        total_time = time.time() - start_time
        print(f"Performance: Generated {len(scenarios)} scenarios in {total_time:.3f}s")
        
        return scenarios
    
    def create_custom_scenario(self, name: str, adjustments: Dict[str, float], 
                             salary_adjustment: float = 0.0) -> Dict:
        """
        Create a custom scenario with specified adjustments
        
        Args:
            name: Scenario name
            adjustments: Dictionary of category adjustments (e.g., {'Rent': 0.10})
            salary_adjustment: Salary adjustment percentage
            
        Returns:
            Dictionary with scenario results
        """
        if self.baseline_expenses is None:
            raise ValueError("Baseline data must be set before creating scenarios")
        
        scenario = self._create_scenario(name, adjustments, salary_adjustment)
        self.scenarios[name] = scenario
        
        return scenario
    
    def _create_scenario(self, name: str, expense_adjustments: Dict[str, float], 
                        salary_adjustment: float = 0.0) -> Dict:
        """
        Create a scenario with specified adjustments - OPTIMIZED VERSION
        
        Args:
            name: Scenario name
            expense_adjustments: Dictionary of expense category adjustments
            salary_adjustment: Salary adjustment percentage
            
        Returns:
            Dictionary with scenario results
        """
        start_time = time.time()
        
        # Pre-calculate baseline totals for performance
        if not hasattr(self, '_baseline_totals'):
            self._baseline_totals = {
                'expenses': self.baseline_expenses['Amount'].sum(),
                'income': self.baseline_salary['Amount'].sum()
            }
            self._baseline_totals['net'] = self._baseline_totals['income'] - self._baseline_totals['expenses']
        
        # Use vectorized operations for better performance
        adjusted_expenses_total = self._baseline_totals['expenses']
        
        # Optimize expense adjustments with vectorized operations
        if expense_adjustments:
            # Create a single mask for all categories to avoid multiple DataFrame operations
            category_mask = self.baseline_expenses['Category'].isin(expense_adjustments.keys())
            if category_mask.any():
                # Group by category and apply adjustments in one operation
                category_groups = self.baseline_expenses[category_mask].groupby('Category')['Amount'].sum()
                
                for category, adjustment in expense_adjustments.items():
                    if category in category_groups.index:
                        original_amount = category_groups[category]
                        adjusted_amount = original_amount * (1 + adjustment)
                        adjusted_expenses_total += (adjusted_amount - original_amount)
        
        # Optimize salary adjustment
        adjusted_income_total = self._baseline_totals['income']
        if salary_adjustment != 0:
            adjusted_income_total *= (1 + salary_adjustment)
        
        # Calculate net amount
        net_amount = adjusted_income_total - adjusted_expenses_total
        
        # Calculate percentage changes efficiently
        expense_change = ((adjusted_expenses_total - self._baseline_totals['expenses']) / self._baseline_totals['expenses']) * 100
        income_change = ((adjusted_income_total - self._baseline_totals['income']) / self._baseline_totals['income']) * 100
        net_change = ((net_amount - self._baseline_totals['net']) / self._baseline_totals['net']) * 100 if self._baseline_totals['net'] != 0 else 0
        
        # Performance logging
        execution_time = time.time() - start_time
        if execution_time > 0.1:  # Log slow operations
            print(f"Performance: Scenario '{name}' created in {execution_time:.3f}s")
        
        return {
            'name': name,
            'metrics': {
                'total_expenses': adjusted_expenses_total,
                'total_income': adjusted_income_total,
                'net_amount': net_amount
            },
            'changes': {
                'total_expenses': expense_change,
                'total_income': income_change,
                'net_amount': net_change
            },
            'adjustments': {
                'expense_adjustments': expense_adjustments,
                'salary_adjustment': salary_adjustment
            },
            'execution_time': execution_time
        }
    
    def compare_scenarios(self) -> pd.DataFrame:
        """
        Compare all scenarios in a tabular format
        
        Returns:
            DataFrame with scenario comparison
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for comparison")
        
        comparison_data = []
        
        # Add baseline
        baseline_expenses = self.baseline_expenses['Amount'].sum()
        baseline_income = self.baseline_salary['Amount'].sum()
        baseline_net = baseline_income - baseline_expenses
        
        comparison_data.append({
            'Scenario': 'Baseline',
            'Total Expenses': baseline_expenses,
            'Total Income': baseline_income,
            'Net Amount': baseline_net,
            'Expense Change (%)': 0.0,
            'Income Change (%)': 0.0,
            'Net Change (%)': 0.0
        })
        
        # Add scenarios
        for scenario_name, scenario in self.scenarios.items():
            metrics = scenario['metrics']
            changes = scenario['changes']
            
            comparison_data.append({
                'Scenario': scenario['name'],
                'Total Expenses': metrics['total_expenses'],
                'Total Income': metrics['total_income'],
                'Net Amount': metrics['net_amount'],
                'Expense Change (%)': changes['total_expenses'],
                'Income Change (%)': changes['total_income'],
                'Net Change (%)': changes['net_amount']
            })
        
        return pd.DataFrame(comparison_data)
    
    def create_scenario_chart(self) -> Dict[str, go.Figure]:
        """
        Create visualization charts for scenario analysis - OPTIMIZED VERSION
        
        Returns:
            Dictionary with scenario charts
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for charting")
        
        start_time = time.time()
        charts = {}
        
        # Pre-extract data for better performance
        scenarios_list = list(self.scenarios.keys())
        scenario_data = {
            'names': [self.scenarios[s]['name'] for s in scenarios_list],
            'expenses': [self.scenarios[s]['metrics']['total_expenses'] for s in scenarios_list],
            'net': [self.scenarios[s]['metrics']['net_amount'] for s in scenarios_list]
        }
        
        # Create expenses comparison chart with optimized styling
        fig_expenses = go.Figure()
        fig_expenses.add_trace(go.Bar(
            x=scenario_data['names'],
            y=scenario_data['expenses'],
            marker=dict(
                color=scenario_data['expenses'],
                colorscale=[
                    [0, COLORS['accent3']],      # Light green for lower amounts
                    [0.25, COLORS['accent2']],    # Light blue for medium amounts
                    [0.5, COLORS['accent1']],     # Purple for higher amounts
                    [0.75, COLORS['secondary']],  # Pink for high amounts
                    [1, COLORS['primary']]        # Bright blue for highest amounts
                ],
                showscale=True,
                colorbar=dict(title="Amount ($)")
            ),
            hovertemplate='<b>%{x}</b><br>Expenses: $%{y:,.0f}<extra></extra>'
        ))
        
        # Apply optimized layout
        fig_expenses.update_layout(
            title={
                'text': 'Total Expenses by Scenario',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': COLORS['text_primary']}
            },
            height=500,
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['surface'],
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        fig_expenses.update_yaxes(tickformat='$,.0f')
        charts['expenses_comparison'] = fig_expenses
        
        # Create net amount comparison chart with optimized styling
        fig_net = go.Figure()
        fig_net.add_trace(go.Bar(
            x=scenario_data['names'],
            y=scenario_data['net'],
            marker=dict(
                color=scenario_data['net'],
                colorscale=[
                    [0, COLORS['accent3']],      # Light green for lower amounts
                    [0.25, COLORS['accent2']],    # Light blue for medium amounts
                    [0.5, COLORS['accent1']],     # Purple for higher amounts
                    [0.75, COLORS['secondary']],  # Pink for high amounts
                    [1, COLORS['primary']]        # Bright blue for highest amounts
                ],
                showscale=True,
                colorbar=dict(title="Net Amount ($)")
            ),
            hovertemplate='<b>%{x}</b><br>Net: $%{y:,.0f}<extra></extra>'
        ))
        
        # Apply optimized layout for net chart
        fig_net.update_layout(
            title={
                'text': 'Net Amount by Scenario',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': COLORS['text_primary']}
            },
            height=500,
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['surface'],
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        fig_net.update_yaxes(tickformat='$,.0f')
        charts['net_comparison'] = fig_net
        
        # Create change comparison chart
        expense_changes = [self.scenarios[s]['changes']['total_expenses'] for s in scenarios_list]
        income_changes = [self.scenarios[s]['changes']['total_income'] for s in scenarios_list]
        net_changes = [self.scenarios[s]['changes']['net_amount'] for s in scenarios_list]
        
        fig_changes = go.Figure()
        
        fig_changes.add_trace(go.Bar(
            x=scenario_data['names'],
            y=expense_changes,
            name='Expense Change (%)',
            marker_color=COLORS['warning']
        ))
        
        fig_changes.add_trace(go.Bar(
            x=scenario_data['names'],
            y=income_changes,
            name='Income Change (%)',
            marker_color=COLORS['success']
        ))
        
        fig_changes.add_trace(go.Bar(
            x=scenario_data['names'],
            y=net_changes,
            name='Net Change (%)',
            marker_color=COLORS['primary']
        ))
        
        fig_changes.update_layout(
            title={
                'text': 'Percentage Changes by Scenario',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': COLORS['text_primary']}
            },
            xaxis_title='Scenario',
            yaxis_title='Change (%)',
            barmode='group',
            height=500,
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['surface']
        )
        
        charts['changes_comparison'] = fig_changes
        
        # Performance logging
        execution_time = time.time() - start_time
        print(f"Performance: Charts created in {execution_time:.3f}s")
        
        return charts
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Get performance metrics for scenario analysis
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.scenarios:
            return {}
        
        total_execution_time = sum(
            scenario.get('execution_time', 0) for scenario in self.scenarios.values()
        )
        
        return {
            'total_scenarios': len(self.scenarios),
            'total_execution_time': total_execution_time,
            'average_execution_time': total_execution_time / len(self.scenarios) if self.scenarios else 0,
            'fastest_scenario': min(
                (scenario.get('execution_time', 0), name) for name, scenario in self.scenarios.items()
            )[1] if self.scenarios else None,
            'slowest_scenario': max(
                (scenario.get('execution_time', 0), name) for name, scenario in self.scenarios.items()
            )[1] if self.scenarios else None
        }
    
    def get_best_scenario(self) -> Optional[str]:
        """
        Identify the best scenario based on net amount
        
        Returns:
            Name of the best scenario, or None if no scenarios
        """
        if not self.scenarios:
            return None
        
        best_scenario = None
        best_net = float('-inf')
        
        for scenario_name, scenario in self.scenarios.items():
            net_amount = scenario['metrics']['net_amount']
            if net_amount > best_net:
                best_net = net_amount
                best_scenario = scenario_name
        
        return best_scenario
    
    def get_worst_scenario(self) -> Optional[str]:
        """
        Identify the worst scenario based on net amount
        
        Returns:
            Name of the worst scenario, or None if no scenarios
        """
        if not self.scenarios:
            return None
        
        worst_scenario = None
        worst_net = float('inf')
        
        for scenario_name, scenario in self.scenarios.items():
            net_amount = scenario['metrics']['net_amount']
            if net_amount < worst_net:
                worst_net = net_amount
                worst_scenario = scenario_name
        
        return worst_scenario
    
    def export_scenario_results(self, filename: str) -> None:
        """
        Export scenario results to CSV
        
        Args:
            filename: Output filename
        """
        try:
            comparison_df = self.compare_scenarios()
            comparison_df.to_csv(filename, index=False)
            print(f"Scenario results exported to {filename}")
        except Exception as e:
            print(f"Error exporting scenario results: {str(e)}")


def main():
    """Test the scenario analyzer"""
    # Create sample data
    dates = pd.date_range('2023-01-01', periods=12, freq='M')
    
    sample_expenses = pd.DataFrame({
        'Date': dates,
        'Category': ['Rent', 'Groceries', 'Transportation', 'Rent', 'Groceries', 'Transportation',
                    'Rent', 'Groceries', 'Transportation', 'Rent', 'Groceries', 'Transportation'],
        'Amount': [1200, 300, 200, 1200, 300, 200, 1200, 300, 200, 1200, 300, 200],
        'City': ['Austin'] * 12,
        'PaymentType': ['Credit Card'] * 12
    })
    
    sample_salary = pd.DataFrame({
        'Date': dates,
        'Amount': [2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500],
        'Category': ['Part-Time'] * 12,
        'City': ['Austin'] * 12
    })
    
    # Test scenario analysis
    analyzer = ScenarioAnalyzer()
    
    try:
        # Set baseline data
        analyzer.set_baseline_data(sample_expenses, sample_salary)
        
        # Run preset scenarios
        scenarios = analyzer.run_preset_scenarios()
        print(f"Generated {len(scenarios)} preset scenarios")
        
        # Create custom scenario
        custom_scenario = analyzer.create_custom_scenario(
            'Custom Test',
            {'Rent': 0.05, 'Groceries': -0.10},
            salary_adjustment=0.15
        )
        print("Created custom scenario")
        
        # Compare scenarios
        comparison = analyzer.compare_scenarios()
        print(f"Scenario comparison created: {len(comparison)} scenarios")
        
        # Get best/worst scenarios
        best = analyzer.get_best_scenario()
        worst = analyzer.get_worst_scenario()
        print(f"Best scenario: {best}")
        print(f"Worst scenario: {worst}")
        
        # Create charts
        charts = analyzer.create_scenario_chart()
        print(f"Created {len(charts)} scenario charts")
        
    except Exception as e:
        print(f"Error in scenario analysis: {str(e)}")


if __name__ == "__main__":
    main() 