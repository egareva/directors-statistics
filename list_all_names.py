import copy
from collections import defaultdict
from structures import ChannelData
from raw_data_loader import RawDataLoader


"""
1. Вывести список режиссеров по алфавиту, провалидировать корректность написания
2. Для валидации корректности можно использовать функцию похожести 
   (сравнить каждого с каждым и вывести похожих, но близких)
3. Провалидировать фильмы на корректность написания
"""


def get_unique_directors(channel_datas: list[ChannelData], top: int | None = None, print_rating: bool = False):
    all_names_by_count = defaultdict(int)
    all_names_by_rating = defaultdict(int)
    directors_films = defaultdict(list)
    for channel_data in channel_datas:
        votes = copy.deepcopy(channel_data.votes)
        if top:
            votes = votes[:top]
        for vote in votes:
            all_names_by_count[vote.name] += 1
            all_names_by_rating[vote.name] += vote.rating
            directors_films[vote.name].extend(vote.films)

    print(f"Total channels: {len(channel_datas)}\n")
    print(f"Total names: {len(all_names_by_count)}\n")
    for name in sorted(all_names_by_count.keys()):
        print(name)
    print("\n")
    if print_rating:
        for name in sorted(all_names_by_count.items(), key=lambda item: item[1], reverse=True):
            print(name)
        print("\n")
        print(f"Rating stats")
        for name in sorted(all_names_by_rating.items(), key=lambda item: item[1], reverse=True):
            print(name)
    print("\nDirectors films:")
    for director_name, directors_film in directors_films.items():
        if directors_film:
            print(f"{director_name} [{len(set(directors_film))}]: {set(directors_film)}")


def main():
    chanel_infos = RawDataLoader.get_directors_info_from_folder(folder_name="./raw")
    get_unique_directors(chanel_infos, print_rating=True)


main()
