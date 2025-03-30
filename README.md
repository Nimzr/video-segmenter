# VideoSegmenter Project

A simple web application to display videos (like YouTube) with a color-coded timeline breakdown showing different content segments (intro, main content, ads, etc.).

## Features

* Lists videos from a `data/videos.json` file.
* Embeds videos for viewing.
* Displays tags associated with each video.
* Shows a visual timeline below each video, color-coded by segment type (e.g., content, intro, ad).
* Timeline segments show details on hover (label, start/end time, type).

## Technology Stack

* **Backend:** Python 3, Flask
* **Frontend:** HTML, CSS, Jinja2
* **Data:** JSON

## Setup and Running

1.  **Prerequisites:** Python 3.7+ and `pip` installed.
2.  **Clone/Download:** Get the project files.
3.  **Navigate:** `cd VideoSegmenter`
4.  **(Recommended) Create Virtual Environment:**
    * `python -m venv venv`
    * Activate:
        * Windows: `.\venv\Scripts\activate`
        * macOS/Linux: `source venv/bin/activate`
5.  **Install Dependencies:** `pip install -r requirements.txt`
6.  **Run Development Server:** `python app.py`
7.  **Access:** Open your web browser and go to `http://127.0.0.1:5000` or `http://localhost:5000`.

## Adding/Updating Videos

1.  Determine the Channel Name and Video Title.
2.  **Create a Sanitized Filename:**
    * Combine the channel name and video title (e.g., `channelname-videoname`).
    * Convert to lowercase.
    * Replace spaces and consecutive hyphens with a single hyphen (`-`).
    * Remove any characters that are not letters, numbers, hyphens, or underscores.
    * Append `.yaml` to the end.
    * Example: "My Channel / Vids" and "Cool Video Title!" becomes `my-channel-vids-cool-video-title.yaml`.
    * **Ensure the filename is unique within the `data/` directory.**
3.  Navigate to the `data/` directory.
4.  **To Add:** Create the new file using the sanitized name (e.g., `my-channel-vids-cool-video-title.yaml`).
5.  **To Update:** Edit the existing `.yaml` file corresponding to the video.
6.  Structure the content of the YAML file as a dictionary representing one video.
7.  **Required Fields Inside YAML:** `id` (use the unique video ID like from YouTube), `title`, `embed_url`, `total_duration_seconds`, `timeline`. The `id` field is crucial for unique identification, even though the filename is human-readable.
8.  **Timeline Segments:** Each item in the `timeline` list needs `start` (seconds), `end` (seconds), and `type`. `label` is recommended.
9.  **Comments:** Feel free to add comments using `#` anywhere in the YAML file.
10. **Type -> Color Mapping:** The `type` value (e.g., "content") determines the color via CSS (`.segment-content`). Add CSS rules for new types.
11. Ensure segment times are continuous and the final `end` matches `total_duration_seconds`.
12. Save the `.yaml` file.
13. Restart the Flask server (`Ctrl+C` and `python app.py`) or rely on automatic reload (`debug=True`).

## Automatic Analysis

The app automatically calculates a basic content analysis based on the timeline:
* It sums the duration of all segments marked with `type: 'content'`.
* It compares this to the `total_duration_seconds`.
* If content is >= 60% (configurable in `app.py`), it's marked "Primarily Content". Otherwise, it's marked "Mixed Content/Fluff".
* This appears as the "Analysis:" note below the video title.

## Deployment to Azure

This Flask application can be deployed to Azure App Service using various methods (e.g., Zip Deploy, Docker Container, Git Deploy). You would typically need:

1.  An Azure Account.
2.  Azure CLI (optional but helpful).
3.  A `Procfile` (for some deployment methods) telling Azure how to start the app (e.g., `web: gunicorn --bind 0.0.0.0:$PORT app:app`).
4.  Install `gunicorn` (`pip install gunicorn` and add to `requirements.txt`) as a production-ready web server.
5.  Configure the App Service instance (Python version, startup command).