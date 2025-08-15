"""
Enhanced Configuration Settings for Professional Dashboard
Unified design system with consistent spacing, colors, and layouts
"""

import os
from datetime import datetime, timedelta

# =============================================================================
# DESIGN SYSTEM & LAYOUT
# =============================================================================

# Import unified design system
from .design_system import COLORS, FONT_SIZES, FONT_WEIGHTS, SPACING, BORDER_RADIUS, SHADOWS, COMPONENT_SIZES

# Use design system colors and spacing
CHART_COLORS = [
    COLORS['primary'],    # Cyan
    COLORS['secondary'],  # Pink
    COLORS['accent1'],    # Lavender
    COLORS['accent2'],    # Light Blue
    COLORS['accent3'],    # Mint Green
    COLORS['accent4'],    # Amber
    COLORS['info'],       # Blue
    COLORS['success'],    # Green
    COLORS['warning'],    # Orange
    COLORS['error']       # Red
]

# Category-specific colors with semantic meaning
CATEGORY_COLORS = {
    'Rent': COLORS['primary'],           # Housing - Cyan
    'Groceries': COLORS['secondary'],    # Food - Pink
    'Tuition Fees': COLORS['error'],     # Education - Red
    'Mobile Recharge': COLORS['accent1'], # Utilities - Lavender
    'Travel': COLORS['accent3'],         # Transportation - Mint
    'Gas': COLORS['accent4'],            # Fuel - Amber
    'Restaurants': COLORS['accent2'],    # Dining - Light Blue
    'Miscellaneous': COLORS['info'],     # Other - Blue
    'Shopping': COLORS['secondary'],     # Retail - Pink
    'Car Insurance': COLORS['success'],  # Insurance - Green
    'Car Rental': COLORS['accent2'],     # Rental - Light Blue
    'DPS': COLORS['warning'],            # Government - Orange
    'Driving School': COLORS['secondary'], # Education - Pink
    'Flight': COLORS['accent1'],         # Travel - Purple
    'HP Laptop/Related': COLORS['primary'], # Technology - Cyan
    'Deposit': COLORS['success']         # Financial - Green
}

# Color-blind safe palette for accessibility
ACCESSIBLE_COLORS = CHART_COLORS

# =============================================================================
# DASHBOARD LAYOUT & COMPONENTS
# =============================================================================

# Page configuration with premium settings
PAGE_CONFIG = {
    'page_title': 'International Student Financial Dashboard',
    'page_icon': '',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'menu_items': {
        'Get Help': 'https://github.com/your-repo/issues',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': '# International Student Financial Dashboard\nProfessional financial analysis and planning tool.'
    }
}

# Layout grid system
GRID_CONFIG = {
    'columns': 12,           # 12-column grid system
    'gutter': '1rem',        # Column spacing
    'margin': '1rem',        # Page margins
    'padding': '1rem',       # Content padding
}

# Component sizing (using design system)
# COMPONENT_SIZES is imported from design_system.py

# Chart templates and configurations
CHART_TEMPLATES = {
    'premium': 'plotly_dark',
    'minimal': 'plotly_white',
    'dark': 'plotly_dark'
}

# Chart layout configurations
CHART_LAYOUT = {
    'background_color': COLORS['background'],
    'paper_bgcolor': COLORS['background'],
    'plot_bgcolor': COLORS['surface'],
    'font_color': COLORS['text_primary'],
    'title_font_color': COLORS['text_primary'],
    'legend_font_color': COLORS['text_secondary'],
    'xaxis_color': COLORS['text_secondary'],
    'yaxis_color': COLORS['text_secondary'],
    'grid_color': COLORS['grid'],
    'border_color': COLORS['border']
}

# Typography system (using design system)
TYPOGRAPHY = {
    'font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    'title_size': '1.5rem',
    'subtitle_size': '1.25rem',
    'body_size': '1rem',
    'caption_size': '0.875rem',
    'font_weight_light': 300,
    'font_weight_normal': 400,
    'font_weight_medium': 500,
    'font_weight_semibold': 600,
    'font_weight_bold': 700
}

# =============================================================================
# DATA CONFIGURATION
# =============================================================================

# File paths
DATA_PATHS = {
    'expenses': 'data/cost_of_living.csv',
    'salary': 'data/salary.csv',  # Time-series salary data
    'city_costs': 'data/city_costs.csv',
    'salary_data': 'data/salary_data.csv'  # Role-based salary data
}

# Date range for analysis
DEFAULT_DATE_RANGE = 24  # Months to analyze

# =============================================================================
# ANALYTICAL CONSTANTS
# =============================================================================

# Financial analysis parameters
FINANCIAL_PARAMS = {
    'inflation_rate': 0.03,      # 3% annual inflation
    'roi_break_even_years': 5,   # Expected break-even time
    'savings_rate': 0.25,        # Default savings rate
    'emergency_fund_months': 6,  # Emergency fund target
    'debt_to_income_ratio': 0.43, # Maximum DTI ratio
}

# Anomaly detection parameters
ANOMALY_PARAMS = {
    'threshold': 2.0,            # Standard deviations for anomaly detection
    'min_amount': 100,           # Minimum amount to flag
    'rolling_window': 3,         # Rolling window for trend analysis
}

# =============================================================================
# SCENARIO ANALYSIS PARAMETERS
# =============================================================================

