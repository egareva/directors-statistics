import time

import requests
from pyquery import PyQuery
from raw_data_loader import RawDataLoader


def find_director(director_name: str, index: int):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
    answer = requests.get(f"https://www.kinopoisk.ru/index.php?kp_query={director_name}", headers=headers)
    doc = PyQuery(answer.text)
    if answer.history and 'name' in answer.history[-1].url:
        # print(f"[{index}] {director_name} redirected")
        return
    try:
        found_name = list(doc(".search_results .most_wanted .name a").items())[0].text()
        if found_name != director_name:
            print(f"[{index}] Different: {director_name} -> {found_name}")
    except IndexError:
        print(f"[{index}] Director not found: {director_name}")


def get_director_page(url: str, director_name: str, ):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
    answer = requests.get(url, headers=headers)
    doc = PyQuery(answer.text)
    found_name = list(doc("h1").items())[0].text()
    if found_name != director_name:
        print(f"Different: {director_name} -> {found_name}")


def check_directors():
    channel_infos = RawDataLoader.get_directors_info_from_folder(folder_name="./raw")
    directors_names = {vote.name for channel in channel_infos for vote in channel.votes}
    for index, director in enumerate(directors_names):
        find_director(director, index)
        time.sleep(0.5)


if __name__ == "__main__":
    check_directors()