"""
Unified Design System Configuration
Professional dashboard design system with consistent typography, spacing, colors, and components
"""

# =============================================================================
# COLOR SYSTEM
# =============================================================================

# Primary Color Palette
COLORS = {
    # Core Colors
    'primary': '#00d4ff',           # Bright Blue - Primary actions
    'secondary': '#ff6b9d',         # Pink - Secondary actions
    'accent1': '#b8a9ff',          # Purple - Accent elements
    'accent2': '#7dd3fc',          # Light Blue - Subtle accents
    'accent3': '#86efac',          # Green - Success states
    'accent4': '#fbbf24',          # Yellow - Warning states
    
    # Semantic Colors
    'success': '#10b981',           # Green - Success messages
    'warning': '#f59e0b',           # Amber - Warning messages
    'error': '#ef4444',             # Red - Error messages
    'info': '#3b82f6',              # Blue - Information
    
    # Background Colors
    'background': '#0a0e1a',        # Dark Navy - Main background
    'surface': '#1a1f2e',           # Dark Gray - Card backgrounds
    'surface_light': '#2d3748',     # Lighter Gray - Hover states
    
    # Text Colors
    'text_primary': '#ffffff',      # White - Primary text
    'text_secondary': '#cbd5e1',    # Light Gray - Secondary text
    'text_muted': '#94a3b8',        # Muted Gray - Tertiary text
    
    # Border and Grid Colors
    'border': '#334155',             # Border color
    'grid': '#1e293b',              # Grid lines
    'hover': '#2d3748',             # Hover state
}

# =============================================================================
# TYPOGRAPHY SYSTEM
# =============================================================================

# Font Family
FONT_FAMILY = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

# Font Sizes (rem-based scale)
FONT_SIZES = {
    'xs': '0.75rem',      # 12px
    'sm': '0.875rem',     # 14px
    'base': '1rem',       # 16px
    'lg': '1.125rem',     # 18px
    'xl': '1.25rem',      # 20px
    '2xl': '1.5rem',      # 24px
    '3xl': '1.875rem',    # 30px
    '4xl': '2.25rem',     # 36px
    '5xl': '3rem',        # 48px
    '6xl': '3.75rem',     # 60px
}

# Font Weights
FONT_WEIGHTS = {
    'light': 300,
    'normal': 400,
    'medium': 500,
    'semibold': 600,
    'bold': 700,
    'extrabold': 800,
}

# Line Heights
LINE_HEIGHTS = {
    'tight': 1.25,
    'normal': 1.5,
    'relaxed': 1.75,
}

# =============================================================================
# SPACING SYSTEM
# =============================================================================

# Spacing Scale (rem-based)
SPACING = {
    '0': '0rem',          # 0px
    '1': '0.25rem',       # 4px
    '2': '0.5rem',        # 8px
    '3': '0.75rem',       # 12px
    '4': '1rem',          # 16px
    '5': '1.25rem',       # 20px
    '6': '1.5rem',        # 24px
    '8': '2rem',          # 32px
    '10': '2.5rem',       # 40px
    '12': '3rem',         # 48px
    '16': '4rem',         # 64px
    '20': '5rem',         # 80px
    '24': '6rem',         # 96px
}

# =============================================================================
# BORDER RADIUS SYSTEM
# =============================================================================

BORDER_RADIUS = {
    'none': '0rem',
    'sm': '0.25rem',      # 4px
    'base': '0.375rem',   # 6px
    'md': '0.5rem',       # 8px
    'lg': '0.75rem',      # 12px
    'xl': '1rem',         # 16px
    '2xl': '1.5rem',      # 24px
    'full': '9999px',
}

# =============================================================================
# SHADOW SYSTEM
# =============================================================================

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    'none': 'none',
}

# =============================================================================
# COMPONENT SIZES
# =============================================================================

COMPONENT_SIZES = {
    'chart_height': 500,
    'card_height': 300,
    'table_height': 400,
    'sidebar_width': 300,
    'header_height': 80,
    'footer_height': 60,
}

# =============================================================================
# CHART STYLING
# =============================================================================

