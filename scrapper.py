import json
import requests
from bs4 import BeautifulSoup
import re as regex

def scrape_view_count(video_url):
    response = requests.get(video_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script tag containing the JSON data
        script_content = soup.find('body').find('script').string

        match = regex.search(r'var\s+(\w+)\s+=\s+({.*?});', script_content)

        if match:
            # json_variable_name = match.group(1)
            json_content = match.group(2)

            # Parse the JSON content
            data = json.loads(json_content)

            # viewCount
            view_count = data['videoDetails']['viewCount']

            return view_count
        else:
            print("Failed to extract JSON data from script.")

