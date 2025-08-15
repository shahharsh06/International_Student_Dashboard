"""
Error Handler Utility
Professional error management and user feedback for the dashboard
"""

import streamlit as st
import traceback
from typing import Optional, Dict, Any
from datetime import datetime
import logging

class ErrorHandler:
    """Professional error handling and user feedback system"""
    
    def __init__(self):
        """Initialize the error handler"""
        self.error_log = []
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DashboardErrorHandler')
    
    def display_error(self, title: str, message: str, error_type: str = "error", 
                     show_traceback: bool = False, context: Optional[Dict[str, Any]] = None):
        """
        Display user-friendly error message
        
        Args:
            title: Error title
            message: Error message
            error_type: Type of error (error, warning, info)
            show_traceback: Whether to show technical details
            context: Additional context information
        """
        # Log the error
        self.log_error(title, message, error_type, context)
        
        # Display appropriate error message
        if error_type == "warning":
            st.warning(f"**{title}**: {message}")
        elif error_type == "info":
            st.info(f"**{title}**: {message}")
        else:
            st.error(f"**{title}**: {message}")
        
        # Show context if provided
        if context:
            with st.expander("Error Context"):
                for key, value in context.items():
                    st.write(f"**{key}**: {value}")
        
        # Show traceback for debugging (only in development)
        if show_traceback:
            with st.expander("🐛 Technical Details"):
                st.code(traceback.format_exc())
    
    def handle_exception(self, func):
        """Decorator to handle exceptions gracefully"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.display_error(
                    "Function Error", 
                    str(e), 
                    context={"function": func.__name__, "args": str(args)}
                )
                return None
        return wrapper
    
    def safe_execute(self, func, *args, fallback=None, **kwargs):
        """
        Safely execute a function with error handling
        
        Args:
            func: Function to execute
            *args: Function arguments
            fallback: Fallback value if function fails
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or fallback value
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.display_error(
                "Execution Error",
                f"Failed to execute {func.__name__}: {str(e)}",
                context={"function": func.__name__}
            )
            return fallback
    
    def validate_data(self, data, required_fields: list, data_name: str = "Data"):
        """
        Validate data structure and required fields
        
        Args:
            data: Data to validate
            required_fields: List of required field names
            data_name: Name of the data for error messages
            
        Returns:
            bool: True if valid, False otherwise
        """
        if data is None:
            self.display_error(
                "Data Validation Error",
                f"{data_name} is None or empty",
                error_type="warning"
            )
            return False
        
        missing_fields = []
        for field in required_fields:
            if not hasattr(data, field) or getattr(data, field) is None:
                missing_fields.append(field)
        
        if missing_fields:
            self.display_error(
                "Data Validation Error",
                f"{data_name} missing required fields: {', '.join(missing_fields)}",
                error_type="warning"
            )
            return False
        
        return True
    
    def log_error(self, title: str, message: str, error_type: str, context: Optional[Dict[str, Any]] = None):
        """Log error for debugging and monitoring"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'title': title,
            'message': message,
            'type': error_type,
            'context': context or {}
        }
        
        self.error_log.append(error_entry)
        
        # Log to system logger
        if error_type == "error":
            self.logger.error(f"{title}: {message}")
        elif error_type == "warning":
            self.logger.warning(f"{title}: {message}")
        else:
            self.logger.info(f"{title}: {message}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of recent errors for monitoring"""
        if not self.error_log:
            return {"total_errors": 0, "error_types": {}, "recent_errors": []}
        
        error_types = {}
        for error in self.error_log:
            error_type = error['type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_log),
            "error_types": error_types,
            "recent_errors": self.error_log[-5:]  # Last 5 errors
        }
    
    def clear_error_log(self):
        """Clear the error log"""
        self.error_log.clear()
        self.logger.info("Error log cleared")
    
    def display_error_summary(self):
        """Display error summary for debugging"""
        summary = self.get_error_summary()
        
        if summary["total_errors"] == 0:
            st.success("✅ No errors logged")
            return
        
        st.markdown("### Error Summary")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Errors", summary["total_errors"])
        
        with col2:
            st.metric("Error Types", len(summary["error_types"]))
        
        # Show error type breakdown
        if summary["error_types"]:
            st.markdown("**Error Type Distribution:**")
            for error_type, count in summary["error_types"].items():
                st.write(f"- {error_type}: {count}")
        
        # Show recent errors
        if summary["recent_errors"]:
            with st.expander("Recent Errors"):
                for error in summary["recent_errors"]:
                    st.write(f"**{error['timestamp']}** - {error['title']}: {error['message']}")
        
        # Clear log button
        if st.button("Clear Error Log"):
            self.clear_error_log()
            st.rerun() 