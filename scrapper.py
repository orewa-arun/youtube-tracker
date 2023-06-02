import json
import requests
from bs4 import BeautifulSoup
import re as regex


def scrape_stats_count(video_url):
    response = requests.get(video_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script tag containing the JSON data
        view_scrap = soup.find('body').find('script').string
        like_scrap = soup.findAll("script")

        likes = get_likes(like_scrap)
        views = get_views(view_scrap)

    return views, likes


def get_likes(like_scrap):
    for k in like_scrap:

        # regex for 'var variableName = { ... };'
        match = regex.search(r'var\s+(\w+)\s+=\s+({.*?});', str(k))

        if match:
            json_variable_name = match.group(1)

            if json_variable_name == "ytInitialData":
                json_content = match.group(2)

                # Parse the JSON content
                data = json.loads(json_content)

                like_script = data["contents"]["twoColumnWatchNextResults"]["results"][
                    "results"]["contents"][0]["videoPrimaryInfoRenderer"][
                        "videoActions"]["menuRenderer"]["topLevelButtons"][0][
                            "segmentedLikeDislikeButtonRenderer"]["likeButton"][
                                "toggleButtonRenderer"]["defaultText"][
                                    "accessibility"]["accessibilityData"]["label"]
                likes = like_script.split(maxsplit=1)[0].replace(",", "")

                return likes


def get_views(view_scrap):
    match = regex.search(r'var\s+(\w+)\s+=\s+({.*?});', view_scrap)

    if match:
        # json_variable_name = match.group(1)
        json_content = match.group(2)

        # Parse the JSON content
        data = json.loads(json_content)

        # viewCount
        view_count = data['videoDetails']['viewCount']

        return view_count


# print(scrape_stats_count("https://www.youtube.com/watch?v=0aavCtXiiX4"))
