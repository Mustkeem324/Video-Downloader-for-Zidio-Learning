# Video Downloader for Zidio Learning

This project is a Python script that downloads video lessons from the Zidio Learning platform. It scrapes course details, extracts video URLs, and downloads the videos while displaying the progress.

## Features

- Scrapes course details including lesson names and durations.
- Extracts video URLs from lesson pages.
- Downloads videos concurrently using threads for faster performance.
- Displays download progress as a percentage.

## Requirements

To run this script, you need the following Python packages:

- `requests`
- `beautifulsoup4`
- `concurrent.futures`

You can install the required packages using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set the course ID** in the script. You can adjust the `course_id` variable to point to the course you want to download.

3. **Run the script**:
   ```bash
   python <script-name>.py
   ```

   Replace `<script-name>` with the name of your Python file.

4. **Output**: Videos will be downloaded to a folder named `videos`. If the folder does not exist, it will be created automatically.

## Code Explanation

- `sanitize_filename(filename, max_length=50)`: Cleans up the filename to ensure it's valid and of a reasonable length.
- `download_video(video_url, video_name, save_dir)`: Downloads a video from the provided URL and shows the download progress.
- `scrape_course_details(course_url)`: Scrapes lesson details from a course page.
- `scrape_video_urls(course_id, lesson_id)`: Scrapes video URLs from a lesson's video page.
- `course_download(course_id, save_dir)`: Main function that orchestrates the downloading of videos for all lessons in a course.

## Notes

- Ensure that you have permission to download the videos before running this script, as it may violate the terms of service of the platform.
- The script uses hardcoded headers and cookies for requests. These may need to be updated based on any changes in the website’s security or session management.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
