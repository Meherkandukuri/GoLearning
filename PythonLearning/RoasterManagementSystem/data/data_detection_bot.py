import pandas as pd

class DataDetectionBot:
    def __init__(self):
        self.column_identifiers = {
            'EMP ID': ['emp', 'id', 'employee', 'staff'],
            'Name': ['name', 'employee name', 'staff'],
            'date': ['date', 'day', 'd-', 'shift date'],
            'shift': ['shift', 'timing', 'schedule', 'pattern'],
            'department': ['dept', 'department', 'team'],
            'position': ['position', 'role', 'designation']
        }
        self.date_formats = [
            "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d", "%d-%b-%y", 
            "%d %B %Y", "%d-%m-%y", "%m-%d-%y", "%y-%m-%d"
        ]

    def detect_columns(self, df):
        detected = {}
        for col in df.columns:
            col_lower = str(col).lower()
            for field, identifiers in self.column_identifiers.items():
                if any(id in col_lower for id in identifiers):
                    detected[field] = col
                    break
        return detected