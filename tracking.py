# Tracking and counting module
import numpy as np

class Counter:
    def __init__(self, line_position=(600, 400), direction='vertical'):
        self.line_position = line_position
        self.direction = direction
        self.crossed_ids = set()
        self.id_class = {}
        self.point_history = {}

    def is_point_crossed_line(self, id, point, line):

        line_x1, line_y1 = line[0]
        line_x2, line_y2 = line[1]

        x, y = point
        if id in self.point_history:
            
            """
            Determines if a point is above a line defined by two points.

            Args:
            - point: A tuple (x0, y0) representing the point to check.
            - line_point1: A tuple (x1, y1) representing the first point on the line.
            - line_point2: A tuple (x2, y2) representing the second point on the line.

            Returns:
            - True if the point is above the line, False if it is below or on the line.
            """
            x0, y0 = x, y
            x1, y1 = line_x1, line_y1
            x2, y2 = line_x2, line_y2
            
            prev_x, prev_y = self.point_history[id]
            

            # Calculate the slope (m) of the line
            if x2 - x1 == 0:  # Avoid division by zero for vertical lines
                return False  # Vertical line; point cannot be above or below

            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1  # y-intercept

            # Calculate the y value of the line at x0
            y_line = m * x0 + b

            self.point_history[id] = point

            if (id < 2):
                print(f"ID: {id} - {x0}\t{y0} vs {x1}\t{y1} vs {y0}\t{y_line}")
            # Check if the point is below the line
            return y0 > y_line            
        else:
            self.point_history[id] = (0, 0)

        return False

    def update(self, detections, line):
        # Simple implementation: increment count for each detection crossing the line
        for det in detections:
            id = det['id']
            x1, y1, x2, y2 = det['bbox']
            center_y = (y1 + y2) / 2
            center_x = (x1 + x2) / 2

            if self.is_point_crossed_line(id, (center_x, center_y), line):
                if id not in self.crossed_ids:
                    print(f"\n>>>>> ID {id} crossed the line. <<<<<\n")
                    self.crossed_ids.add(id)

            self.point_history[id] = (center_x, center_y)
            self.id_class[id] = det['class']

        return len(self.crossed_ids)


    def get_crossed_class_count_representation(self, class_names=None):
        result = {}
        for id in self.crossed_ids:
            class_id = self.id_class.get(id)
            if class_id:
                result[class_id] = result.get(class_id, 0) + 1

        if class_names:
            result = {class_names.get(k, k): v for k, v in result.items()}

        return result