CHART_COLORS = [
    COLORS['primary'],
    COLORS['secondary'],
    COLORS['accent1'],
    COLORS['accent2'],
    COLORS['accent3'],
    COLORS['accent4'],
    COLORS['success'],
    COLORS['warning'],
    COLORS['error'],
    COLORS['info'],
]

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
    'border_color': COLORS['border'],
}

# =============================================================================
# CSS UTILITY CLASSES
# =============================================================================

def get_css_utilities():
    """Generate CSS utility classes for consistent styling"""
    return f"""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Base styles */
    * {{
        box-sizing: border-box;
    }}
    
    body {{
        font-family: {FONT_FAMILY};
        background-color: {COLORS['background']};
        color: {COLORS['text_primary']};
        line-height: {LINE_HEIGHTS['normal']};
        margin: 0;
        padding: 0;
    }}
    
    /* Typography utilities */
    .text-xs {{ font-size: {FONT_SIZES['xs']}; }}
    .text-sm {{ font-size: {FONT_SIZES['sm']}; }}
    .text-base {{ font-size: {FONT_SIZES['base']}; }}
    .text-lg {{ font-size: {FONT_SIZES['lg']}; }}
    .text-xl {{ font-size: {FONT_SIZES['xl']}; }}
    .text-2xl {{ font-size: {FONT_SIZES['2xl']}; }}
    .text-3xl {{ font-size: {FONT_SIZES['3xl']}; }}
    .text-4xl {{ font-size: {FONT_SIZES['4xl']}; }}
    .text-5xl {{ font-size: {FONT_SIZES['5xl']}; }}
    .text-6xl {{ font-size: {FONT_SIZES['6xl']}; }}
    
    .font-light {{ font-weight: {FONT_WEIGHTS['light']}; }}
    .font-normal {{ font-weight: {FONT_WEIGHTS['normal']}; }}
    .font-medium {{ font-weight: {FONT_WEIGHTS['medium']}; }}
    .font-semibold {{ font-weight: {FONT_WEIGHTS['semibold']}; }}
    .font-bold {{ font-weight: {FONT_WEIGHTS['bold']}; }}
    .font-extrabold {{ font-weight: {FONT_WEIGHTS['extrabold']}; }}
    
    /* Spacing utilities */
    .p-0 {{ padding: {SPACING['0']}; }}
    .p-1 {{ padding: {SPACING['1']}; }}
    .p-2 {{ padding: {SPACING['2']}; }}
    .p-3 {{ padding: {SPACING['3']}; }}
    .p-4 {{ padding: {SPACING['4']}; }}
    .p-5 {{ padding: {SPACING['5']}; }}
    .p-6 {{ padding: {SPACING['6']}; }}
    .p-8 {{ padding: {SPACING['8']}; }}
    
    .m-0 {{ margin: {SPACING['0']}; }}
    .m-1 {{ margin: {SPACING['1']}; }}
    .m-2 {{ margin: {SPACING['2']}; }}
    .m-3 {{ margin: {SPACING['3']}; }}
    .m-4 {{ margin: {SPACING['4']}; }}
    .m-5 {{ margin: {SPACING['5']}; }}
    .m-6 {{ margin: {SPACING['6']}; }}
    .m-8 {{ margin: {SPACING['8']}; }}
    
    /* Border radius utilities */
    .rounded-none {{ border-radius: {BORDER_RADIUS['none']}; }}
    .rounded-sm {{ border-radius: {BORDER_RADIUS['sm']}; }}
    .rounded {{ border-radius: {BORDER_RADIUS['base']}; }}
    .rounded-md {{ border-radius: {BORDER_RADIUS['md']}; }}
    .rounded-lg {{ border-radius: {BORDER_RADIUS['lg']}; }}
    .rounded-xl {{ border-radius: {BORDER_RADIUS['xl']}; }}
    .rounded-2xl {{ border-radius: {BORDER_RADIUS['2xl']}; }}
    .rounded-full {{ border-radius: {BORDER_RADIUS['full']}; }}
    
    /* Shadow utilities */
    .shadow-none {{ box-shadow: {SHADOWS['none']}; }}
    .shadow-sm {{ box-shadow: {SHADOWS['sm']}; }}
    .shadow {{ box-shadow: {SHADOWS['base']}; }}
    .shadow-md {{ box-shadow: {SHADOWS['md']}; }}
    .shadow-lg {{ box-shadow: {SHADOWS['lg']}; }}
    .shadow-xl {{ box-shadow: {SHADOWS['xl']}; }}
    .shadow-2xl {{ box-shadow: {SHADOWS['2xl']}; }}
    .shadow-inner {{ box-shadow: {SHADOWS['inner']}; }}
    
    /* Component styles */
    .dashboard-card {{
        background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['background']} 100%);
        border: 1px solid {COLORS['border']};
        border-radius: {BORDER_RADIUS['lg']};
        padding: {SPACING['6']};
        box-shadow: {SHADOWS['lg']};
        transition: all 0.2s ease;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-2px);
        box-shadow: {SHADOWS['xl']};
    }}
    
    .section-header {{
        color: {COLORS['text_primary']};
        font-size: {FONT_SIZES['3xl']};
        font-weight: {FONT_WEIGHTS['bold']};
        margin-bottom: {SPACING['6']};
        font-family: {FONT_FAMILY};
    }}
    
    .section-subtitle {{
        color: {COLORS['text_secondary']};
        font-size: {FONT_SIZES['lg']};
        font-weight: {FONT_WEIGHTS['medium']};
        margin-bottom: {SPACING['8']};
        font-family: {FONT_FAMILY};
    }}
    
    .metric-title {{
        color: {COLORS['text_secondary']};
        font-size: {FONT_SIZES['sm']};
        font-weight: {FONT_WEIGHTS['medium']};
        margin-bottom: {SPACING['2']};
        font-family: {FONT_FAMILY};
    }}
    
    .metric-value {{
        color: {COLORS['text_primary']};
        font-size: {FONT_SIZES['4xl']};
        font-weight: {FONT_WEIGHTS['extrabold']};
        margin-bottom: {SPACING['3']};
        font-family: {FONT_FAMILY};
        letter-spacing: -0.025em;
    }}
    
    .metric-subtitle {{
        color: {COLORS['text_secondary']};
        font-size: {FONT_SIZES['sm']};
        font-weight: {FONT_WEIGHTS['medium']};
        font-family: {FONT_FAMILY};
    }}
    </style>
    """

