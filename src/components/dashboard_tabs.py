"""
Dashboard Tab Components
Professional tab implementations with consistent architecture and styling
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
import plotly.express as px
import time

from ..utils.error_handler import ErrorHandler
from ..utils.cache_manager import CacheManager
from config.settings import format_currency, format_percentage
from config.design_system import (
    COLORS, FONT_SIZES, FONT_WEIGHTS, SPACING, 
    BORDER_RADIUS, SHADOWS, FONT_FAMILY
)

class BaseTab:
    """Base class for all dashboard tabs with common functionality"""
    
    def __init__(self, error_handler: ErrorHandler = None, cache_manager: CacheManager = None):
        """Initialize base tab with optional dependencies"""
        self.error_handler = error_handler or ErrorHandler()
        self.cache_manager = cache_manager or CacheManager()
    
    def render(self):
        """Render the tab content - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement render method")
    
    def safe_render(self):
        """Safely render tab content with error handling"""
        try:
            self.render()
        except Exception as e:
            self.error_handler.display_error(
                f"{self.__class__.__name__} Error",
                str(e),
                context={"tab": self.__class__.__name__}
            )
    
    def _render_section_header(self, title: str, subtitle: str = None, level: int = 2):
        """Render consistent section headers with unified design system"""
        header_tag = f"h{level}"
        
        if subtitle:
            st.markdown(f"""
            <div style="
                margin: {SPACING['8']} 0 {SPACING['6']} 0;
                padding: {SPACING['4']} 0;
            ">
                <{header_tag} style="
                    color: {COLORS['text_primary']};
                    font-size: {FONT_SIZES['3xl']};
                    font-weight: {FONT_WEIGHTS['bold']};
                    margin: 0;
                    font-family: {FONT_FAMILY};
                    display: flex;
                    align-items: center;
                    gap: {SPACING['3']};
                ">
                    {title}
                </{header_tag}>
                <p style="
                    color: {COLORS['text_secondary']};
                    font-size: {FONT_SIZES['base']};
                    font-weight: {FONT_WEIGHTS['normal']};
                    margin: {SPACING['2']} 0 0 0;
                    font-family: {FONT_FAMILY};
                ">{subtitle}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                margin: {SPACING['8']} 0 {SPACING['6']} 0;
                padding: {SPACING['4']} 0;
            ">
                <{header_tag} style="
                    color: {COLORS['text_primary']};
                    font-size: {FONT_SIZES['3xl']};
                    font-weight: {FONT_WEIGHTS['bold']};
                    margin: 0;
                    font-family: {FONT_FAMILY};
                ">
                    {title}
                </{header_tag}>
            </div>
            """, unsafe_allow_html=True)

