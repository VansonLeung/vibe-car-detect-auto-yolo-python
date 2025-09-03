# uiux/dashboard.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import cv2
import numpy as np
import base64
from detection import Detector
from camera import Camera

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def frame_to_jpeg(frame):
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

def get_frame_with_boxes(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = map(int, det['bbox'])
        label = str(det.get('class', 'car'))
        conf = det.get('confidence', 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return frame

def get_encoded_frame():
    camera = Camera()
    camera.open()
    frame = camera.read()
    detector = Detector(model_path='YOLO11L.pt')
    detections = detector.detect(frame)
    frame = get_frame_with_boxes(frame, detections)
    camera.release()
    jpeg_bytes = frame_to_jpeg(frame)
    encoded = base64.b64encode(jpeg_bytes).decode()
    return f"data:image/jpeg;base64,{encoded}"

app.layout = dbc.Container([
    html.H2("Road Car Traffic Counter - Live Detection"),
    html.Img(id='live-image', src=get_encoded_frame(), style={'width': '80%', 'border': '2px solid #333'}),
    html.Div(id='object-count', style={'marginTop': '20px'})
])

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
