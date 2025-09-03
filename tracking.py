# Tracking and counting module
import numpy as np

class Counter:
    def __init__(self, line_position=(600, 400), direction='vertical'):
        self.line_position = line_position
        self.direction = direction
        self.count = 0

    def update(self, detections, prev_positions):
        # Simple implementation: increment count for each detection crossing the line
        # TODO: Replace with proper tracking logic (e.g., SORT, DeepSORT)
        for det in detections:
            # det['bbox'] = [x1, y1, x2, y2] (single bbox per detection)
            x1, y1, x2, y2 = det['bbox']
            center_y = (y1 + y2) / 2
            center_x = (x1 + x2) / 2
            
            if self.direction == 'vertical':
                if abs(center_y - self.line_position[1]) < 10:  # Close to line
                    self.count += 1
            elif self.direction == 'horizontal':
                if abs(center_x - self.line_position[0]) < 10:  # Close to line
                    self.count += 1
        return self.count
