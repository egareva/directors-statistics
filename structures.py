import dataclasses


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
