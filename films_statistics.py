from structures import DirectorsInfoStatistics
from raw_data_loader import RawDataLoader
from main_statistics import count_statistics


def print_top_different_films(statistics: list[DirectorsInfoStatistics], top: int = None):
    # у каких режиссеров были названы самые разнообразные фильмы
    sorted_statistics = sorted(statistics, key=lambda item: len(item.films), reverse=True)
    if top:
        sorted_statistics = sorted_statistics[:top]
    print(f"Top {top if top else 'all'} different films:")
    for stat in sorted_statistics:
        print(stat.name, len(stat.films))
        print(dict(stat.films))


def print_top_count_films(statistics: list[DirectorsInfoStatistics], top: int = None):
    # у каких режиссеров было названо больше всего фильмов
    sorted_statistics = sorted(statistics, key=lambda item: sum(item.films.values()), reverse=True)
    if top:
        sorted_statistics = sorted_statistics[:top]
    print(f"Top {top if top else 'all'} count films:")
    for stat in sorted_statistics:
        print(stat.name, sum(stat.films.values()))
        print(dict(stat.films))


def print_top_popular_films(statistics: list[DirectorsInfoStatistics], top: int = None):
    # какие фильмы появлялись в списках чаще всего
    popular_films = []
    for stat in statistics:
        for film_name, count in stat.films.items():
            popular_films.append((stat.name, film_name, count))
    sorted_films = sorted(popular_films, key=lambda item: item[2], reverse=True)
    if top:
        sorted_films = sorted_films[:top]
    print(f"Top {top if top else 'all'} popular films:")
    for film in sorted_films:
        print(film)


def main():
    chanel_infos = RawDataLoader.get_directors_info_from_folder(folder_name="./raw")
    stats = count_statistics(chanel_infos)
    # топ N режиссеров с самыми разнообразными фильмами
    print_top_different_films(statistics=list(stats.values()), top=20)
    print("\n")
    print_top_count_films(statistics=list(stats.values()), top=20)
    print("\n")
    print_top_popular_films(statistics=list(stats.values()), top=20)

if __name__ == "__main__":
    main()