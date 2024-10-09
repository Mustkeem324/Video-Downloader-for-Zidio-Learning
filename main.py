import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re

def sanitize_filename(filename, max_length=50):
    # Remove leading and trailing whitespace
    filename = filename.strip()
    # Replace multiple spaces with a single underscore
    filename = re.sub(r'\s+', '_', filename)
    # Remove any characters that are not alphanumeric, underscores, or dashes
    safe_name = re.sub(r'[^\w\-_\.]', '_', filename)
    # Limit the filename length
    return safe_name[:max_length]

def download_video(video_url, video_name, save_dir):
    # Replace spaces with underscores in the lesson name to create a valid file name
    print(f"Download started: {video_name}")
    video_name_safe = sanitize_filename(video_name) + ".mp4"
    save_path = os.path.join(save_dir, video_name_safe)

    # Use a session for better performance
    with requests.Session() as session:
        response = session.get(video_url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        
        # Get the total file size from the response headers
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        # Open the file and write chunks of the video
        with open(save_path, 'wb') as video_file:
            chunk_size = 8192  # 8 KB
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    video_file.write(chunk)
                    downloaded_size += len(chunk)

                    # Calculate and display the download progress
                    if total_size > 0:
                        percent = (downloaded_size / total_size) * 100
                        print(f"Downloaded {downloaded_size} of {total_size} bytes ({percent:.2f}%)", end='\r')

    print(f"\nDownloaded: {video_name_safe}")


# Function to scrape video URLs and lesson details
def scrape_course_details(course_url):
    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cookie': 'strictly_allow=1; performance_allow=1; functional_allow=1; targeting_allow=1; allow=1; XSRF-TOKEN=eyJpdiI6ImJWZXpjTnlMQ0JLcC9lbkVnSlNxK3c9PSIsInZhbHVlIjoiWFNwZWxJWUwrUE9jRHAxbzAxekdkcmVsM3RXRlQ5bzBTZkdrZUpkQU41SDNUc2RKUVdNVWx2aU8rT2k2Mkd3ZVh6NS8rcHdwRlpFWW12c1hlRVROSUtXYThzRjRMdzR1Z2NXTndTNU5pc2pIMlRzcUU4eURzOXFYTVNjbjNDaVQiLCJtYWMiOiJhZDNmNWJiN2YxZmJkY2ZmYmQwZmM3MjYwNGZiYjA5NzRkMDA2ZTI0NmNiZTIwNWUxNmViNmFlYjAzYjliOWQzIiwidGFnIjoiIn0%3D; zidio_training_and_internships_session=eyJpdiI6IjlHL0t4cFNTZE9FMDBVYjhtQ0FoeHc9PSIsInZhbHVlIjoiSDZuRkczTTJIdFRFZU1JZ0dRYlZLT1VLdGVlcit6WGk4NmMwS1pkc1BLcGdYT1dTTG5ycUJZYWFDL2VNaTR6cG5kWlc5VTNZa1E2TndvYllGc0Y4YUFMendlVkRqSTViR2hOZE9xdElSeUc4NEp6ZFFuNGJBeEp4UGcyb0NNQ3ciLCJtYWMiOiIyYjUxMmNhYTllZDdiNGM2ZDZiNmMwNjMyOWIxZTJjZjI4MzNlY2RmNDc1ZjMzZWNiZmI0ODhmMmE4MzU2YmFhIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IlIyV2RLa2QyUWhTMG5hcDFuU0h6QXc9PSIsInZhbHVlIjoidEZlOUY4bUtLeGNtNVV6MlBKcnNtZ1p2UWFrTWhEVEIzVkZTU1JjQ1RzUnBqN3JZcmJ5NWNpZlJKS3hGZzF5b0tqSU44TW5wcjI3dkFLZFBXZ25nWVMzcWZoMTVreExSSEtQU21xaGpxS081eGZUNnBoMmo5ZTFxNlBwNCsyb3kiLCJtYWMiOiI1N2ZkODBlZjdjMGI4ZmU3NmZiMmZlMWFmN2RjMWM5OWMxMWNiNmE2YjI3ZDE4YmQ2OGNkZjQyMjBiODY1ZmY3IiwidGFnIjoiIn0%3D; zidio_training_and_internships_session=eyJpdiI6IkZQVHQ5Q3J2Z3Y5Q1p2UnJxdmV4aGc9PSIsInZhbHVlIjoiU0NLaGpDbk9RZktTK0tWQXJzM1F1Ti95cEVXelJJY0VsZVVDY2hyTjdXN2xxYXFLWTdPdHlvTkpaaWVFNk5sUEx3WFRHN25WdnFOQ0NyTUlkeTZuUUxtS1lMOWtwdGQzcTZVR09RYm9XRlphN1lYODNtWU83WVEydEZBRzdQRnMiLCJtYWMiOiJiZWU5ZjkxNzk2NzMyMGE4ZjEyMjY0YmU0MDczZTdmMmYyY2EyOTMzZGM4NWE2YjY1MTdiN2QxNWRiMzQ4OTgyIiwidGFnIjoiIn0%3D',
      'dnt': '1',
      'priority': 'u=0, i',
      'referer': 'https://zidiolearning.in/fullscreen-view/3/252',
      'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
      'sec-ch-ua-mobile': '?1',
      'sec-ch-ua-platform': '"Android"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36'
    }

    response = requests.request("GET", course_url, headers=headers, data=payload)
    print(f"URL : {course_url} = {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to store lesson details
    lessons = []

    # Extract lesson information (e.g., ID, name, and duration)
    lesson_divs = soup.find_all('div', class_='single_play_list')

    for lesson_div in lesson_divs:
        # Extract lesson name (trim extra spaces and newlines)
        lesson_name = lesson_div.find('span', onclick=True).get_text(strip=True)
        lesson_duration = lesson_div.find('span', class_='course_play_duration').get_text(strip=True)
        lesson_id = lesson_div.get('id').split('_')[-1]  # Extract lesson ID

        # Append lesson details
        lessons.append({
            'lesson_id': lesson_id,
            'name': lesson_name,
            'duration': lesson_duration
        })


    return lessons

# Function to scrape video URLs for a lesson
def scrape_video_urls(course_id, lesson_id):
    video_page_url = f"https://zidiolearning.in/fullscreen-view/{course_id}/{lesson_id}"
    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cookie': 'strictly_allow=1; performance_allow=1; functional_allow=1; targeting_allow=1; allow=1; XSRF-TOKEN=eyJpdiI6ImJWZXpjTnlMQ0JLcC9lbkVnSlNxK3c9PSIsInZhbHVlIjoiWFNwZWxJWUwrUE9jRHAxbzAxekdkcmVsM3RXRlQ5bzBTZkdrZUpkQU41SDNUc2RKUVdNVWx2aU8rT2k2Mkd3ZVh6NS8rcHdwRlpFWW12c1hlRVROSUtXYThzRjRMdzR1Z2NXTndTNU5pc2pIMlRzcUU4eURzOXFYTVNjbjNDaVQiLCJtYWMiOiJhZDNmNWJiN2YxZmJkY2ZmYmQwZmM3MjYwNGZiYjA5NzRkMDA2ZTI0NmNiZTIwNWUxNmViNmFlYjAzYjliOWQzIiwidGFnIjoiIn0%3D; zidio_training_and_internships_session=eyJpdiI6IjlHL0t4cFNTZE9FMDBVYjhtQ0FoeHc9PSIsInZhbHVlIjoiSDZuRkczTTJIdFRFZU1JZ0dRYlZLT1VLdGVlcit6WGk4NmMwS1pkc1BLcGdYT1dTTG5ycUJZYWFDL2VNaTR6cG5kWlc5VTNZa1E2TndvYllGc0Y4YUFMendlVkRqSTViR2hOZE9xdElSeUc4NEp6ZFFuNGJBeEp4UGcyb0NNQ3ciLCJtYWMiOiIyYjUxMmNhYTllZDdiNGM2ZDZiNmMwNjMyOWIxZTJjZjI4MzNlY2RmNDc1ZjMzZWNiZmI0ODhmMmE4MzU2YmFhIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IlIyV2RLa2QyUWhTMG5hcDFuU0h6QXc9PSIsInZhbHVlIjoidEZlOUY4bUtLeGNtNVV6MlBKcnNtZ1p2UWFrTWhEVEIzVkZTU1JjQ1RzUnBqN3JZcmJ5NWNpZlJKS3hGZzF5b0tqSU44TW5wcjI3dkFLZFBXZ25nWVMzcWZoMTVreExSSEtQU21xaGpxS081eGZUNnBoMmo5ZTFxNlBwNCsyb3kiLCJtYWMiOiI1N2ZkODBlZjdjMGI4ZmU3NmZiMmZlMWFmN2RjMWM5OWMxMWNiNmE2YjI3ZDE4YmQ2OGNkZjQyMjBiODY1ZmY3IiwidGFnIjoiIn0%3D; zidio_training_and_internships_session=eyJpdiI6IkZQVHQ5Q3J2Z3Y5Q1p2UnJxdmV4aGc9PSIsInZhbHVlIjoiU0NLaGpDbk9RZktTK0tWQXJzM1F1Ti95cEVXelJJY0VsZVVDY2hyTjdXN2xxYXFLWTdPdHlvTkpaaWVFNk5sUEx3WFRHN25WdnFOQ0NyTUlkeTZuUUxtS1lMOWtwdGQzcTZVR09RYm9XRlphN1lYODNtWU83WVEydEZBRzdQRnMiLCJtYWMiOiJiZWU5ZjkxNzk2NzMyMGE4ZjEyMjY0YmU0MDczZTdmMmYyY2EyOTMzZGM4NWE2YjY1MTdiN2QxNWRiMzQ4OTgyIiwidGFnIjoiIn0%3D',
      'dnt': '1',
      'priority': 'u=0, i',
      'referer': 'https://zidiolearning.in/fullscreen-view/3/252',
      'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
      'sec-ch-ua-mobile': '?1',
      'sec-ch-ua-platform': '"Android"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36'
    }

    response = requests.request("GET", video_page_url, headers=headers, data=payload)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract video URLs from <source> tags
    video_sources = soup.find_all('source')
    video_urls = [source['src'] for source in video_sources if 'mp4' in source['src']]

    return video_urls

# Main function to download videos for all lessons in the course
def course_download(course_id, save_dir="videos"):
    course_url = f"https://zidiolearning.in/fullscreen-view/3/7"  # Adjust this based on actual course URL
    lessons = scrape_course_details(course_url)

    # Create folder if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Process each lesson
    for lesson in lessons:
        print(f"Processing lesson:{lesson['name']}(ID: {lesson['lesson_id']}, Duration: {lesson['duration']})")
        video_name = lesson['name']
        video_urls = scrape_video_urls(course_id, lesson['lesson_id'])
        if not video_urls:
            print(f"No video found for lesson: {lesson['name']}")
            continue
        
        # Download each video in parallel and save with the lesson name and ID
        with ThreadPoolExecutor() as executor:
            executor.map(lambda video_url: download_video(video_url, f"{lesson['name']}_ID{lesson['lesson_id']}", save_dir), video_urls)
            print(f"Downloaded video for lesson: {lesson['name']}")
    print("All videos downloaded successfully.")

# Example usage
course_id = 3
course_download(course_id)


