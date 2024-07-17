"""
Скрипт проверки схожести имен режиссеров и названий фильмов
1. Если есть похожие имена режиссеров, которые после ручной проверки оказываются одинаковыми,
то нужно заменить имя на указанное на Кинопоиске
2. Могут быть ложные срабатывания:
например, Дэвид Литч, Дэвид Лин, Дэвид Линч - разные режиссеры, хотя скрипт определяет их как похожих
"""


import copy
from collections import defaultdict
from nltk.util import ngrams
from raw_data_loader import RawDataLoader
from structures import ChannelData


def jaccard_similarity(word1: str, word2: str, n: int = 2) -> float:
    """ Функция схожести двух строк по n-граммам """
    word1_bigrams = list(ngrams(word1, n))
    word2_bigrams = list(ngrams(word2, n))

    intersection = len(list(set(word1_bigrams).intersection(set(word2_bigrams))))
    union = (len(set(word1_bigrams)) + len(set(word2_bigrams))) - intersection

    return float(intersection) / union


def check_directors_similarity(directors_list: list[str]) -> None:
    for index, director_name_1 in enumerate(directors_list):
        for director_name_2 in directors_list:
            if director_name_1 != director_name_2:
                similarity = jaccard_similarity(director_name_1, director_name_2)
                if 0.4 < similarity <= 1:
                    print(f"{director_name_1} | {director_name_2} | {similarity}")


def check_directors_films_similarity(channel_datas: list[ChannelData]):
    directors_films = defaultdict(list)
    for channel_data in channel_datas:
        votes = copy.deepcopy(channel_data.votes)
        for vote in votes:
            directors_films[vote.name].extend(vote.films)

    for director, films in directors_films.items():
        for index, film1 in enumerate(films):
            for film2 in films[index:]:
                similarity = jaccard_similarity(film1, film2)
                if 0.2 < similarity < 1:
                    print(f"{director}: {film1} | {film2} | {similarity}")


def main():
    channel_infos = RawDataLoader.get_directors_info_from_folder(folder_name="./raw")
    directors_names = {vote.name for channel in channel_infos for vote in channel.votes}
    print("Directors similarity: ")
    check_directors_similarity(list(directors_names))
    print("\nFilms similarity: ")
    check_directors_films_similarity(channel_infos)


if __name__ == "__main__":
    main()
