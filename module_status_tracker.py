"""
Status tracking module for tour planning process.
Provides progress indicators, error reporting, and status summaries.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd


class StatusTracker:
    """
    Tracks the status of the tour planning process, including errors, warnings, and progress.
    """
    
    def __init__(self):
        self.steps: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
    def start(self):
        """Mark the start of the process."""
        self.start_time = datetime.now()
        
    def end(self):
        """Mark the end of the process."""
        self.end_time = datetime.now()
        
    def add_step(self, step_name: str, status: str, message: str = "", 
                 details: Optional[Dict[str, Any]] = None):
        """
        Add a processing step with its status.
        
        Args:
            step_name: Name of the processing step
            status: 'success', 'error', 'warning', or 'info'
            message: Human-readable message
            details: Optional dictionary with additional details
        """
        step = {
            "step": step_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.steps.append(step)
        
        if status == "error":
            self.errors.append(step)
        elif status == "warning":
            self.warnings.append(step)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the process status."""
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            
        return {
            "total_steps": len(self.steps),
            "successful_steps": len([s for s in self.steps if s["status"] == "success"]),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "duration_seconds": duration,
            "status": "error" if self.errors else ("warning" if self.warnings else "success")
        }
    
    def print_summary(self):
        """Print a formatted summary of the process."""
        summary = self.get_summary()
        
        print("\n" + "="*80)
        print("TOUR PLANNING PROCESS SUMMARY")
        print("="*80)
        print(f"Total Steps: {summary['total_steps']}")
        print(f"Successful: {summary['successful_steps']}")
        print(f"Errors: {summary['errors']}")
        print(f"Warnings: {summary['warnings']}")
        
        if summary['duration_seconds']:
            print(f"Duration: {summary['duration_seconds']:.2f} seconds")
        
        print(f"\nOverall Status: {summary['status'].upper()}")
        print("="*80)
        
        # Print step details
        print("\nSTEP DETAILS:")
        print("-"*80)
        for i, step in enumerate(self.steps, 1):
            status_symbol = {
                "success": "✓",
                "error": "✗",
                "warning": "⚠",
                "info": "ℹ"
            }.get(step["status"], "?")
            
            print(f"{i}. [{status_symbol}] {step['step']}: {step['message']}")
            if step.get("details"):
                for key, value in step["details"].items():
                    print(f"   - {key}: {value}")
        
        # Print errors if any
        if self.errors:
            print("\n" + "="*80)
            print("ERRORS:")
            print("="*80)
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. {error['step']}: {error['message']}")
                if error.get("details"):
                    for key, value in error["details"].items():
                        print(f"   - {key}: {value}")
        
        # Print warnings if any
        if self.warnings:
            print("\n" + "="*80)
            print("WARNINGS:")
            print("="*80)
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i}. {warning['step']}: {warning['message']}")
                if warning.get("details"):
                    for key, value in warning["details"].items():
                        print(f"   - {key}: {value}")
        
        print("\n" + "="*80 + "\n")
    
    def get_steps_dataframe(self) -> pd.DataFrame:
        """Convert steps to a pandas DataFrame for easy viewing."""
        if not self.steps:
            return pd.DataFrame()
        
        return pd.DataFrame(self.steps)
    
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0


# Global status tracker instance
_status_tracker = StatusTracker()


def get_tracker() -> StatusTracker:
    """Get the global status tracker instance."""
    return _status_tracker


def reset_tracker():
    """Reset the global status tracker (useful for re-running the notebook)."""
    global _status_tracker
    _status_tracker = StatusTracker()

