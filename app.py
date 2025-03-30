# app.py
# import json # No longer needed for loading
import os
import yaml # Import the YAML library
from flask import Flask, render_template

app = Flask(__name__)

# Define the path to the data directory
DATA_DIR = 'data'

# Maps segment type keys (from YAML) to display names
SEGMENT_TYPE_LEGEND = {
    'intro': 'Introduction',
    'content': 'Main Content',
    'ad': 'Advertisement / Sponsor',
    'engagement': 'Engagement Prompt (Like/Sub/etc.)',
    'outro': 'Outro / Recap',
    'other': 'Other / Off-Topic'
    # Add or modify entries here if you use different types in your YAML
}

# Percentage of 'content' type needed to be considered "Primarily Content"
LOGIC_CONTENT_THRESHOLD = 60 # e.g., 60%

def load_video_data():
    """Loads video data from individual YAML files in the DATA_DIR."""
    print(f"--- Attempting to load video data from directory: '{os.path.abspath(DATA_DIR)}'") # Print absolute path
    all_videos = []
    filenames = [] # Initialize filenames list
    try:
        # List all files in the data directory
        print(f"--- Checking directory: {DATA_DIR}")
        if not os.path.isdir(DATA_DIR):
             print(f"--- ERROR: Directory '{DATA_DIR}' not found or is not a directory.")
             return [] # Exit early if directory doesn't exist

        filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(('.yaml', '.yml'))]
        print(f"--- Found YAML files: {filenames}") # Print the list of found files

        if not filenames:
            print("--- No YAML files found in the data directory.")

    except FileNotFoundError:
        print(f"--- ERROR: Data directory not found at {DATA_DIR}")
        return [] # Return empty list if directory doesn't exist
    except Exception as e:
        print(f"--- ERROR listing files in {DATA_DIR}: {e}")
        return []

    for filename in filenames:
        filepath = os.path.join(DATA_DIR, filename)
        print(f"--- Processing file: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                video_data = yaml.safe_load(f)
                print(f"--- Successfully loaded data from {filename}")

                if not isinstance(video_data, dict):
                     print(f"--- WARNING: Content of {filename} is not a dictionary. Skipping.")
                     continue

                # --- Timeline Width Calculation (Existing Logic) ---
                total_duration = video_data.get('total_duration_seconds', 0)
                content_duration = 0

                if total_duration > 0:
                    for segment in video_data.get('timeline', []):
                        try:
                            start = float(segment['start'])
                            end = float(segment['end'])
                            duration = end - start
                            segment['width_percent'] = round((duration / total_duration) * 100, 2)
                            # --- Accumulate content duration ---
                            if segment.get('type') == 'content':
                                content_duration += duration
                        except (KeyError, TypeError, ValueError) as e:
                            print(f"--- WARNING: Invalid segment data in {filename}: {segment}. Error: {e}")
                            segment['width_percent'] = 0
                else:
                     print(f"--- WARNING: Missing or zero total_duration_seconds in {filename}.")
                     for segment in video_data.get('timeline', []):
                        segment['width_percent'] = 0

                # --- Calculate Logic-Based Recommendation ---
                content_percentage = 0
                if total_duration > 0:
                    content_percentage = round((content_duration / total_duration) * 100, 1)
                    if content_percentage >= LOGIC_CONTENT_THRESHOLD:
                        video_data['logic_recommendation'] = 'Primarily Content'
                        video_data['logic_recommendation_css'] = 'good' # For styling class
                    else:
                        video_data['logic_recommendation'] = 'Mixed Content/Fluff'
                        video_data['logic_recommendation_css'] = 'caution'
                else:
                    video_data['logic_recommendation'] = 'Analysis Unavailable'
                    video_data['logic_recommendation_css'] = 'unknown'

                video_data['content_percentage'] = content_percentage # Store for display
                print(f"--- Logic analysis for {filename}: {video_data['logic_recommendation']} ({content_percentage}%)")

                # User recommendation is loaded directly from YAML if present

                all_videos.append(video_data)
                print(f"--- Added video '{video_data.get('title', 'Untitled')}' to the list.")

        except yaml.YAMLError as e:
            print(f"--- ERROR: Could not parse YAML file {filename}: {e}")
        except FileNotFoundError:
             print(f"--- ERROR: File {filename} disappeared during processing?") # Less likely
        except Exception as e:
            print(f"--- ERROR processing file {filename}: {e}")

    print(f"--- Finished loading data. Total videos loaded: {len(all_videos)}")
    return all_videos


@app.route('/')
def index():
    """Serves the main page with the list of videos."""
    videos = load_video_data()
    # Pass the legend data to the template along with videos
    return render_template('index.html',
                           videos=videos,
                           legend_data=SEGMENT_TYPE_LEGEND)


@app.template_filter('format_time')
def format_time_filter(seconds):
    """Converts seconds into MM:SS format for display."""
    try:
        seconds = float(seconds) # Ensure it's a number
        if seconds < 0: return "00:00" # Handle negative times?
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    except (TypeError, ValueError):
        return "N/A" # Handle non-numeric input gracefully


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)