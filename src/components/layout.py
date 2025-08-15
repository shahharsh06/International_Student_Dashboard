"""
Dashboard Layout Component
Premium design system with deep navy background and pastel neon accents
"""

import streamlit as st
from typing import Optional

class DashboardLayout:
    """Premium dashboard layout with modern design system"""
    
    def __init__(self):
        """Initialize the layout component"""
        from config.settings import COLORS, SPACING
        self.colors = COLORS
        self.spacing = SPACING
    
    def apply_design_system(self):
        """Apply premium design system to the dashboard"""
        st.markdown(self._get_css_styles(), unsafe_allow_html=True)
    
    def render_header(self, title: str, subtitle: Optional[str] = None):
        """Render premium dashboard header with gradient background"""
        if subtitle:
            header_html = f"""
            <div class="dashboard-header">
                <div class="header-content">
                    <h1 class="main-title">{title}</h1>
                    <p class="subtitle">{subtitle}</p>
                </div>
            </div>
            """
        else:
            header_html = f"""
            <div class="dashboard-header">
                <div class="header-content">
                    <h1 class="main-title">{title}</h1>
                </div>
            </div>
            """
        
        st.markdown(header_html, unsafe_allow_html=True)
    
    def render_metric_card(self, title: str, value: str, delta: Optional[str] = None, 
                          delta_color: str = "normal", help_text: Optional[str] = None):
        """Render premium metric card with neon accents"""
        # Build HTML components separately to avoid f-string issues
        delta_section = f'<div class="metric-delta {delta_color}">{delta}</div>' if delta else ''
        help_section = f'<div class="metric-help">{help_text}</div>' if help_text else ''
        
        metric_html = f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3 class="metric-title">{title}</h3>
                <div class="metric-value">{value}</div>
                {delta_section}
                {help_section}
            </div>
        </div>
        """
        
        st.markdown(metric_html, unsafe_allow_html=True)
    
    def render_info_card(self, title: str, content: str, card_type: str = "info"):
        """Render information card with premium styling"""
        icon_map = {
            "info": "ℹ",
            "success": "✓", 
            "warning": "⚠",
            "error": "✗"
        }
        
        icon = icon_map.get(card_type, "ℹ")
        css_class = f"info-card {card_type}"
        
        info_html = f"""
        <div class="{css_class}">
            <div class="info-header">
                <span class="info-icon">{icon}</span>
                <h4 class="info-title">{title}</h4>
            </div>
            <div class="info-content">{content}</div>
        </div>
        """
        
        st.markdown(info_html, unsafe_allow_html=True)
    
    def render_section_header(self, title: str, icon: str = "", level: int = 2):
        """Render consistent section headers with premium styling"""
        header_tag = f"h{level}"
        icon_html = f"{icon} " if icon else ""
        
        section_html = f"""
        <{header_tag} class="section-header">
            {icon_html}{title}
        </{header_tag}>
        """
        
        st.markdown(section_html, unsafe_allow_html=True)
    
    def _get_css_styles(self) -> str:
        """Get premium CSS styles with deep navy theme and neon accents"""
        return """
        <style>
        /* ===== PREMIUM DESIGN SYSTEM ===== */
        
        /* Import Inter font for premium typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* CSS Custom Properties for premium theme */
        :root {
            --background: #0a0e1a;
            --surface: #1a1f2e;
            --primary: #00d4ff;
            --secondary: #ff6b9d;
            --accent1: #b8a9ff;
            --accent2: #7dd3fc;
            --accent3: #86efac;
            --accent4: #fbbf24;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --text-primary: #ffffff;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border: #334155;
            --grid: #1e293b;
            --hover: #2d3748;
            
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 20px rgba(0, 212, 255, 0.3);
            
            --radius-sm: 0.5rem;
            --radius-md: 0.75rem;
            --radius-lg: 1rem;
            --radius-xl: 1.5rem;
            
            /* Typography System */
            --title-size: 3rem;
            --subtitle-size: 1.25rem;
            --body-size: 1rem;
            --caption-size: 0.875rem;
            --font-weight-light: 300;
            --font-weight-normal: 400;
            --font-weight-medium: 500;
            --font-weight-semibold: 600;
            --font-weight-bold: 700;
        }
        
        /* Global styles */
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--background);
            color: var(--text-primary);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }
        
        /* Premium Dashboard Header */
        .dashboard-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            margin-bottom: 2rem;
            padding: 2.5rem 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }
        
        .dashboard-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, 
                rgba(0, 212, 255, 0.05) 0%, 
                rgba(255, 107, 157, 0.05) 50%, 
                rgba(184, 169, 255, 0.05) 100%);
            pointer-events: none;
        }
        
        .header-content {
            position: relative;
            z-index: 2;
            text-align: center;
        }
        
        .main-title {
            font-size: var(--title-size, 2.5rem);
            font-weight: var(--font-weight-bold, 700);
            margin: 0 0 1rem 0;
            color: var(--text-primary);
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            letter-spacing: 0.5px;
            line-height: 1.2;
        }
        
        .subtitle {
            font-size: var(--subtitle-size, 1.2rem);
            margin: 0;
            color: var(--text-secondary);
            font-weight: var(--font-weight-medium, 500);
            opacity: 1;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.25px;
        }
        
        /* Premium Section Headers */
        .section-header {
            color: var(--text-primary);
            font-size: var(--title-size, 1.5rem);
            font-weight: var(--font-weight-semibold, 600);
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--border);
            position: relative;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 1px;
        }
        
        /* Premium Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, var(--surface) 0%, rgba(26, 31, 46, 0.8) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            margin: 1rem 0;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            border-color: var(--primary);
        }
        
        .metric-title {
            font-size: var(--caption-size, 0.875rem);
            color: var(--text-muted);
            margin: 0 0 0.75rem 0;
            font-weight: var(--font-weight-medium, 500);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            font-size: 2.25rem;
            font-weight: var(--font-weight-bold, 700);
            color: var(--text-primary);
            margin: 0;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-delta {
            font-size: 0.875rem;
            margin-top: 0.75rem;
            padding: 0.375rem 0.75rem;
            border-radius: var(--radius-sm);
            display: inline-block;
            font-weight: 500;
        }
        
        .metric-delta.normal {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        .metric-delta.inverse {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
            color: var(--error);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        .metric-help {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.75rem;
            font-style: italic;
        }
        
        /* Premium Info Cards */
        .info-card {
            background: linear-gradient(135deg, var(--surface) 0%, rgba(26, 31, 46, 0.8) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin: 1rem 0;
            padding: 1.25rem;
            position: relative;
            overflow: hidden;
        }
        
        .info-card.info {
            border-left: 4px solid var(--primary);
        }
        
        .info-card.success {
            border-left: 4px solid var(--success);
        }
        
        .info-card.warning {
            border-left: 4px solid var(--warning);
        }
        
        .info-card.error {
            border-left: 4px solid var(--error);
        }
        
        .info-header {
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
        }
        
        .info-icon {
            font-size: 1.25rem;
            margin-right: 0.75rem;
        }
        
        .info-title {
            margin: 0;
            font-weight: 600;
            font-size: 1.125rem;
            color: var(--text-primary);
        }
        
        .info-content {
            margin: 0;
            line-height: 1.6;
            color: var(--text-secondary);
        }
        
        /* Premium Tab Styling - Deep Navy Theme */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.75rem;
            background: var(--surface);
            padding: 1rem;
            border-radius: var(--radius-lg);
            border: 1px solid var(--border);
            box-shadow: var(--shadow-md);
            margin: 1rem 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 3.5rem;
            white-space: nowrap;
            background: var(--surface);
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--text-secondary);
            font-weight: 500;
            font-family: 'Inter, sans-serif';
            padding: 0 1.5rem;
            position: relative;
            overflow: hidden;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: var(--hover);
            color: var(--text-primary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm);
            border-color: var(--primary);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--text-primary);
            border-color: var(--primary);
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
            position: relative;
        }
        
        .stTabs [aria-selected="true"]::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 2px;
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }
        
        /* Tab content styling */
        .stTabs [data-baseweb="tab-panel"] {
            background: var(--surface);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            margin-top: 1rem;
            border: 1px solid var(--border);
        }
        
        /* Tab icon and text styling */
        .stTabs [data-baseweb="tab"] svg {
            width: 20px;
            height: 20px;
            margin-right: 0.5rem;
            vertical-align: middle;
        }
        
        .stTabs [aria-selected="true"] svg {
            filter: brightness(0) invert(1);
        }
        
        /* Tab container enhancements */
        .stTabs {
            margin: 2rem 0;
        }
        
        /* Responsive tab adjustments */
        @media (max-width: 768px) {
            .stTabs [data-baseweb="tab-list"] {
                padding: 0.75rem;
                gap: 0.5rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 3rem;
                padding: 0 1rem;
                font-size: 0.875rem;
            }
        }
        
        /* Premium Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--text-primary);
            border: none;
            border-radius: var(--radius-md);
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md), var(--shadow-glow);
        }
        
        /* Premium Data Tables */
        .dataframe {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            color: var(--text-primary);
        }
        
        .stDataFrame {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
        }
        
        /* Premium Chart Containers */
        [data-testid="stPlotlyChart"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1rem;
            box-shadow: var(--shadow-sm);
        }
        
        /* Premium Metric Containers */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, var(--surface) 0%, rgba(26, 31, 46, 0.8) 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1rem;
            box-shadow: var(--shadow-sm);
        }
        
        /* Premium Input Styling */
        .stTextInput > div > div > input {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
        }
        
        /* Premium Selectbox Styling */
        .stSelectbox > div > div > div {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
        }
        
        .stSelectbox > div > div > div:focus-within {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
        }
        
        /* Premium Slider Styling */
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        /* Premium Progress Bar Styling */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        /* Premium Success/Error/Warning Messages */
        .stSuccess {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: var(--radius-md);
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
            color: var(--error);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: var(--radius-md);
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: var(--radius-md);
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Premium Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--surface);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
        }
        
        /* Premium Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .metric-card, .info-card {
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* Premium Hover Effects */
        .metric-card:hover::before {
            background: linear-gradient(90deg, var(--secondary) 0%, var(--primary) 100%);
        }
        
        /* Premium Focus States */
        .stButton > button:focus,
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus-within {
            outline: none;
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2);
        }
        </style>
        """ 