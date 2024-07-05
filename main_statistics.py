from structures import ChannelData, DirectorsInfoStatistics
from raw_data_loader import RawDataLoader
from collections import OrderedDict, defaultdict


def count_statistics(channel_data_list: list[ChannelData]) -> OrderedDict[str, DirectorsInfoStatistics]:
    directors_statistics: OrderedDict[str, DirectorsInfoStatistics] = OrderedDict()

    for channel_data in channel_data_list:
        for director_info in channel_data.votes:
            if director_info.name not in directors_statistics:
                directors_statistics[director_info.name] = DirectorsInfoStatistics(
                    name=director_info.name,
                    films=defaultdict(int),
                    total_rating=0,
                    total_votes=0,
                    rating_dict={5: 0, 3: 0, 2: 0, 1: 0},
                    places_dict={i: 0 for i in range(1, 31)},
                    final_place=None,
                    average_vote_place=None,
                )
            directors_statistics[director_info.name].total_rating += director_info.rating
            directors_statistics[director_info.name].total_votes += 1
            directors_statistics[director_info.name].rating_dict[director_info.rating] += 1
            directors_statistics[director_info.name].places_dict[director_info.index] += 1
            for film in director_info.films:
                directors_statistics[director_info.name].films[film] += 1
    for directors_statistic in directors_statistics.values():
        places_sum = 0
        places_count = 0
        for place, count in directors_statistic.places_dict.items():
            if count:
                places_sum += place
                places_count += 1
        directors_statistic.average_vote_place = places_sum/places_count
    return directors_statistics


def sort_directors_info_by_rating(
        directors_info_statistics: OrderedDict[str, DirectorsInfoStatistics]
) -> list[DirectorsInfoStatistics]:
    sorted_values: list[DirectorsInfoStatistics] = sorted(
        directors_info_statistics.values(),
        key=lambda item: (
            item.total_rating,
            item.total_votes,
            item.rating_dict[5],
            item.rating_dict[3],
            item.rating_dict[2],
            item.rating_dict[1],
            item.average_vote_place,
        ),
        reverse=True,
    )
    for index, value in enumerate(sorted_values, start=1):
        # value.title_name = f"{value.title_name} [{index}]"
        value.final_place = index
    return sorted_values


def main():
    chanel_infos = RawDataLoader.get_directors_info_from_folder(folder_name="./raw")
    stats = count_statistics(chanel_infos)
    for directors_stat in sort_directors_info_by_rating(stats):
        print(f"[{directors_stat.final_place}] {directors_stat.name} = {directors_stat.total_rating}, "
              f"votes={directors_stat.total_votes}, avg={round(directors_stat.average_vote_place, 3)}")
        print(directors_stat.rating_dict)
        print(f"Films {len(directors_stat.films)}: {dict(directors_stat.films)}")


if __name__ == "__main__":
    main()
