"""
Enhanced Visualization Module for Professional Dashboard
Core chart types with consistent styling and professional layouts
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List
import sys
import os
import warnings
from plotly.subplots import make_subplots

# Suppress FutureWarning for pandas datetime operations
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')
warnings.filterwarnings('ignore', category=FutureWarning, module='_plotly_utils')
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    COLORS, CHART_COLORS, CHART_LAYOUT, CHART_TEMPLATES, COMPONENT_SIZES
)
from config.design_system import get_chart_layout, get_hover_template, get_hover_label_config


class DashboardVisualizations:
    """
    Enhanced visualization class with core chart types and professional styling
    """
    
    def __init__(self):
        """Initialize the visualization class with professional settings"""
        self.colors = COLORS
        self.chart_colors = CHART_COLORS
        self.chart_layout = CHART_LAYOUT
        self.chart_templates = CHART_TEMPLATES
        
    def _get_standard_legend_config(self):
        """Get standardized legend configuration for all charts"""
        font_sizes = self._get_standard_font_sizes()
        return dict(
            orientation="v",
            yanchor="top",
            y=0.95,
            xanchor="left",
            x=1.02,
            bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
            bordercolor=COLORS['border'],
            borderwidth=1,
            font=dict(
                color=COLORS['text_primary'],
                family='Inter, sans-serif',
                size=font_sizes['legend']
            ),
            itemsizing='constant',
            itemwidth=30
        )
    
    def _get_standard_margin_config(self):
        """Get standardized margin configuration for charts with legends"""
        return dict(l=80, r=120, t=100, b=100)
    
    def _get_standard_hoverlabel_config(self, border_color: str = None):
        """Get standardized hover label configuration for all charts"""
        if border_color is None:
            border_color = COLORS['primary']
        
        return dict(
            bgcolor=COLORS['surface'],
            bordercolor=border_color,
            font=dict(
                color=COLORS['text_primary'],
                family='Inter, sans-serif',
                size=12
            )
        )
    
    def _get_standard_font_sizes(self):
        """Get standardized font sizes for all chart elements"""
        return {
            'title': 20,
            'axis_title': 14,
            'axis_tick': 11,
            'legend': 11,
            'hover': 12,
            'annotation': 12,
            'text': 10
        }
        
    def _apply_professional_layout(self, fig: go.Figure, title: str = None, 
                                 height: int = None, template: str = None) -> go.Figure:
        """Apply premium professional layout to all charts with deep navy theme"""
        height = height or COMPONENT_SIZES['chart_height']
        template = template or self.chart_templates['premium']
        
        # Premium chart layout with deep navy theme
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'yanchor': 'top',
                'font': {
                    'size': 20, 
                    'color': COLORS['text_primary'], 
                    'family': 'Inter, sans-serif'
                }
            },
            height=height,
            template=template,
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['surface'],
            margin=dict(l=80, r=80, t=100, b=80),
            showlegend=True,
            legend=self._get_standard_legend_config(),
            hovermode='closest',
            dragmode='zoom',
            modebar=dict(
                orientation='v',
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.9)',
                color=COLORS['text_muted'],
                activecolor=COLORS['primary'],
                remove=['pan', 'select', 'lasso2d']
            ),
            font=dict(
                family='Inter, sans-serif',
                color=COLORS['text_secondary']
            )
        )
        
        # Update axes with premium styling
        font_sizes = self._get_standard_font_sizes()
        fig.update_xaxes(
            gridcolor=COLORS['grid'],
            gridwidth=1,
            zerolinecolor=COLORS['border'],
            zerolinewidth=1,
            showline=True,
            linecolor=COLORS['border'],
            linewidth=1,
            title_font=dict(
                color=COLORS['text_primary'],
                family='Inter, sans-serif',
                size=font_sizes['axis_title']
            ),
            tickfont=dict(
                color=COLORS['text_secondary'],
                family='Inter, sans-serif',
                size=font_sizes['axis_tick']
            )
        )
        
        fig.update_yaxes(
            gridcolor=COLORS['grid'],
            gridwidth=1,
            zerolinecolor=COLORS['border'],
            zerolinewidth=1,
            showline=True,
            linecolor=COLORS['border'],
            linewidth=1,
            title_font=dict(
                color=COLORS['text_primary'],
                family='Inter, sans-serif',
                size=font_sizes['axis_title']
            ),
            tickfont=dict(
                color=COLORS['text_secondary'],
                family='Inter, sans-serif',
                size=font_sizes['axis_tick']
            )
        )
        
        return fig
        
    def create_monthly_trend_chart(self, monthly_data: pd.DataFrame) -> go.Figure:
        """
        Create premium monthly trend chart with enhanced styling and interactions
        
        Args:
            monthly_data: DataFrame with monthly summaries
            
        Returns:
            Plotly figure object
        """
        # Ensure YearMonth is properly formatted as string
        if 'YearMonth' in monthly_data.columns:
            monthly_data = monthly_data.copy()
            monthly_data['YearMonth'] = monthly_data['YearMonth'].astype(str)
        
        fig = go.Figure()
        
        # Enhanced expense line with premium styling
        fig.add_trace(go.Scatter(
            x=monthly_data['YearMonth'].astype(str),
            y=monthly_data['TotalExpenses'],
            mode='lines+markers',
            name='Expenses',
            line=dict(
                color=COLORS['secondary'], 
                width=4,
                shape='spline'
            ),
            marker=dict(
                size=10, 
                symbol='circle',
                color=COLORS['secondary'],
                line=dict(color=COLORS['background'], width=2)
            ),
            hovertemplate='<b>%{x}</b><br>' +
                         '<span style="color: ' + COLORS['error'] + ';">Expenses: $%{y:,.0f}</span><extra></extra>',
            hoverlabel=self._get_standard_hoverlabel_config(COLORS['secondary'])
        ))
        
        # Enhanced income line with premium styling
        fig.add_trace(go.Scatter(
            x=monthly_data['YearMonth'].astype(str),
            y=monthly_data['TotalIncome'],
            mode='lines+markers',
            name='Income',
            line=dict(
                color=COLORS['primary'], 
                width=4,
                shape='spline'
            ),
            marker=dict(
                size=10, 
                symbol='diamond',
                color=COLORS['primary'],
                line=dict(color=COLORS['background'], width=2)
            ),
            hovertemplate='<b>%{x}</b><br>' +
                         '<span style="color: ' + COLORS['success'] + ';">Income: $%{y:,.0f}</span><extra></extra>',
            hoverlabel=self._get_standard_hoverlabel_config(COLORS['primary'])
        ))
        
        # Enhanced net amount line with premium styling
        fig.add_trace(go.Scatter(
            x=monthly_data['YearMonth'].astype(str),
            y=monthly_data['NetAmount'],
            mode='lines+markers',
            name='Net Amount',
            line=dict(
                color=COLORS['accent3'], 
                width=4, 
                dash='dash',
                shape='spline'
            ),
            marker=dict(
                size=10, 
                symbol='square',
                color=COLORS['accent3'],
                line=dict(color=COLORS['background'], width=2)
            ),
            hovertemplate='<b>%{x}</b><br>' +
                         '<span style="color: ' + COLORS['accent3'] + ';">Net: $%{y:,.0f}</span><extra></extra>',
            hoverlabel=self._get_standard_hoverlabel_config(COLORS['accent3'])
        ))
        
        # Enhanced cumulative net area with premium styling
        fig.add_trace(go.Scatter(
            x=monthly_data['YearMonth'].astype(str),
            y=monthly_data['CumulativeNet'],
            mode='lines',
            name='Cumulative Net',
            line=dict(
                color=COLORS['accent1'], 
                width=3,
                shape='spline'
            ),
            fill='tonexty',
            fillcolor=f'rgba({int(COLORS["accent1"][1:3], 16)}, {int(COLORS["accent1"][3:5], 16)}, {int(COLORS["accent1"][5:7], 16)}, 0.2)',
            hovertemplate='<b>%{x}</b><br>' +
                         '<span style="color: ' + COLORS['accent1'] + ';">Cumulative: $%{y:,.0f}</span><extra></extra>',
            hoverlabel=self._get_standard_hoverlabel_config(COLORS['accent1'])
        ))
        
        # Apply premium professional layout
        fig = self._apply_professional_layout(
            fig, 
            title='Monthly Financial Trends & Cumulative Growth',
            height=500
        )
        
        # Enhanced axes with premium styling
        # Convert YearMonth strings back to datetime for formatting
        yearmonth_dates = pd.to_datetime(monthly_data['YearMonth'] + '-01')
        
        fig.update_xaxes(
            title='Month',
            tickangle=45,
            tickmode='array',
            ticktext=yearmonth_dates.dt.strftime('%b %Y'),
            tickvals=monthly_data['YearMonth'].astype(str)
        )
        
        fig.update_yaxes(
            title='Amount ($)',
            tickformat='$,.0f',
            zeroline=True,
            zerolinecolor=COLORS['border'],
            zerolinewidth=2
        )
        
        # Enhanced hover mode for better interaction
        fig.update_layout(
            hovermode='x unified',
            hoverdistance=100,
            spikedistance=1000,
            # Enhanced legend configuration - positioned outside chart area
            showlegend=True,
            legend=self._get_standard_legend_config(),
            # Increase right margin to accommodate the legend
            margin=self._get_standard_margin_config()
        )
        
        return fig
    
    def create_category_breakdown_chart(self, category_data: pd.DataFrame) -> go.Figure:
        """
        Create premium category breakdown chart with enhanced styling
        
        Args:
            category_data: DataFrame with category summaries
            
        Returns:
            Plotly figure object
        """
        # Handle empty or invalid data
        if category_data.empty or category_data['Amount'].sum() == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=COLORS['text_muted'])
            )
            fig.update_layout(
                title='No Data Available',
                height=400,
                paper_bgcolor=COLORS['background'],
                plot_bgcolor=COLORS['surface']
            )
            return fig
        
        # Create individual pie chart for category distribution
        fig = go.Figure()
        
        # Enhanced pie chart with premium styling - completely redesigned for maximum text visibility
        fig.add_trace(
            go.Pie(
                labels=category_data['Category'],
                values=category_data['Amount'],
                name="Category Distribution",  # More descriptive name
                hole=0,  # No hole - solid pie chart
                marker=dict(
                    colors=[CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(category_data))],
                    line=dict(color=COLORS['background'], width=1)  # Thinner line for cleaner look
                ),
                textinfo='percent',
                textposition='inside',
                textfont=dict(
                    color=COLORS['text_primary'],
                    size=10,  # Smaller text to fit better in smaller slices
                    family='Inter, sans-serif'
                ),
            hovertemplate='<b>%{label}</b><br>' +
                         'Amount: $%{value:,.0f}<br>' +
                             'Percentage: %{percent:.1%}<extra></extra>',
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    bordercolor=COLORS['primary'],
                    font=dict(color=COLORS['text_primary'], size=12)
                )
            )
        )
        

        
        # Apply premium professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Category Distribution',
            height=500
        )
        
        # Enhanced layout for standalone pie chart with legend - positioned on right side
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # Move legend to right side, outside chart area (consistent with other charts)
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
                bordercolor=COLORS['border'],
                borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=10  # Increased font size for better readability
                ),
                itemsizing='constant',  # Consistent legend item sizes
                itemwidth=30  # Control legend item width (minimum valid value)
            ),
            margin=dict(l=80, r=120, t=100, b=100),  # Balanced margins: left=80, right=120 for legend
            height=500  # Optimized height for single chart
        )
        
        return fig
    
    def create_category_comparison_chart(self, category_data: pd.DataFrame) -> go.Figure:
        """
        Create standalone category comparison bar chart
        
        Args:
            category_data: DataFrame with category summaries
            
        Returns:
            Plotly figure object
        """
        # Handle empty or invalid data
        if category_data.empty or category_data['Amount'].sum() == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=COLORS['text_muted'])
            )
            fig.update_layout(
                title='No Data Available',
                height=400,
                paper_bgcolor=COLORS['background'],
                plot_bgcolor=COLORS['surface']
            )
            return fig
        
        # Create standalone horizontal bar chart
        fig = go.Figure()
        
        # Enhanced horizontal bar chart with premium styling
        fig.add_trace(
            go.Bar(
                y=category_data['Category'],  # Categories on Y-axis for horizontal bars
                x=category_data['Amount'],    # Amounts on X-axis
                name="Category Comparison",
                orientation='h',              # Horizontal orientation
                marker=dict(
                    color=[CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(category_data))],
                    line=dict(color=COLORS['background'], width=1),
                    opacity=0.8
                ),
                text=category_data['Amount'].apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
                textfont=dict(
                    color=COLORS['text_primary'],
                    size=10,
                    family='Inter, sans-serif'
                ),
                hovertemplate='<b>%{y}</b><br>' +
                             'Amount: $%{x:,.0f}<extra></extra>',
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    bordercolor=COLORS['primary'],
                    font=dict(color=COLORS['text_primary'], size=12)
                )
            )
        )
        
        # Apply premium professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Category Comparison',
            height=500
        )
        
        # Enhanced horizontal bar chart axes
        fig.update_xaxes(
            title="Amount ($)",
            tickformat='$,.0f'
        )
        
        fig.update_yaxes(
            title="Category"
        )
        
        # Enhanced layout for standalone bar chart
        fig.update_layout(
            showlegend=False,  # No legend needed for single chart
            margin=dict(l=80, r=50, t=100, b=100),
            height=500
        )
        
        return fig
    
    def create_category_trend_chart(self, expenses_data: pd.DataFrame, 
                                  search_context: str = None) -> go.Figure:
        """
        Create enhanced category trend chart with area and line combinations
        
        Args:
            expenses_data: DataFrame with expense data
            search_context: Optional search context for dynamic title
            
        Returns:
            Plotly figure object
        """
        # Handle empty data
        if expenses_data.empty or expenses_data['Amount'].sum() == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=COLORS['text_muted'])
            )
            fig.update_layout(
                title='No Data Available',
                height=400,
                paper_bgcolor=COLORS['background'],
                plot_bgcolor=COLORS['surface']
            )
            return fig
        
        # Group by month and category
        monthly_categories = expenses_data.groupby([
            expenses_data['Date'].dt.to_period('M'), 'Category'
        ])['Amount'].sum().reset_index()
        
        # Pivot data for stacked area chart
        pivot_data = monthly_categories.pivot(
            index='Date', columns='Category', values='Amount'
        ).fillna(0)
        
        # Convert Period index to string
        pivot_data.index = pivot_data.index.astype(str)
        
        # Create stacked area chart
        fig = go.Figure()
        
        # Add traces for each category with premium styling
        for i, category in enumerate(pivot_data.columns):
            color = CHART_COLORS[i % len(CHART_COLORS)]
            fig.add_trace(go.Scatter(
                x=pivot_data.index,
                y=pivot_data[category],
                name=category,
                fill='tonexty',
                line=dict(color=color, width=3, shape='spline'),
                marker=dict(size=8, color=color, line=dict(color=COLORS['background'], width=1)),
                stackgroup='one',
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Month: %{x}<br>' +
                             'Amount: $%{y:,.0f}<extra></extra>',
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    bordercolor=color,
                    font=dict(color=COLORS['text_primary'], size=12)
                )
            ))
        
        # Apply professional layout
        fig = self._apply_professional_layout(
            fig,
            title=f'Category Trends Over Time{f" - {search_context}" if search_context else ""}',
            height=500
        )
        
        # Update axes
        fig.update_xaxes(title='Month', tickangle=45)
        fig.update_yaxes(title='Amount ($)', tickformat='$,.0f')
        
        # Enhanced legend configuration - positioned outside chart area
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # Move legend outside chart area to prevent overlap
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][3:5], 16)}, 0.95)',
                bordercolor=COLORS['border'],
                borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=10
                ),
                itemsizing='constant',
                itemwidth=30
            ),
            # Increase right margin to accommodate the legend
            margin=dict(l=80, r=120, t=100, b=100)
        )
        
        return fig
    
    def create_city_comparison_chart(self, city_costs_data: pd.DataFrame, 
                                   selected_categories: List[str] = None) -> go.Figure:
        """
        Create enhanced city comparison with grouped bar chart
        
        Args:
            city_costs_data: DataFrame with city cost data
            selected_categories: List of categories to include
            
        Returns:
            Plotly figure object
        """
        if selected_categories is None:
            selected_categories = sorted(city_costs_data['Category'].unique())
        
        filtered_data = city_costs_data[city_costs_data['Category'].isin(selected_categories)]
        
        # Create grouped bar chart with premium styling
        fig = go.Figure()
        
        for i, category in enumerate(selected_categories):
            category_data = filtered_data[filtered_data['Category'] == category]
            color = CHART_COLORS[i % len(CHART_COLORS)]
            
            fig.add_trace(go.Bar(
                name=category,
                x=category_data['City'],
                y=category_data['MonthlyCost'],
                marker=dict(
                    color=color,
                    line=dict(color=COLORS['background'], width=1),
                    opacity=0.8
                ),
                hovertemplate='<b>%{x}</b><br>' +
                             'Category: %{fullData.name}<br>' +
                             'Monthly Cost: $%{y:,.0f}<extra></extra>',
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    bordercolor=color,
                    font=dict(color=COLORS['text_primary'], size=12)
                )
            ))
        
        # Apply professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Monthly Cost Comparison by City and Category',
            height=500
        )
        
        # Update layout for grouped bars with better spacing
        fig.update_layout(
            barmode='group',
            bargap=0.2,
            bargroupgap=0.15,
            margin=dict(l=80, r=120, t=100, b=100),  # Increased right margin for legend
            legend=dict(
                orientation="v",  # Changed to vertical for better fit
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # Move legend outside chart area to prevent overlap
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
                bordercolor=COLORS['border'],
                borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=10
                ),
                itemsizing='constant',
                itemwidth=30
            )
        )
        
        # Update axes with better alignment
        fig.update_xaxes(
            title='City',
            title_font=dict(size=14, color=COLORS['text_primary']),
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            tickangle=45,
            tickmode='array',
            ticktext=filtered_data['City'].unique(),
            tickvals=list(range(len(filtered_data['City'].unique())))
        )
        
        fig.update_yaxes(
            title='Monthly Cost ($)',
            title_font=dict(size=14, color=COLORS['text_primary']),
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            tickformat='$,.0f',
            gridcolor=COLORS['border'],
            gridwidth=0.5
        )
        
        return fig
    
    def create_salary_comparison_chart(self, salary_data: pd.DataFrame, 
                                     selected_cities: List[str] = None) -> go.Figure:
        """
        Create enhanced salary comparison with heatmap
        
        Args:
            salary_data: DataFrame with salary data
            selected_cities: List of cities to include
            
        Returns:
            Plotly figure object
        """
        if selected_cities is None:
            selected_cities = sorted(salary_data['City'].unique())
        
        filtered_data = salary_data[salary_data['City'].isin(selected_cities)]
        
        # Use 'AverageSalary' if present, else fallback to 'AnnualSalary'
        value_col = 'AverageSalary' if 'AverageSalary' in filtered_data.columns else 'AnnualSalary'
        pivot_data = filtered_data.pivot(index='Role', columns='City', values=value_col)
        
        # Create heatmap with premium styling
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale=[
                [0, COLORS['surface']],
                [0.25, COLORS['accent3']],
                [0.5, COLORS['accent2']],
                [0.75, COLORS['accent1']],
                [1, COLORS['primary']]
            ],
            text=pivot_data.values,
            texttemplate='$%{text:,.0f}',
            textfont=dict(size=10, color=COLORS['text_primary']),
            hoverongaps=False,
            hoverlabel=dict(
                bgcolor=COLORS['surface'],
                bordercolor=COLORS['primary'],
                font=dict(color=COLORS['text_primary'], size=12)
            )
        ))
        
        # Apply professional layout
        fig = self._apply_professional_layout(fig, title='Annual Salary by Role and City', height=600)
        
        # Update axes with better alignment
        fig.update_xaxes(
            title='City',
            title_font=dict(size=14, color=COLORS['text_primary']),
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            tickangle=45,
            tickmode='array',
            ticktext=pivot_data.columns,
            tickvals=list(range(len(pivot_data.columns)))
        )
        
        fig.update_yaxes(
            title='Role',
            title_font=dict(size=14, color=COLORS['text_primary']),
            tickfont=dict(size=11, color=COLORS['text_secondary'])
        )
        
        # Fix color bar label and improve layout
        fig.update_layout(
            coloraxis_colorbar=dict(
                title='Annual Salary ($)',
                title_font=dict(size=12, color=COLORS['text_primary']),
                tickfont=dict(size=10, color=COLORS['text_secondary']),
                tickformat='$,.0f',
                len=0.8,
                y=0.5,
                yanchor='middle'
            ),
            margin=dict(l=80, r=120, t=100, b=100)
        )
        
        return fig
    
    def create_roi_analysis_chart(self, roi_data: Dict) -> go.Figure:
        """
        Create enhanced ROI analysis with degree cost vs salaries chart
        
        Args:
            roi_data: Dictionary containing ROI analysis data
            
        Returns:
            Plotly figure object
        """
        # Create standalone chart for degree cost vs salaries
        fig = go.Figure()
        
        # Get scenarios with validation
        scenarios = roi_data.get('scenarios', {})
        total_degree_cost = roi_data.get('total_degree_cost', 0)
        
        # Validate data
        if not scenarios or total_degree_cost == 0:
            # Handle empty data case
            fig.add_annotation(
                text="No ROI data available for the selected filters",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=COLORS['text_muted'])
            )
            fig.update_layout(
                title='No Data Available',
                height=400,
                paper_bgcolor=COLORS['background'],
                plot_bgcolor=COLORS['surface']
            )
            return fig
        
        # Scenario comparison bar chart
        scenario_names = list(scenarios.keys())
        scenario_salaries = [scenarios[name].get('annual_salary', 0) for name in scenario_names]
        
        # Create proper labels for the bar chart with premium styling
        bar_labels = ['Degree Cost'] + [name.title() for name in scenario_names]
        bar_values = [total_degree_cost] + scenario_salaries
        bar_colors = [COLORS['error']] + CHART_COLORS[:len(scenario_names)]
        
        # Add individual traces for each scenario to enable legend control
        # Degree Cost bar
        fig.add_trace(
            go.Bar(
                x=['Degree Cost'],
                y=[total_degree_cost],
                name='Degree Cost',
                marker=dict(
                    color=COLORS['error'],
                    line=dict(color=COLORS['background'], width=1),
                    opacity=0.8
                ),
                text=[f'${total_degree_cost:,.0f}'],
                textposition='auto',
                textfont=dict(color=COLORS['text_primary'], size=11),
                showlegend=True,
                hovertemplate='<b>Degree Cost</b><br>' +
                             'Amount: $%{y:,.0f}<extra></extra>',
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    bordercolor=COLORS['error'],
                    font=dict(color=COLORS['text_primary'], size=12)
                )
            )
        )
        
        # Add individual bars for each salary scenario
        for i, (scenario_name, salary) in enumerate(zip(scenario_names, scenario_salaries)):
            color = CHART_COLORS[i % len(CHART_COLORS)]
            fig.add_trace(
                go.Bar(
                    x=[scenario_name.title()],
                    y=[salary],
                    name=f'{scenario_name.title()} Salary',
                    marker=dict(
                        color=color,
                        line=dict(color=COLORS['background'], width=1),
                        opacity=0.8
                    ),
                    text=[f'${salary:,.0f}'],
                    textposition='auto',
                    textfont=dict(color=COLORS['text_primary'], size=11),
                    showlegend=True,
                    hovertemplate=f'<b>{scenario_name.title()}</b><br>' +
                                 'Salary: $%{y:,.0f}<extra></extra>',
                    hoverlabel=dict(
                        bgcolor=COLORS['surface'],
                        bordercolor=color,
                        font=dict(color=COLORS['text_primary'], size=12)
                    )
                )
            )
             
        # Apply professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Degree Cost vs Target Salaries',
            height=500
        )
        
        # Update axes for standalone chart
        fig.update_xaxes(title_text="Scenarios")
        fig.update_yaxes(title_text="Amount ($)", tickformat='$,.0f')
        
        # Enhanced legend configuration - positioned outside chart area
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # Move legend outside chart area to prevent overlap
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
                bordercolor=COLORS['border'],
                borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=10
                ),
                itemsizing='constant',
                itemwidth=30
            ),
            # Increase right margin to accommodate the legend
            margin=dict(l=80, r=120, t=100, b=100)
        )
        
        return fig
    
    def create_break_even_timeline_chart(self, roi_data: Dict) -> go.Figure:
        """
        Create standalone break-even timeline chart
        
        Args:
            roi_data: Dictionary containing ROI analysis data
            
        Returns:
            Plotly figure object
        """
        # Create standalone chart for break-even timeline
        fig = go.Figure()
        
        # Get scenarios
        scenarios = roi_data.get('scenarios', {})
        total_degree_cost = roi_data['total_degree_cost']
        extended_months = 25  # Default value for x-axis range
        cumulative_savings = []  # Default empty list for y-axis range calculation
        
        # Break-even timeline for realistic scenario
        if 'realistic' in scenarios:
            realistic = scenarios['realistic']
            job_search_months = realistic['job_search_months']
            break_even_months = realistic['break_even_months']
            total_months = job_search_months + break_even_months
            
            # Extend timeline beyond break-even to show positive savings
            extended_months = int(total_months + 6)  # Add 6 more months to show positive trend
            extended_months = max(extended_months, 30)  # Ensure minimum 30 months for better visualization
            
            # Create timeline data
            months = list(range(extended_months + 1))
            cumulative_savings = []
            
            for month in months:
                if month <= job_search_months:
                    # During job search: no income, accumulating debt
                    cumulative_savings.append(-total_degree_cost)
                else:
                    # After job: earning and saving
                    working_months = month - job_search_months
                    savings = realistic['monthly_savings'] * working_months
                    cumulative_savings.append(savings - total_degree_cost)
            
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=cumulative_savings,
                    mode='lines+markers',
                    name='Realistic Break-even Timeline',
                    line=dict(color=COLORS['primary'], width=4, shape='spline'),
                    marker=dict(
                        size=10, 
                        color=COLORS['primary'],
                        line=dict(color=COLORS['background'], width=2)
                    ),
                    showlegend=True,
                    hovertemplate='<b>Month %{x}</b><br>' +
                                 'Cumulative: $%{y:,.0f}<extra></extra>',
                    hoverlabel=dict(
                        bgcolor=COLORS['surface'],
                        bordercolor=COLORS['primary'],
                        font=dict(color=COLORS['text_primary'], size=12)
                    )
                )
            )
            
            # Add break-even line (horizontal line at $0)
            fig.add_hline(y=0, line_dash="dash", line_color=COLORS['text_primary'])
            
            # Add job search period indicator
            fig.add_vline(x=job_search_months, line_dash="dot", line_color=COLORS['warning'])
            
            # Add job search annotation - styled like Timeline chart
            fig.add_annotation(
                x=job_search_months,
                y=0,
                xref="x",
                yref="y",
                text="Job Search Ends",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=COLORS['warning'],
                font=dict(
                    size=12, 
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif'
                ),
                bgcolor=f'rgba({int(COLORS["warning"][1:3], 16)}, {int(COLORS["warning"][3:5], 16)}, {int(COLORS["warning"][5:7], 16)}, 0.95)',
                bordercolor=COLORS['warning'],
                borderwidth=2,
                align='center',
                xanchor='center',
                yanchor='bottom'
            )
        
            # Find and mark the actual break-even point
            break_even_month = None
            for i, savings in enumerate(cumulative_savings):
                if savings >= 0:
                    break_even_month = i
                    break
            
            if break_even_month is not None:
                # Add break-even point annotation - styled like Timeline chart
                fig.add_annotation(
                    x=break_even_month,
                    y=0,
                    xref="x",
                    yref="y",
                    text="Break-even Point",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=COLORS['success'],
                    font=dict(
                        size=12, 
                        color=COLORS['text_primary'],
                        family='Inter, sans-serif'
                    ),
                    bgcolor=f'rgba({int(COLORS["success"][1:3], 16)}, {int(COLORS["success"][3:5], 16)}, {int(COLORS["success"][5:7], 16)}, 0.95)',
                    bordercolor=COLORS['success'],
                    borderwidth=2,
                    align='center',
                    xanchor='center',
                    yanchor='bottom'
                )
                
                # Add a marker at the break-even point
                fig.add_trace(
                    go.Scatter(
                        x=[break_even_month],
                        y=[0],
                        mode='markers',
                        name='Break-even Point',
                        marker=dict(
                            size=15,
                            color=COLORS['success'],
                            symbol='star',
                            line=dict(color='white', width=2)
                        ),
                        showlegend=False
                    )
                )
                
                # Add positive trend annotation
                if break_even_month < extended_months - 5:
                    positive_month = break_even_month + 3
                    positive_savings = cumulative_savings[min(positive_month, len(cumulative_savings) - 1)]
                    if positive_savings > 0:
                        fig.add_annotation(
                            x=positive_month,
                            y=positive_savings,
                            xref="x",
                            yref="y",
                            text="Positive Savings Trend",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor=COLORS['success'],
                            font=dict(
                                size=12, 
                                color=COLORS['text_primary'],
                                family='Inter, sans-serif'
                            ),
                            bgcolor=f'rgba({int(COLORS["success"][1:3], 16)}, {int(COLORS["success"][3:5], 16)}, {int(COLORS["success"][5:7], 16)}, 0.95)',
                            bordercolor=COLORS['success'],
                            borderwidth=2,
                            align='center',
                            xanchor='center',
                            yanchor='bottom'
                        )
        
        # Apply professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Break-even Timeline',
            height=500
        )
        
        # Update axes for standalone chart
        fig.update_xaxes(title_text="Months", range=[0, extended_months], 
                        gridcolor='rgba(0,0,0,0.1)', showgrid=True)
        
        # Calculate y-axis range for better visualization
        if 'realistic' in scenarios and cumulative_savings:
            y_min = min(cumulative_savings) - 5000  # Add buffer below minimum
            y_max = max(cumulative_savings) + 5000   # Add buffer above maximum
            fig.update_yaxes(title_text="Cumulative Savings ($)", 
                           tickformat='$,.0f', range=[y_min, y_max])
        else:
            fig.update_yaxes(title_text="Cumulative Savings ($)", tickformat='$,.0f')
        
        # Enhanced legend configuration - positioned outside chart area
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # Move legend outside chart area to prevent overlap
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
                bordercolor=COLORS['border'],
                borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=10
                ),
                itemsizing='constant',
                itemwidth=30
            ),
            # Increase right margin to accommodate the legend
            margin=dict(l=80, r=120, t=100, b=100)
        )
        
        return fig
    
    def create_anomaly_detection_chart(self, expenses_data: pd.DataFrame, 
                                     anomalies: pd.DataFrame) -> go.Figure:
        """
        Create enhanced anomaly detection chart with statistical analysis
        
        Args:
            expenses_data: DataFrame with expense data
            anomalies: DataFrame with detected anomalies
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Add all expenses as scatter points with premium styling
        fig.add_trace(go.Scatter(
            x=expenses_data['Date'],
            y=expenses_data['Amount'],
            mode='markers',
            name='All Expenses',
            marker=dict(
                color=COLORS['primary'],
                size=8,
                opacity=0.7,
                line=dict(color=COLORS['background'], width=1)
            ),
            hovertemplate='<b>%{x}</b><br>' +
                         'Amount: $%{y:,.0f}<extra></extra>',
            hoverlabel=dict(
                bgcolor=COLORS['surface'],
                bordercolor=COLORS['primary'],
                font=dict(color=COLORS['text_primary'], size=12)
            )
        ))
        
        # Add anomalies as highlighted points with premium styling
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
            x=anomalies['Date'],
            y=anomalies['Amount'],
            mode='markers',
            name='Anomalies',
            marker=dict(
                color=COLORS['warning'],
                size=16,
                symbol='diamond',
                line=dict(color=COLORS['background'], width=2)
                ),
                hovertemplate='<b>%{x}</b><br>' +
                             'Amount: $%{y:,.0f}<br>' +
                             'ANOMALY<extra></extra>',
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    bordercolor=COLORS['warning'],
                    font=dict(color=COLORS['text_primary'], size=12)
                )
        ))
        
        # Add trend line with premium styling
        z = np.polyfit(expenses_data['Date'].astype(np.int64), expenses_data['Amount'], 1)
        p = np.poly1d(z)
        
        fig.add_trace(go.Scatter(
            x=expenses_data['Date'],
            y=p(expenses_data['Date'].astype(np.int64)),
            mode='lines',
            name='Trend Line',
            line=dict(color=COLORS['accent2'], width=3, dash='dash', shape='spline'),
            hovertemplate='<b>Trend Line</b><br>' +
                         'Amount: $%{y:,.0f}<extra></extra>',
            hoverlabel=dict(
                bgcolor=COLORS['surface'],
                bordercolor=COLORS['accent2'],
                font=dict(color=COLORS['text_primary'], size=12)
            )
        ))
        
        # Add statistical bands
        mean_amount = expenses_data['Amount'].mean()
        std_amount = expenses_data['Amount'].std()
        
        # Upper and lower bounds with premium styling
        upper_bound = mean_amount + 2 * std_amount
        lower_bound = mean_amount - 2 * std_amount
        
        fig.add_hline(
            y=upper_bound, 
            line_dash="dot", 
            line_color=COLORS['warning'],
            line_width=2,
            annotation=dict(
                text="Upper Bound (2σ)",
                font=dict(
                    color=COLORS['warning'],
                    size=10,
                    family='Inter, sans-serif'
                ),
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.9)',
                bordercolor=COLORS['warning']
            )
        )
        fig.add_hline(
            y=lower_bound, 
            line_dash="dot", 
            line_color=COLORS['warning'],
            line_width=2,
            annotation=dict(
                text="Lower Bound (2σ)",
                font=dict(
                    color=COLORS['warning'],
                    size=10,
                    family='Inter, sans-serif'
                ),
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.9)',
                bordercolor=COLORS['warning']
            )
        )
        
        # Apply professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Anomaly Detection in Expenses with Statistical Bands',
            height=500
        )
        
        # Update axes
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Amount ($)', tickformat='$,.0f')
        
        # Enhanced legend configuration - positioned outside chart area
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # Move legend outside chart area to prevent overlap
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
                bordercolor=COLORS['border'],
                borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=10
                ),
                itemsizing='constant',
                itemwidth=30
            ),
            # Increase right margin to accommodate the legend
            margin=dict(l=80, r=120, t=100, b=100)
        )
        
        return fig
    
    def create_payment_pie_chart(self, expenses_data: pd.DataFrame) -> go.Figure:
        """
        Create payment type distribution pie chart
        
        Args:
            expenses_data: DataFrame with expense data including PaymentType column
            
        Returns:
            Plotly figure object
        """
        # Group by payment type and sum amounts
        payment_summary = expenses_data.groupby('PaymentType')['Amount'].sum().reset_index()
        
        # Create pie chart with premium styling
        fig = go.Figure(data=[go.Pie(
            labels=payment_summary['PaymentType'],
            values=payment_summary['Amount'],
            hole=0.4,
            textinfo='percent',
            textposition='inside',
            insidetextorientation='radial',
            marker=dict(
                colors=[CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(payment_summary))],
                line=dict(color=COLORS['background'], width=2)
            ),
            textfont=dict(
                color=COLORS['text_primary'],
                size=12,
                family='Inter, sans-serif'
            ),
            hovertemplate='<b>%{label}</b><br>' +
                         'Amount: $%{value:,.0f}<br>' +
                         'Percentage: %{percent:.1%}<extra></extra>',
            hoverlabel=dict(
                bgcolor=COLORS['surface'],
                bordercolor=COLORS['primary'],
                font=dict(color=COLORS['text_primary'], size=12)
            )
        )])
        
        # Apply professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Expense Distribution by Payment Type',
            height=400
        )
        
        # Update layout for better pie chart display with premium styling
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.9)',
                bordercolor=COLORS['border'],
            borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=11
                )
            )
        )
        
        return fig
    
    def create_timeline_chart(self, milestones: List[Dict]) -> go.Figure:
        """
        Create enhanced timeline chart with interactive elements
        
        Args:
            milestones: List of milestone dictionaries
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Create timeline visualization
        for i, milestone in enumerate(milestones):
            label = milestone.get('event', '')
            milestone_type = milestone.get('type', 'general')
            
            # Color coding based on milestone type
            if milestone_type == 'academic':
                color = COLORS['primary']
                symbol = 'diamond'
            elif milestone_type == 'employment':
                color = COLORS['success']
                symbol = 'star'
            elif milestone_type == 'personal':
                color = COLORS['accent1']
                symbol = 'circle'
            elif milestone_type == 'financial':
                color = COLORS['warning']
                symbol = 'square'
            else:
                color = COLORS['text_muted']
                symbol = 'diamond'
            
            fig.add_trace(go.Scatter(
                x=[milestone['date']],
                y=[i],
                mode='markers',
                name=label,
                marker=dict(
                    size=24,
                    color=color,
                    symbol=symbol,
                    line=dict(color=COLORS['background'], width=2)
                ),
                showlegend=False,
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             '<b>Date:</b> %{x}<br>' +
                             '<b>Type:</b> ' + milestone_type.title() + '<br>' +
                             '<b>Impact:</b> ' + milestone.get('impact', 'N/A') + '<br>' +
                             '<b>Financial:</b> ' + milestone.get('financial_implication', 'N/A') + '<extra></extra>',
                hoverlabel=dict(
                    bgcolor=COLORS['surface'],
                    bordercolor=color,
                    font=dict(color=COLORS['text_primary'], size=12)
                )
            ))
            
            # Add milestone label as annotation with premium styling
            fig.add_annotation(
                x=milestone['date'],
                y=i,
                text=label,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=color,
                ax=100,
                ay=0,
                font=dict(
                    size=12, 
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif'
                ),
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
                bordercolor=color,
                borderwidth=2,
                align='left',
                xanchor='left',
                yanchor='middle'
            )
        
        # Apply professional layout
        fig = self._apply_professional_layout(
            fig,
            title='Academic Journey Timeline with Impact Analysis',
            height=500
        )
        
        # Update axes
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Milestone', showticklabels=False)
        
        # Enhanced legend configuration - positioned outside chart area
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.02,  # Move legend outside chart area to prevent overlap
                bgcolor=f'rgba({int(COLORS["surface"][1:3], 16)}, {int(COLORS["surface"][3:5], 16)}, {int(COLORS["surface"][5:7], 16)}, 0.95)',
                bordercolor=COLORS['border'],
                borderwidth=1,
                font=dict(
                    color=COLORS['text_primary'],
                    family='Inter, sans-serif',
                    size=10
                ),
                itemsizing='constant',
                itemwidth=30
            ),
            # Increase right margin to accommodate the legend
            margin=dict(l=80, r=120, t=100, b=100)
        )
        
        return fig


def main():
    """Test the visualization module"""
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'YearMonth': pd.date_range('2023-01-01', periods=12, freq='M'),
        'TotalExpenses': [1000, 1200, 1100, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100],
        'TotalIncome': [2000, 2200, 2100, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100],
        'NetAmount': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        'CumulativeNet': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
    })
    
    # Test visualization
    viz = DashboardVisualizations()
    fig = viz.create_monthly_trend_chart(sample_data)
    fig.show()


if __name__ == "__main__":
    main() 