# Scenario analysis parameters
SCENARIO_ADJUSTMENTS = {
    'optimistic': {
        'rent': -0.10,
        'groceries': -0.15,
        'transportation': -0.20,
        'utilities': -0.05,
        'salary': 0.20
    },
    'pessimistic': {
        'rent': 0.15,
        'groceries': 0.10,
        'transportation': 0.25,
        'utilities': 0.20,
        'salary': -0.10
    },
    'realistic': {
        'rent': 0.05,
        'groceries': 0.03,
        'transportation': 0.08,
        'utilities': 0.05,
        'salary': 0.05
    }
}

# =============================================================================
# CITY & ROLE DATA
# =============================================================================

# Major US cities for comparison
CITIES = [
    'College Station', 'Austin', 'Houston', 'Dallas', 'San Antonio',
    'New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Seattle',
    'Boston', 'Washington DC', 'Atlanta', 'Denver', 'Phoenix'
]

# CS-related roles for salary comparison
CS_ROLES = [
    'Software Engineer', 'Data Scientist', 'Machine Learning Engineer',
    'AI Researcher', 'DevOps Engineer', 'Product Manager',
    'Data Analyst', 'Frontend Developer', 'Backend Developer'
]

# =============================================================================
# EXPORT SETTINGS
# =============================================================================

# PDF export settings
PDF_CONFIG = {
    'page_size': 'A4',
    'margin': 20,
    'title': 'International Student Financial Analysis Report',
    'author': 'Professional Financial Dashboard',
    'subject': 'Financial Planning and Analysis',
    'keywords': 'finance, education, international student, planning'
}

# Excel export settings
EXCEL_CONFIG = {
    'sheet_names': ['Executive Summary', 'Monthly Analysis', 'Forecasts', 'Scenarios', 'Insights'],
    'include_charts': True,
    'chart_format': 'png'
}

# =============================================================================
# ENVIRONMENT VARIABLES
# =============================================================================

def load_env_vars():
    """Load environment variables for API keys and configuration"""
    return {
        'google_maps_api_key': os.getenv('GOOGLE_MAPS_API_KEY'),
        'numeo_api_key': os.getenv('NUMBEO_API_KEY'),
        'database_url': os.getenv('DATABASE_URL'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'plotly_api_key': os.getenv('PLOTLY_API_KEY')
    }

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_date_range(start_date, end_date):
    """Validate date range for analysis"""
    if start_date >= end_date:
        raise ValueError("Start date must be before end date")
    
    if end_date > datetime.now():
        raise ValueError("End date cannot be in the future")
    
    return True

def validate_amount(amount):
    """Validate monetary amounts"""
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be numeric")
    
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    
    return True

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def format_currency(amount):
    """Format amount as currency with professional styling"""
    if amount >= 1_000_000:
        return f"${amount/1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.1f}K"
    else:
        return f"${amount:,.2f}"

def format_percentage(value):
    """Format value as percentage with professional styling"""
    return f"{value:.1%}"

def format_number(value, decimals=2):
    """Format number with consistent decimal places"""
    return f"{value:,.{decimals}f}"

def get_month_name(month_number):
    """Get month name from number"""
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    return months[month_number - 1]

# =============================================================================
# STORYTELLING ELEMENTS
# =============================================================================

# Persona information
PERSONA = {
    'name': 'Harsh',
    'program': 'Master of Computer Science',
    'university': 'Texas A&M University',
    'graduation_year': 2025,
    'hometown': 'Ahmedabad, India',
    'career_goal': 'Software Engineer at a tech company',
    'background': 'International student with strong technical skills',
    'interests': ['Technology', 'Innovation', 'Global Development', 'AI/ML']
}

# Timeline milestones with enhanced metadata
TIMELINE_MILESTONES = [
    {
        'date': '2023-08-01', 
        'event': 'Arrived in College Station', 
        'type': 'arrival',
        'impact': 'Major life transition',
        'financial_implication': 'Initial setup costs'
    },
    {
        'date': '2023-08-21', 
        'event': 'Started Fall Semester', 
        'type': 'academic',
        'impact': 'Academic journey begins',
        'financial_implication': 'Tuition and course materials'
    },
    {
        'date': '2023-08-31', 
        'event': 'Started Part-Time Job', 
        'type': 'employment',
        'impact': 'Income generation begins',
        'financial_implication': 'Regular income stream'
    },
    {
        'date': '2024-01-15', 
        'event': 'Started Spring Semester', 
        'type': 'academic',
        'impact': 'Continued academic progress',
        'financial_implication': 'Semester expenses'
    },
    {
        'date': '2024-01-16', 
        'event': 'Started Graduate Teaching Assistantship', 
        'type': 'employment',
        'impact': 'Enhanced income and experience',
        'financial_implication': 'Increased income, tuition benefits'
    },
    {
        'date': '2024-08-19', 
        'event': 'Started Fall Semester', 
        'type': 'academic',
        'impact': 'Advanced coursework',
        'financial_implication': 'Higher-level course costs'
    },
    {
        'date': '2025-01-13', 
        'event': 'Started Final Semester', 
        'type': 'academic',
        'impact': 'Capstone and graduation preparation',
        'financial_implication': 'Final semester expenses'
    },
    {
        'date': '2025-05-10', 
        'event': 'Graduation', 
        'type': 'academic',
        'impact': 'Degree completion',
        'financial_implication': 'Graduation costs, job search'
    }
] 