# =============================================================================
# CHART CONFIGURATION FUNCTIONS
# =============================================================================

def get_chart_layout(title: str, height: int = 500) -> dict:
    """Get standardized chart layout configuration"""
    return {
        'title': {
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 20,
                'color': COLORS['text_primary'],
                'family': FONT_FAMILY
            }
        },
        'height': height,
        'paper_bgcolor': COLORS['background'],
        'plot_bgcolor': COLORS['surface'],
        'margin': dict(l=50, r=50, t=80, b=50),
        'showlegend': False,
        'xaxis': {
            'tickfont': {
                'color': COLORS['text_secondary'],
                'size': 11,
                'family': FONT_FAMILY
            },
            'title': {
                'text': 'Category',
                'font': {
                    'color': COLORS['text_secondary'],
                    'size': 14,
                    'family': FONT_FAMILY
                }
            },
            'gridcolor': COLORS['grid'],
            'zerolinecolor': COLORS['border']
        },
        'yaxis': {
            'tickfont': {
                'color': COLORS['text_secondary'],
                'size': 11,
                'family': FONT_FAMILY
            },
            'title': {
                'text': 'Amount ($)',
                'font': {
                    'color': COLORS['text_secondary'],
                    'size': 14,
                    'family': FONT_FAMILY
                }
            },
            'gridcolor': COLORS['grid'],
            'zerolinecolor': COLORS['border']
        }
    }

def get_hover_template(label: str, value: str) -> str:
    """Get standardized hover template for charts"""
    return f'<b>%{{x}}</b><br>{label}: {value}<extra></extra>'

def get_hover_label_config(border_color: str = None) -> dict:
    """Get standardized hover label configuration"""
    if border_color is None:
        border_color = COLORS['primary']
    
    return {
        'bgcolor': COLORS['surface'],
        'bordercolor': border_color,
        'font': {
            'color': COLORS['text_primary'],
            'family': FONT_FAMILY,
            'size': 12
        }
    } 