class OverviewTab(BaseTab):
    """Overview tab with key financial metrics and trends"""
    
    def __init__(self, processor, data, viz):
        """Initialize overview tab"""
        super().__init__()
        self.processor = processor
        self.data = data
        self.viz = viz
    
    def render(self):
        """Render overview tab content"""
        # Enhanced main header with unified design system
        st.markdown(f"""
        <div class="dashboard-card" style="
            background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%);
            padding: {SPACING['8']};
            border-radius: {BORDER_RADIUS['xl']};
            margin-bottom: {SPACING['8']};
            text-align: center;
            border: 1px solid {COLORS['border']};
            box-shadow: {SHADOWS['xl']};
        ">
            <h1 style="
                color: {COLORS['text_primary']};
                font-size: {FONT_SIZES['4xl']};
                font-weight: {FONT_WEIGHTS['extrabold']};
                margin: 0;
                font-family: {FONT_FAMILY};
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            ">Financial Overview</h1>
            <p style="
                color: {COLORS['text_secondary']};
                font-size: {FONT_SIZES['lg']};
                font-weight: {FONT_WEIGHTS['medium']};
                margin: {SPACING['2']} 0 0 0;
                font-family: {FONT_FAMILY};
                opacity: 0.9;
            ">Comprehensive analysis of your financial journey</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics section
        self._render_key_metrics()
        
        # Financial trends section
        self._render_financial_trends()
        
        # Category breakdown section
        self._render_category_breakdown()
    
    def _render_key_metrics(self):
        """Render key financial metrics with standardized styling"""
        self._render_section_header("Key Financial Metrics", "Essential financial indicators for informed decision-making")
        
        try:
            # Calculate key metrics
            expenses = self.data['expenses']
            salary = self.data['salary']
            
            total_expenses = expenses['Amount'].sum()
            total_income = salary['Amount'].sum() if not salary.empty else 0
            net_amount = total_income - total_expenses
            
            # Calculate average monthly expenses (excluding tuition)
            monthly_expenses = expenses[expenses['Category'] != 'Tuition'].copy()
            avg_monthly_expenses = monthly_expenses.groupby(
                monthly_expenses['Date'].dt.to_period('M')
            )['Amount'].sum().mean()
            
            # Display metrics in professional layout
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                self._render_metric_card(
                    title="Total Expenses",
                    value=format_currency(total_expenses),
                    subtitle="Total Outflow",
                    value_color=COLORS['error'],  # Red for expenses
                    help="Sum of all recorded expenses"
                )
            
            with col2:
                self._render_metric_card(
                    title="Total Income",
                    value=format_currency(total_income),
                    subtitle="Total Inflow",
                    value_color=COLORS['success'],  # Green for income
                    help="Sum of all recorded income"
                )
            
            with col3:
                # Enhanced Net Amount metric with relevant information
                if net_amount > 0:
                    # Positive (Green)
                    net_amount_color = COLORS['success']
                    net_amount_subtitle = "Income exceeds expenses"
                elif net_amount < 0:
                    # Negative (Red)
                    net_amount_color = COLORS['error']
                    net_amount_subtitle = "Expenses exceed income"
                else:
                    # Neutral (Yellow/Orange)
                    net_amount_color = COLORS['warning']
                    net_amount_subtitle = "Income equals expenses"
                
                # Format net amount without minus sign for display
                display_amount = abs(net_amount)
                display_value = format_currency(display_amount)
                
                self._render_metric_card(
                    title="Net Amount",
                    value=display_value,
                    subtitle=net_amount_subtitle,
                    value_color=net_amount_color,
                    subtitle_color=COLORS['text_muted'],
                    help="Income minus expenses"
                )
            
                with col4:
                    self._render_metric_card(
                        title="Avg Monthly Expenses",
                        value=format_currency(avg_monthly_expenses),
                        subtitle="Monthly Average",
                        value_color=COLORS['warning'],  # Yellow/Orange for averages
                        help="Average monthly spending (excluding tuition)"
                    )
            
            # Tuition information
            tuition_total = expenses[expenses['Category'] == 'Tuition']['Amount'].sum()
            if tuition_total > 0:
                st.markdown("### Tuition Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    self._render_metric_card(
                        title="Total Tuition",
                        value=format_currency(tuition_total),
                        subtitle="Education Investment",
                        value_color=COLORS['accent1'],  # Purple for education
                        help="Total tuition paid"
                    )
                
                with col2:
                    tuition_months = expenses[
                        expenses['Category'] == 'Tuition'
                    ]['Date'].dt.to_period('M').nunique()
                    avg_tuition_per_semester = tuition_total / tuition_months if tuition_months > 0 else 0
                    
                    self._render_metric_card(
                        title="Avg Tuition per Semester",
                        value=format_currency(avg_tuition_per_semester),
                        subtitle="Per Semester",
                        value_color=COLORS['accent1'],  # Light purple for semester average
                        help="Average tuition per semester"
                    )
                
                st.info(f"**Tuition Details:** Total of {format_currency(tuition_total)} paid over {tuition_months} months.")
        
        except Exception as e:
            self.error_handler.display_error("Metrics Calculation Error", str(e))
    
    def _render_metric_card(self, title, value, subtitle, value_color, subtitle_color=None, help=None):
        """Render a standardized metric card with premium styling"""
        if subtitle_color is None:
            subtitle_color = COLORS['text_muted']  # Default muted color
        
        # Create a subtle background color based on the value color
        bg_color = f"rgba({int(value_color[1:3], 16)}, {int(value_color[3:5], 16)}, {int(value_color[5:7], 16)}, 0.1)"
        border_color = f"rgba({int(value_color[1:3], 16)}, {int(value_color[3:5], 16)}, {int(value_color[5:7], 16)}, 0.3)"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {bg_color} 0%, rgba(26, 31, 46, 0.8) 100%);
            border: 1px solid {border_color};
            border-radius: {BORDER_RADIUS['lg']};
            padding: {SPACING['6']};
            box-shadow: {SHADOWS['lg']};
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='{SHADOWS['xl']}'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='{SHADOWS['lg']}'">
            <div style="
                color: {COLORS['text_primary']};
                font-size: {FONT_SIZES['sm']};
                font-weight: {FONT_WEIGHTS['medium']};
                margin-bottom: {SPACING['2']};
                display: flex;
                align-items: center;
                justify-content: center;
                gap: {SPACING['2']};
                font-family: {FONT_FAMILY};
            ">
                {title}
                {f'<span style="color: {COLORS["text_primary"]}; font-size: {FONT_SIZES["xs"]}; opacity: 0.8;" title="{help}">Info</span>' if help else ''}
            </div>
            <div style="
                color: {value_color};
                font-size: {FONT_SIZES['4xl']};
                font-weight: {FONT_WEIGHTS['extrabold']};
                margin-bottom: {SPACING['3']};
                font-family: {FONT_FAMILY};
                letter-spacing: -0.025em;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            ">
                {value}
            </div>
            <div style="
                color: {COLORS['text_primary']};
                font-size: {FONT_SIZES['sm']};
                font-weight: {FONT_WEIGHTS['semibold']};
                opacity: 0.9;
                font-family: {FONT_FAMILY};
                letter-spacing: 0.025em;
            ">
                {subtitle}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_financial_trends(self):
        """Render financial trends visualization"""
        self._render_section_header("Financial Trends", "Track your financial patterns and identify opportunities", level=3)
        
        try:
            # Get monthly summary data
            monthly_data = self.processor.get_monthly_summary()
            if not monthly_data.empty:
                trend_chart = self.viz.create_monthly_trend_chart(monthly_data)
                st.plotly_chart(trend_chart, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No trend data available")
        
        except Exception as e:
            self.error_handler.display_error("Trend Visualization Error", str(e))
    
    def _render_category_breakdown(self):
        """Render expense category breakdown"""
        self._render_section_header("Expense Categories", "Analyze your spending patterns by category", level=3)
        
        try:
            expenses = self.data['expenses']
            
            # Category breakdown - individual charts
            category_breakdown = self.processor.get_category_breakdown()
            
            # Create two columns for individual charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Category Distribution pie chart
                category_chart = self.viz.create_category_breakdown_chart(category_breakdown)
                st.plotly_chart(category_chart, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                # Category Comparison bar chart
                comparison_chart = self.viz.create_category_comparison_chart(category_breakdown)
                st.plotly_chart(comparison_chart, use_container_width=True, config={'displayModeBar': False})
            
            # Category trends over time
            st.markdown("### Category Trends Over Time")
            category_trend_chart = self.viz.create_category_trend_chart(expenses)
            st.plotly_chart(category_trend_chart, use_container_width=True, config={'displayModeBar': False})
        
        except Exception as e:
            self.error_handler.display_error("Category Analysis Error", str(e))

class ExpensesTab(BaseTab):
    """Expenses analysis tab with detailed breakdowns"""
    
    def __init__(self, processor, data, viz):
        """Initialize expenses tab"""
        super().__init__()
        self.processor = processor
        self.data = data
        self.viz = viz
    
    def render(self):
        """Render expenses tab content"""
        st.markdown("## Detailed Expense Analysis")
        
        # Anomaly detection
        self._render_anomaly_detection()
        
        # City comparison
        self._render_city_comparison()
        
        # Payment analysis
        self._render_payment_analysis()
    
    def _render_anomaly_detection(self):
        """Render anomaly detection section"""
        st.markdown("### Anomaly Detection")
        
        try:
            anomalies = self.processor.get_anomalies()
            
            if not anomalies.empty:
                st.warning(f"{len(anomalies)} spending anomalies detected!")
                
                # Anomaly chart
                anomaly_chart = self.viz.create_anomaly_detection_chart(
                    self.data['expenses'], anomalies
                )
                st.plotly_chart(anomaly_chart, use_container_width=True, config={'displayModeBar': False})
                
                # Anomaly details
                st.markdown("#### Anomaly Details")
                anomaly_display = anomalies[['Date', 'Category', 'Amount', 'PaymentType']].head(10).copy()
                anomaly_display['Date'] = anomaly_display['Date'].dt.date
                st.dataframe(anomaly_display, use_container_width=True, hide_index=True)
            else:
                st.success("No significant anomalies detected in your spending patterns.")
        
        except Exception as e:
            self.error_handler.display_error("Anomaly Detection Error", str(e))
    
    def _render_city_comparison(self):
        """Render payment type comparison section"""
        from config.design_system import COLORS
        
        st.markdown("### Payment Type Analysis")
        
        try:
            expenses = self.data['expenses']
            
            # Calculate payment type metrics
            payment_metrics = expenses.groupby('PaymentType').agg({
                'Amount': ['sum', 'mean', 'count'],
                'Category': 'nunique'
            }).round(2)
            
            # Flatten column names
            payment_metrics.columns = ['Total Expenses', 'Average Expense', 'Transaction Count', 'Unique Categories']
            payment_metrics = payment_metrics.sort_values('Total Expenses', ascending=False)
            
            # Display payment type metrics
            st.markdown("#### Payment Method Overview")
            st.dataframe(payment_metrics, use_container_width=True)
            
            # Create visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Total expenses by payment type - Premium styling
                fig1 = px.bar(
                    x=payment_metrics.index,
                    y=payment_metrics['Total Expenses'],
                    title='Total Expenses by Payment Method',
                    labels={'x': 'Payment Method', 'y': 'Total Expenses ($)'},
                    color=payment_metrics['Total Expenses'],
                    color_continuous_scale=[COLORS['primary'], COLORS['accent1'], COLORS['accent4'], COLORS['success']]
                )
                
                # Apply premium styling
                fig1.update_layout(
                    height=400,
                    xaxis_tickangle=45,
                    paper_bgcolor=COLORS['background'],
                    plot_bgcolor=COLORS['surface'],
                    title={
                        'text': 'Total Expenses by Payment Method',
                        'x': 0.5,
                        'xanchor': 'center',
                        'y': 0.95,
                        'yanchor': 'top',
                        'font': dict(
                            size=18,
                            color=COLORS['text_primary'],
                            family='Inter, sans-serif'
                        )
                    },
                    font=dict(
                        family='Inter, sans-serif',
                        color=COLORS['text_secondary']
                    ),
                    margin=dict(l=80, r=50, t=80, b=80)
                )
                
                # Update axes with premium styling
                fig1.update_xaxes(
                    title_font=dict(size=14, color=COLORS['text_primary']),
                    tickfont=dict(size=11, color=COLORS['text_secondary']),
                    gridcolor=COLORS['grid'],
                    gridwidth=0.5,
                    zerolinecolor=COLORS['grid'],
                    zerolinewidth=1
                )
                
                fig1.update_yaxes(
                    title_font=dict(size=14, color=COLORS['text_primary']),
                    tickfont=dict(size=11, color=COLORS['text_secondary']),
                    gridcolor=COLORS['grid'],
                    gridwidth=0.5,
                    zerolinecolor=COLORS['grid'],
                    zerolinewidth=1
                )
                
                # Update bars with premium styling
                fig1.update_traces(
                    marker=dict(
                        line=dict(color=COLORS['background'], width=1),
                        opacity=0.85
                    ),
                    hovertemplate='<b>%{x}</b><br>' +
                                 'Total Expenses: $%{y:,.0f}<extra></extra>',
                    hoverlabel=dict(
                        bgcolor=COLORS['surface'],
                        bordercolor=COLORS['primary'],
                        font=dict(color=COLORS['text_primary'], size=12)
                    )
                )
                
                st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                # Average expense by payment type - Premium styling
                fig2 = px.bar(
                    x=payment_metrics.index,
                    y=payment_metrics['Average Expense'],
                    title='Average Expense by Payment Method',
                    labels={'x': 'Payment Method', 'y': 'Average Expense ($)'},
                    color=payment_metrics['Average Expense'],
                    color_continuous_scale=[COLORS['accent2'], COLORS['accent3'], COLORS['warning'], COLORS['error']]
                )
                
                # Apply premium styling
                fig2.update_layout(
                    height=400,
                    xaxis_tickangle=45,
                    paper_bgcolor=COLORS['background'],
                    plot_bgcolor=COLORS['surface'],
                    title={
                        'text': 'Average Expense by Payment Method',
                        'x': 0.5,
                        'xanchor': 'center',
                        'y': 0.95,
                        'yanchor': 'top',
                        'font': dict(
                            size=18,
                            color=COLORS['text_primary'],
                            family='Inter, sans-serif'
                        )
                    },
                    font=dict(
                        family='Inter, sans-serif',
                        color=COLORS['text_secondary']
                    ),
                    margin=dict(l=80, r=50, t=80, b=80)
                )
                
                # Update axes with premium styling
                fig2.update_xaxes(
                    title_font=dict(size=14, color=COLORS['text_primary']),
                    tickfont=dict(size=11, color=COLORS['text_secondary']),
                    gridcolor=COLORS['grid'],
                    gridwidth=0.5,
                    zerolinecolor=COLORS['grid'],
                    zerolinewidth=1
                )
                
                fig2.update_yaxes(
                    title_font=dict(size=14, color=COLORS['text_primary']),
                    tickfont=dict(size=11, color=COLORS['text_secondary']),
                    gridcolor=COLORS['grid'],
                    gridwidth=0.5,
                    zerolinecolor=COLORS['grid'],
                    zerolinewidth=1
                )
                
                # Update bars with premium styling
                fig2.update_traces(
                    marker=dict(
                        line=dict(color=COLORS['background'], width=1),
                        opacity=0.85
                    ),
                    hovertemplate='<b>%{x}</b><br>' +
                                 'Average Expense: $%{y:,.2f}<extra></extra>',
                    hoverlabel=dict(
                        bgcolor=COLORS['surface'],
                        bordercolor=COLORS['accent2'],
                        font=dict(color=COLORS['text_primary'], size=12)
                    )
                )
                
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        except Exception as e:
            self.error_handler.display_error("Payment Analysis Error", str(e))
    
    def _render_payment_analysis(self):
        """Render payment analysis section"""
        st.markdown("### Payment Analysis")
        
        try:
            expenses = self.data['expenses']
            payment_pie = self.viz.create_payment_pie_chart(expenses)
            st.plotly_chart(payment_pie, use_container_width=True, config={'displayModeBar': False})
        
        except Exception as e:
            self.error_handler.display_error("Payment Analysis Error", str(e))

class ScenarioAnalysisTab(BaseTab):
    """Scenario analysis tab for what-if analysis"""
    
    def __init__(self, scenario_analyzer, viz):
        """Initialize scenario analysis tab"""
        super().__init__()
        self.scenario_analyzer = scenario_analyzer
        self.viz = viz
    
    def render(self):
        """Render scenario analysis tab content"""
        self._render_section_header("Scenario Analysis", 'Explore "what-if" scenarios to optimize your financial planning')
        
        # Preset scenarios
        self._render_preset_scenarios()
        
        # Custom scenarios
        self._render_custom_scenarios()
    
    def _render_preset_scenarios(self):
        """Render preset scenarios section"""
        st.markdown("### Preset Scenarios")
        
        if st.button("Run Preset Scenarios", type="primary"):
            with st.spinner("Running scenario analysis..."):
                try:
                    # Performance optimization: Use caching for scenario generation
                    @st.cache_data(ttl=300)  # Cache for 5 minutes
                    def generate_scenarios():
                        return self.scenario_analyzer.run_preset_scenarios()
                    
                    # Performance optimization: Use caching for comparison data
                    @st.cache_data(ttl=300)
                    def generate_comparison(scenarios):
                        return self.scenario_analyzer.compare_scenarios()
                    
                    # Performance optimization: Use caching for charts
                    @st.cache_data(ttl=300)
                    def generate_charts(scenarios):
                        return self.scenario_analyzer.create_scenario_chart()
                    
                    # Generate scenarios with performance monitoring
                    start_time = time.time()
                    scenarios = generate_scenarios()
                    scenario_time = time.time() - start_time
                    
                    st.success(f"Generated {len(scenarios)} scenarios in {scenario_time:.2f}s")
                    
                    # Display scenario comparison with optimized dataframe
                    comparison_df = generate_comparison(scenarios)
                    
                    # Performance optimization: Use st.dataframe with optimized settings
                    st.dataframe(
                        comparison_df, 
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Total Expenses": st.column_config.NumberColumn(
                                "Total Expenses ($)",
                                format="$%.0f"
                            ),
                            "Total Income": st.column_config.NumberColumn(
                                "Total Income ($)",
                                format="$%.0f"
                            ),
                            "Net Amount": st.column_config.NumberColumn(
                                "Net Amount ($)",
                                format="$%.0f"
                            ),
                            "Expense Change (%)": st.column_config.NumberColumn(
                                "Expense Change (%)",
                                format="%.1f%%"
                            ),
                            "Income Change (%)": st.column_config.NumberColumn(
                                "Income Change (%)",
                                format="%.1f%%"
                            ),
                            "Net Change (%)": st.column_config.NumberColumn(
                                "Net Change (%)",
                                format="%.1f%%"
                            )
                        }
                    )
                    
                    # Create scenario charts with performance monitoring
                    chart_start_time = time.time()
                    scenario_charts = generate_charts(scenarios)
                    chart_time = time.time() - chart_start_time
                    
                    # Performance optimization: Use columns with optimized chart rendering
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            scenario_charts['expenses_comparison'], 
                            use_container_width=True,
                            config={'displayModeBar': False}  # Hide plotly toolbar for performance
                        )
                    
                    with col2:
                        st.plotly_chart(
                            scenario_charts['net_comparison'], 
                            use_container_width=True,
                            config={'displayModeBar': False}
                        )
                    
                    # Performance summary
                    total_time = time.time() - start_time
                    st.info(f"**Performance Summary:** Scenarios: {scenario_time:.2f}s | Charts: {chart_time:.2f}s | Total: {total_time:.2f}s")
                
                except Exception as e:
                    self.error_handler.display_error("Scenario Analysis Error", str(e))
    
    def _render_custom_scenarios(self):
        """Render custom scenarios section"""
        st.markdown("### Custom Scenario")
        
        try:
            available_categories = self.scenario_analyzer.get_available_categories()
            
            if available_categories:
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_category = st.selectbox(
                        "Select category to adjust:", 
                        available_categories
                    )
                
                with col2:
                    adjustment_percentage = st.slider(
                        "Adjustment percentage:", 
                        min_value=-50, 
                        max_value=100, 
                        value=0,
                        help="Negative values reduce expenses, positive values increase them"
                    )
                
                if st.button("Run Custom Scenario", type="primary"):
                    with st.spinner("Calculating scenario..."):
                        try:
                            # Performance optimization: Use caching for custom scenario
                            @st.cache_data(ttl=300)
                            def create_custom_scenario(name, adj, salary_adj=0.0):
                                return self.scenario_analyzer.create_custom_scenario(name, adj, salary_adj)
                            
                            # Create adjustments dictionary
                            adjustments = {selected_category: adjustment_percentage / 100}
                            scenario_name = f"{selected_category} {'Increase' if adjustment_percentage > 0 else 'Decrease'} ({abs(adjustment_percentage)}%)"
                            
                            # Performance monitoring
                            start_time = time.time()
                            custom_scenario = create_custom_scenario(scenario_name, adjustments)
                            calculation_time = time.time() - start_time
                            
                            st.success(f"Custom scenario calculated in {calculation_time:.3f}s!")
                            
                            # Performance optimization: Use optimized metric display
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric(
                                    "Total Expenses",
                                    format_currency(custom_scenario['metrics']['total_expenses']),
                                    delta=f"{custom_scenario['changes']['total_expenses']:.1f}%",
                                    delta_color="inverse" if custom_scenario['changes']['total_expenses'] > 0 else "normal"
                                )
                            
                            with col2:
                                st.metric(
                                    "Total Income",
                                    format_currency(custom_scenario['metrics']['total_income']),
                                    delta=f"{custom_scenario['changes']['total_income']:.1f}%",
                                    delta_color="normal" if custom_scenario['changes']['total_income'] > 0 else "inverse"
                                )
                            
                            with col3:
                                st.metric(
                                    "Net Amount",
                                    format_currency(custom_scenario['metrics']['net_amount']),
                                    delta=f"{custom_scenario['changes']['net_amount']:.1f}%",
                                    delta_color="normal" if custom_scenario['metrics']['net_amount'] >= 0 else "inverse"
                                )
                            
                            # Performance optimization: Use compact info display
                            st.markdown("#### Scenario Details")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(f"**Scenario:** {scenario_name}")
                                st.info(f"**Category Adjusted:** {selected_category}")
                            with col2:
                                st.info(f"**Adjustment:** {adjustment_percentage:+.1f}%")
                                st.info(f"**Calculation Time:** {calculation_time:.3f}s")
                            
                        except Exception as e:
                            st.error(f"Error creating custom scenario: {str(e)}")
            else:
                st.warning("No baseline data available. Please run preset scenarios first.")
        
        except Exception as e:
            self.error_handler.display_error("Custom Scenario Error", str(e))

class ROIAnalysisTab(BaseTab):
    """ROI analysis tab for investment return analysis"""
    
    def __init__(self, processor, data, viz):
        """Initialize ROI analysis tab"""
        super().__init__()
        self.processor = processor
        self.data = data
        self.viz = viz
    
    def render(self):
        """Render ROI analysis tab content"""
        st.markdown("## ROI Analysis")
        
        try:
            # Calculate ROI metrics
            roi_analysis = self.processor.get_roi_analysis()
            
            # Display key metrics
            self._render_roi_metrics(roi_analysis)
            
            # ROI chart
            self._render_roi_chart(roi_analysis)
            
            # City comparisons
            self._render_city_comparisons()
            
            # Additional insights
            self._render_roi_insights()
        
        except Exception as e:
            self.error_handler.display_error("ROI Analysis Error", str(e))
    
    def _render_roi_metrics(self, roi_analysis):
        """Render ROI metrics"""
        st.markdown("### Investment Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Degree Cost",
                format_currency(roi_analysis['total_degree_cost'])
            )
        
        with col2:
            if 'salary_ranges' in roi_analysis:
                realistic_salary = roi_analysis['salary_ranges']['realistic']
                st.metric(
                    "Target Annual Salary",
                    format_currency(realistic_salary),
                    help="Median salary from industry dataset"
                )
            else:
                st.metric(
                    "Target Annual Salary",
                    format_currency(roi_analysis['actual_annual_salary']),
                    help="Current salary (for reference only)"
                )
        
        with col3:
            if 'realistic' in roi_analysis['scenarios']:
                realistic = roi_analysis['scenarios']['realistic']
                st.metric(
                    "Realistic Break-even",
                    f"{realistic['break_even_years']:.1f} years"
                )
            else:
                st.metric("Break-even Time", "N/A")
    
    def _render_roi_chart(self, roi_analysis):
        """Render ROI charts"""
        st.markdown("### ROI Analysis Dashboard")
        
        st.info("""
        **Analysis Context:** This ROI analysis uses real industry salary data from your dataset. 
        The break-even timeline accounts for job search periods and realistic savings rates.
        """)
        
        # Create two columns for individual charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Degree Cost vs Salaries chart
            degree_chart = self.viz.create_roi_analysis_chart(roi_analysis)
            st.plotly_chart(degree_chart, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Break-even Timeline chart
            timeline_chart = self.viz.create_break_even_timeline_chart(roi_analysis)
            st.plotly_chart(timeline_chart, use_container_width=True, config={'displayModeBar': False})
    
    def _render_city_comparisons(self):
        """Render city comparison charts"""
        st.markdown("### City Comparisons")
        
        # Top chart: Annual Salary by Role and City
        st.markdown("#### Annual Salary by Role and City")
        salary_chart = self.viz.create_salary_comparison_chart(self.data['salary_data'])
        st.plotly_chart(salary_chart, use_container_width=True, config={'displayModeBar': False})
        
        # Bottom chart: Monthly Cost Comparison by City and Category
        st.markdown("#### Monthly Cost Comparison by City and Category")
        cost_chart = self.viz.create_city_comparison_chart(self.data['city_costs'])
        st.plotly_chart(cost_chart, use_container_width=True, config={'displayModeBar': False})
    
    def _render_roi_insights(self):
        """Render ROI insights"""
        st.markdown("### Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Investment Considerations")
            st.markdown("""
            - **Job Search Time**: Account for 1-6 months of job searching
            - **Entry-level Salaries**: Start with realistic expectations
            - **Savings Rate**: Consider living expenses and taxes
            - **Career Growth**: Salaries typically increase with experience
            """)
        
        with col2:
            st.markdown("#### Success Factors")
            st.markdown("""
            - **Networking**: Build professional connections during studies
            - **Skills Development**: Focus on in-demand technical skills
            - **Location Strategy**: Consider cost of living vs. salary
            - **Financial Planning**: Budget for job search period
            """)

class StoryTab(BaseTab):
    """Story tab for narrative-driven insights"""
    
    def __init__(self, viz, data):
        """Initialize story tab"""
        super().__init__()
        self.viz = viz
        self.data = data
    
    def render(self):
        """Render story tab content"""
        st.markdown("## Harsh's Journey")
        st.markdown("*An interactive exploration of academic and financial growth*")
        
        # Interactive story navigation
        st.markdown("### Story Navigation")
        story_sections = ["Personal Profile", "Financial Journey", "Timeline"]
        selected_section = st.selectbox("Choose your story path:", story_sections, index=0)
        
        # Dynamic content based on selection
        if selected_section == "Personal Profile":
            self._render_personal_profile()
        elif selected_section == "Financial Journey":
            self._render_financial_journey()
        elif selected_section == "Timeline":
            self._render_interactive_timeline()
    
    def _render_personal_profile(self):
        """Render personal profile section"""
        st.markdown("### Meet Harsh - Interactive Profile")
        
        # Academic background
        with st.expander("Academic Background", expanded=True):
            self._render_academic_background()
        
        # Personal background
        with st.expander("Personal Background", expanded=True):
            self._render_personal_background()
        
        # Career aspirations
        with st.expander("Career Aspirations"):
            self._render_career_aspirations()
    
    def _render_academic_background(self):
        """Render academic background section"""
        from config.settings import PERSONA
        
        # Academic information in a clean card layout with premium styling
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%); 
                    padding: {SPACING['6']}; border-radius: {BORDER_RADIUS['lg']}; margin-bottom: {SPACING['4']}; 
                    border: 1px solid {COLORS['border']}; box-shadow: {SHADOWS['lg']};">
            <h4 style="margin-bottom: {SPACING['4']}; color: {COLORS['primary']}; font-weight: {FONT_WEIGHTS['semibold']};">Academic Information</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: {SPACING['4']}; color: {COLORS['text_secondary']};">
                <div>
                    <p><strong style="color: {COLORS['text_primary']};">Program:</strong> {PERSONA['program']}</p>
                    <p><strong style="color: {COLORS['text_primary']};">University:</strong> {PERSONA['university']}</p>
                </div>
                <div>
                    <p><strong style="color: {COLORS['text_primary']};">Expected Graduation:</strong> {PERSONA['graduation_year']}</p>
                    <p><strong style="color: {COLORS['text_primary']};">Current Status:</strong> <span style="color: {COLORS['success']};">Former/Alumni Student</span></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Academic progress visualization
        st.markdown("#### Academic Performance")
        
        academic_data = {
            'Semester': ['Fall 2023', 'Spring 2024', 'Fall 2024', 'Spring 2025'],
            'Credits': [9, 9, 11, 10],
            'GPA': [3.66, 3.66, 4.0, 4.0]
        }
        
        # Display as metrics with consistent styling
        cols = st.columns(4)
        for i, (semester, credits, gpa) in enumerate(zip(academic_data['Semester'], academic_data['Credits'], academic_data['GPA'])):
            with cols[i]:
                st.metric(semester, f"{gpa:.2f}", f"{credits} Credits", delta_color="off")
    
    def _render_personal_background(self):
        """Render personal background section"""
        from config.settings import PERSONA
        
        # Personal information in a clean card layout with premium styling
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%); 
                    padding: {SPACING['6']}; border-radius: {BORDER_RADIUS['lg']}; margin-bottom: {SPACING['4']}; 
                    border: 1px solid {COLORS['border']}; box-shadow: {SHADOWS['lg']};">
            <h4 style="margin-bottom: {SPACING['4']}; color: {COLORS['secondary']}; font-weight: {FONT_WEIGHTS['semibold']};">Personal Information</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: {SPACING['4']}; color: {COLORS['text_secondary']};">
                <div>
                    <p><strong style="color: {COLORS['text_primary']};">Hometown:</strong> {PERSONA['hometown']}</p>
                    <p><strong style="color: {COLORS['text_primary']};">Nationality:</strong> Indian</p>
                </div>
                <div>
                    <p><strong style="color: {COLORS['text_primary']};">Languages:</strong> English, Hindi, Gujarati</p>
                    <p><strong style="color: {COLORS['text_primary']};">Interests:</strong> Technology, Innovation, Global Development</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Skills & confidence visualization
        st.markdown("#### Skills & Confidence")
        
        cultural_data = {
            'Aspect': ['Language Proficiency', 'Cultural Adaptation', 'Academic Excellence', 'Career Readiness'],
            'Confidence': [95, 90, 85, 80]
        }
        
        # Display as progress bars with better styling
        for aspect, confidence in zip(cultural_data['Aspect'], cultural_data['Confidence']):
            st.markdown(f"**{aspect}**")
            if confidence >= 90:
                st.progress(confidence/100, text=f"{confidence}% - Excellent")
            elif confidence >= 80:
                st.progress(confidence/100, text=f"{confidence}% - Good")
            else:
                st.progress(confidence/100, text=f"{confidence}% - Developing")
            st.markdown("---")
    
    def _render_career_aspirations(self):
        """Render career aspirations section"""
        from config.settings import PERSONA
        
        st.markdown(f"**Primary Goal**: {PERSONA['career_goal']}")
        
        # Career path visualization
        career_steps = [
            "Graduate with MS in CS",
            "Secure Entry-level Position",
            "Develop Technical Skills",
            "Advance to Senior Role",
            "Lead Technical Teams"
        ]
        
        for i, step in enumerate(career_steps):
            col1, col2, col3 = st.columns([1, 20, 1])
            with col2:
                if i == 0:
                    st.success(f"{step}")
                elif i == 1:
                    st.info(f"{step}")
                else:
                    st.info(f"{step}")
    
    def _render_financial_journey(self):
        """Render financial journey section"""
        st.markdown("### Financial Journey - Interactive Analysis")
        
        try:
            # Financial health dashboard with better layout
            st.markdown("#### Financial Health Assessment")
            
            # Calculate financial health metrics
            expenses = self.data['expenses']
            income = self.data['salary'] if 'salary' in self.data else pd.DataFrame()
            
            # Financial health calculation
            if not income.empty:
                total_income = income['Amount'].sum()
                total_expenses = expenses['Amount'].sum()
                savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0
                
                # Health score based on multiple factors
                health_score = min(100, max(0, 
                    (savings_rate * 40) +  # Savings rate (40 points)
                    (min(1, total_income / total_expenses) * 30) +  # Income vs expenses (30 points)
                    (min(1, len(expenses) / 24) * 30)  # Data completeness (30 points)
                ))
                
                # Display health score in a prominent card with premium styling
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); 
                            padding: {SPACING['6']}; border-radius: {BORDER_RADIUS['xl']}; margin: {SPACING['4']} 0; color: {COLORS['text_primary']}; text-align: center;
                            box-shadow: {SHADOWS['xl']}; border: 1px solid {COLORS['border']};">
                    <h3 style="margin: 0 0 {SPACING['2']} 0; font-size: {FONT_SIZES['lg']};">Overall Financial Health Score</h3>
                    <h2 style="margin: 0; font-size: {FONT_SIZES['5xl']}; font-weight: {FONT_WEIGHTS['bold']};">{health_score:.1f}/100</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Health indicators with premium styling
                if health_score >= 80:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%); 
                                color: {COLORS['success']}; padding: {SPACING['4']}; border-radius: {BORDER_RADIUS['md']}; 
                                border-left: 4px solid {COLORS['success']}; margin: {SPACING['4']} 0; border: 1px solid {COLORS['border']};
                                box-shadow: {SHADOWS['lg']};">
                        <h4 style="margin: 0; color: {COLORS['text_primary']};">Excellent Financial Health</h4>
                        <p style="margin: {SPACING['2']} 0 0 0; color: {COLORS['text_secondary']};">Your financial management is outstanding!</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif health_score >= 60:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%); 
                                color: {COLORS['success']}; padding: {SPACING['4']}; border-radius: {BORDER_RADIUS['md']}; 
                                border-left: 4px solid {COLORS['success']}; margin: {SPACING['4']} 0; border: 1px solid {COLORS['border']};
                                box-shadow: {SHADOWS['lg']};">
                        <h4 style="margin: 0; color: {COLORS['text_primary']};">Good Financial Health</h4>
                        <p style="margin: {SPACING['2']} 0 0 0; color: {COLORS['text_secondary']};">You're on the right track with your finances.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif health_score >= 40:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%); 
                                color: {COLORS['warning']}; padding: {SPACING['4']}; border-radius: {BORDER_RADIUS['md']}; 
                                border-left: 4px solid {COLORS['warning']}; margin: {SPACING['4']} 0; border: 1px solid {COLORS['border']};
                                box-shadow: {SHADOWS['lg']};">
                        <h4 style="margin: 0; color: {COLORS['text_primary']};">Fair Financial Health</h4>
                        <p style="margin: {SPACING['2']} 0 0 0; color: {COLORS['text_secondary']};">There's room for improvement in your financial planning.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%); 
                                color: {COLORS['error']}; padding: {SPACING['4']}; border-radius: {BORDER_RADIUS['md']}; 
                                border-left: 4px solid {COLORS['error']}; margin: {SPACING['4']} 0; border: 1px solid {COLORS['border']};
                                box-shadow: {SHADOWS['lg']};">
                        <h4 style="margin: 0; color: {COLORS['text_primary']};">Needs Attention</h4>
                        <p style="margin: {SPACING['2']} 0 0 0; color: {COLORS['text_secondary']};">Consider reviewing your spending patterns and budget.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Income data not available for health calculation")
            
            # Spending patterns with better visualization
            st.markdown("#### Spending Patterns Analysis")
            
            # Category spending analysis
            category_totals = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
            
            # Display top categories in a more visually appealing way
            top_categories = category_totals.head(5)
            
            # Create a better spending breakdown display
            st.markdown("**Top 5 Expense Categories**")
            
            # Display categories as progress bars with amounts
            for category, amount in top_categories.items():
                percentage = (amount / top_categories.max()) * 100
                st.markdown(f"**{category}**")
                st.progress(percentage/100, text=f"${amount:,.0f}")
                st.markdown("---")
        
        except Exception as e:
            self.error_handler.display_error("Financial Journey Error", str(e))
    
    def _render_interactive_timeline(self):
        """Render interactive timeline section"""
        st.markdown("### Interactive Academic Journey Timeline")
        
        try:
            from config.settings import TIMELINE_MILESTONES
            
            # Timeline controls
            timeline_filter = st.selectbox(
                "Filter timeline by:",
                ["All Events", "Academic", "Employment", "Personal", "Financial"]
            )
            
            # Filter milestones based on selection
            if timeline_filter == "All Events":
                filtered_milestones = TIMELINE_MILESTONES
            else:
                filtered_milestones = [
                    m for m in TIMELINE_MILESTONES 
                    if m.get('type', '').lower() == timeline_filter.lower()
                ]
            
            # Enhanced timeline chart
            timeline_chart = self.viz.create_timeline_chart(filtered_milestones)
            st.plotly_chart(timeline_chart, use_container_width=True, config={'displayModeBar': False})
        
        except Exception as e:
            self.error_handler.display_error("Timeline Error", str(e)) 