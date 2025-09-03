# Data logging module
import pandas as pd
import csv

class Logger:
    def __init__(self, output_csv='traffic_log.csv', enable_encryption=False):
        self.output_csv = output_csv
        self.enable_encryption = enable_encryption

    def log(self, data):
        # data: dict with keys ['timestamp', 'count', 'detections']
        # Convert detections to string for CSV storage
        log_data = data.copy()
        log_data['detections'] = str(len(data.get('detections', [])))  # Store count instead of full data
        
        df = pd.DataFrame([log_data])
        df.to_csv(self.output_csv, mode='a', header=not self._file_exists(), index=False)

    def _file_exists(self):
        try:
            with open(self.output_csv, 'r') as f:
                return True
        except FileNotFoundError:
            return False
