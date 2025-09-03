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
        
        # separate detected data count by class 1/2/3/4/5/6
        # annotate the class by their real class type names e.g. bicycle, car
        class_counts = {1: 0, 2: 0, 3: 0, 5: 0, 6: 0, 7: 0}
        class_names = {1: 'bicycle', 2: 'car', 3: 'motorcycle', 5: 'bus', 6: 'train', 7: 'truck'}
        for det in data.get('detections', []):
            class_id = det.get('class')
            if class_id in class_counts:
                class_counts[class_id] += 1

        # Annotate the class names
        for class_id, count in class_counts.items():
            log_data[class_names.get(class_id, f'class_{class_id}')] = count

        log_data['total_detections'] = sum(class_counts.values())
        
        # remove "detections" details from log_data
        log_data.pop('detections', None)

        df = pd.DataFrame([log_data])
        df.to_csv(self.output_csv, mode='a', header=not self._file_exists(), index=False)

    def _file_exists(self):
        try:
            with open(self.output_csv, 'r') as f:
                return True
        except FileNotFoundError:
            return False
