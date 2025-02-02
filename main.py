import cv2
import numpy as np
import math
import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TrafficAnalyzer:
    def __init__(self):
        self.min_contour_width = 40
        self.min_contour_height = 40
        self.offset = 10
        self.line_height = 1120
        self.min_distance = 13
        self.vehicles = 0
        self.matches = []

    def get_centroid(self, x, y, w, h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        return x + x1, y + y1

    def distance(self, c1, c2):
        return math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2)

    def analyze_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        cap.set(3, 1920)
        cap.set(4, 1080)

        if not cap.isOpened():
            return None

        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        
        start_time = time.time()
        last_reset_time = start_time
        traffic_densities = []

        while ret:
            d = cv2.absdiff(frame1, frame2)
            grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(grey, (5, 5), 0)
            ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(th, np.ones((5, 5)))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
            contours, h = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for (i, c) in enumerate(contours):
                (x, y, w, h) = cv2.boundingRect(c)
                if w < self.min_contour_width or h < self.min_contour_height:
                    continue

                centroid = self.get_centroid(x, y, w, h)
                match_found = any(self.distance((mx, my), centroid) < self.min_distance 
                                for (mx, my) in self.matches)

                if not match_found:
                    self.matches.append(centroid)

                for (x, y) in self.matches[:]:
                    if self.line_height - self.offset < y < self.line_height + self.offset:
                        self.vehicles += 1
                        self.matches.remove((x, y))

            elapsed_time = time.time() - last_reset_time

            if elapsed_time >= 10:
                traffic_density = self.vehicles / elapsed_time if elapsed_time > 0 else 0
                traffic_densities.append(traffic_density)
                self.vehicles = 0
                last_reset_time = time.time()

            frame1 = frame2
            ret, frame2 = cap.read()

        cap.release()
        return np.mean(traffic_densities) if traffic_densities else 0

def determine_traffic_signals(density1, density2):
    """
    Determine traffic light cycle durations based on traffic densities.
    Returns a dictionary with complete signal timing including yellow transitions.
    
    Signal cycle for each junction:
    1. Green light
    2. Yellow light (3 seconds)
    3. Red light while other junction goes through its cycle
    """
    total_density = density1 + density2
    if total_density == 0:
        base_time = 30  # Default time if no traffic
        time1 = time2 = base_time
    else:
        # Calculate proportional times (minimum 15 seconds, maximum 60 seconds)
        time1 = min(60, max(15, int(45 * (density1 / total_density))))
        time2 = min(60, max(15, int(45 * (density2 / total_density))))
    
    yellow_time = 3  # Standard yellow light duration
    
    return {
        "junction1": {
            "green_time": time1,
            "yellow_time": yellow_time,
            "sequence": [
                {"state": "red", "duration": time2 + yellow_time},  # While junction2 is active
                {"state": "green", "duration": time1},
                {"state": "yellow", "duration": yellow_time}
            ]
        },
        "junction2": {
            "green_time": time2,
            "yellow_time": yellow_time,
            "sequence": [
                {"state": "green", "duration": time2},
                {"state": "yellow", "duration": yellow_time},
                {"state": "red", "duration": time1 + yellow_time}  # While junction1 is active
            ]
        },
        "cycle_time": time1 + time2 + (2 * yellow_time)  # Total cycle duration
    }

class VideoHandler(FileSystemEventHandler):
    def __init__(self):
        self.analyzer = TrafficAnalyzer()
        self.videos_processed = set()
        
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.mp4', '.avi', '.mov')):
            self.process_new_video(event.src_path)
    
    def process_new_video(self, video_path):
        if video_path in self.videos_processed:
            return
            
        self.videos_processed.add(video_path)
        video_name = os.path.basename(video_path)
        
        # Wait for both videos to be uploaded
        if len([f for f in os.listdir('Videos') if f.endswith(('.mp4', '.avi', '.mov'))]) >= 2:
            video1_path = os.path.join('Videos', 'junction1.mp4')
            video2_path = os.path.join('Videos', 'junction2.mp4')
            
            if os.path.exists(video1_path) and os.path.exists(video2_path):
                # Analyze videos
                density1 = self.analyzer.analyze_video(video1_path)
                density2 = self.analyzer.analyze_video(video2_path)
                
                if density1 is not None and density2 is not None:
                    signal_timings = determine_traffic_signals(density1, density2)
                    
                    # Write results to a JSON file
                    result = {
                        "junction1": {
                            "density": round(density1, 2),
                            "timings": signal_timings["junction1"]
                        },
                        "junction2": {
                            "density": round(density2, 2),
                            "timings": signal_timings["junction2"]
                        },
                        "total_cycle_time": signal_timings["cycle_time"]
                    }
                    
                    with open('analysis_result.json', 'w') as f:
                        json.dump(result, f)
                    
                    # Clear the processed videos set for next analysis
                    self.videos_processed.clear()

def main():
    # Create Videos directory if it doesn't exist
    os.makedirs('Videos', exist_ok=True)
    
    # Set up the file system observer
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, path='Videos', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
