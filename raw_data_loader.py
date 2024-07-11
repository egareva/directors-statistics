from structures import ChannelData, DirectorInfo
from utils.tools import get_cleaned_data, clean_quotes, remove_year
from os import walk
from utils.channel_data_validator import ChannelDataValidator


def get_rating(index: int) -> int:
    if index == 1:
        return 5
    if 2 <= index <= 5:
        return 3
    if 6 <= index <= 10:
        return 2
    if index > 30:
        raise Exception()
    return 1


class RawDataLoader:
    @classmethod
    def get_films_list(cls, raw_string: str) -> tuple[str, list[str]]:
        """
        Строка вида:
        Анджей Вайда ("Свадьба" (1972), "Пилат и другие" (1972), "Земля обетованная" (1974), "Пан Тадеуш" (1999)).
        разбивает на имя режиссера и список фильмов
        """
        if '(' in raw_string:
            first_index = raw_string.index('(')
            last_index = raw_string.rindex(')')
            # строку с фильмами делим по точке с запятой на отдельные названия\
            director_name = raw_string[:first_index].strip()
            films_in_string = raw_string[first_index+1:last_index].split(';')
            # убираем из названия год
            # убираем кавычки из названия
            films_list = [clean_quotes(remove_year(film)).strip() for film in films_in_string]
            return director_name, films_list
        # если нет скобок, то вся строчка - имя режиссера (фильмы не указаны)
        return raw_string.strip(), []

    @classmethod
    def load_raw_data(cls, filename: str) -> ChannelData:
        """
        Читает файл и возвращает статистику по каналу
        """
        channel_data = None
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("#") or not line.strip():
                    # пропускаем комментарии и пустые строки
                    continue

                if line.startswith("КАНАЛ: "):
                    channel_name = line.removeprefix("КАНАЛ: ").strip()
                elif line.startswith("ССЫЛКА: "):
                    channel_url = line.removeprefix("ССЫЛКА: ").strip()
                    channel_data = ChannelData(title=channel_name, link=channel_url, votes=[])
                    index = 0
                elif line:
                    index += 1
                    director_line = get_cleaned_data(line)
                    director, films = RawDataLoader.get_films_list(director_line)
                    channel_data.votes.append(
                        DirectorInfo(name=director, index=index, films=films, rating=get_rating(index))
                    )
        return channel_data

    @classmethod
    def get_directors_info_from_folder(cls, folder_name: str) -> list[ChannelData]:
        filenames = next(walk(folder_name), (None, None, []))[2]
        chanel_infos: list[ChannelData] = []
        for filename in filenames:
            print(filename)
            chanel_data = cls.load_raw_data(f"{folder_name}/{filename}")
            ChannelDataValidator.validate(chanel_data)
            chanel_infos.append(chanel_data)
        return chanel_infos
