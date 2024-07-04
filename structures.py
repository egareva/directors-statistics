import dataclasses
from typing import Optional


@dataclasses.dataclass
class DirectorInfo:
    name: str
    index: int
    rating: int
    films: list

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


@dataclasses.dataclass
class ChannelData:
    title: str
    link: str
    votes: list[DirectorInfo]


@dataclasses.dataclass
class DirectorsInfoStatistics:
    name: str
    films: dict[str, int]
    total_rating: int
    total_votes: int
    rating_dict: dict[int, int]
    places_dict: dict[int, int]
    final_place: Optional[int] = None
