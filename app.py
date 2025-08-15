"""
International Student Financial Dashboard
Professional-grade financial analysis and planning tool with unified design system
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os
import warnings
import tracemalloc

# Enable tracemalloc to fix RuntimeWarning
tracemalloc.start()

# Suppress FutureWarning for pandas datetime operations
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')
warnings.filterwarnings('ignore', category=FutureWarning, module='_plotly_utils')
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import core modules
from src.data_processor import DataProcessor
from src.visualizations import DashboardVisualizations
from src.scenario_analysis import ScenarioAnalyzer
from src.components import (
    DashboardLayout, OverviewTab, ExpensesTab, ScenarioAnalysisTab, 
    ROIAnalysisTab, StoryTab
)
from src.utils import ErrorHandler, CacheManager
from config.settings import (
    PAGE_CONFIG, PERSONA, TIMELINE_MILESTONES,
    format_currency, format_percentage
)
from config.design_system import COLORS

# Initialize Streamlit configuration
st.set_page_config(**PAGE_CONFIG)

# Add unified design system CSS
from config.design_system import get_css_utilities
st.markdown(get_css_utilities(), unsafe_allow_html=True)

# Initialize core services
@st.cache_resource
def initialize_services():
    """Initialize and cache core dashboard services"""
    try:
        layout = DashboardLayout()
        error_handler = ErrorHandler()
        cache_manager = CacheManager()
        
        return layout, error_handler, cache_manager
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        return None, None, None

@st.cache_data
def load_dashboard_data():
    """Load and cache dashboard data with error handling"""
    try:
        processor = DataProcessor()
        data = processor.load_data()
        processor.clean_data()
        return processor, data
    except Exception as e:
        raise Exception(f"Data loading failed: {str(e)}")

def main():
    """Main dashboard application with professional architecture"""
    
    # Initialize services
    layout, error_handler, cache_manager = initialize_services()
    if not all([layout, error_handler, cache_manager]):
        st.error("Dashboard initialization failed. Please refresh the page.")
        return
    
    try:
        # Apply unified design system
        layout.apply_design_system()
        
        # Header with professional styling
        layout.render_header("International Student Financial Dashboard")
        
        # Load data with proper error handling
        try:
            processor, data = load_dashboard_data()
        except Exception as e:
            error_handler.display_error("Data Loading Error", str(e))
            return
        
        # Initialize analysis modules
        viz = DashboardVisualizations()
        scenario_analyzer = ScenarioAnalyzer()
        scenario_analyzer.set_baseline_data(data['expenses'], data['salary'])
        
        # Main dashboard layout
        tab_names = ["Overview", "Expenses", "Scenario Analysis", "ROI Analysis", "Story"]
        tabs = st.tabs(tab_names)
        
        # Tab content with proper error handling
        with tabs[0]:
            OverviewTab(processor, data, viz).render()
        
        with tabs[1]:
            ExpensesTab(processor, data, viz).render()
        
        with tabs[2]:
            ScenarioAnalysisTab(scenario_analyzer, viz).render()
        
        with tabs[3]:
            ROIAnalysisTab(processor, data, viz).render()
        
        with tabs[4]:
            StoryTab(viz, data).render()
            
    except Exception as e:
        error_handler.display_error("Dashboard Error", str(e))
        st.info("Please refresh the page or check your data files.")

if __name__ == "__main__":
    main() 