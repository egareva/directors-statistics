from structures import ChannelData


class ChannelDataValidator:
    MAX_DIRECTORS_COUNT = 30

    @staticmethod
    def validate_directors_count(channel_data: ChannelData):
        if len(channel_data.votes) != ChannelDataValidator.MAX_DIRECTORS_COUNT:
            print(f"{channel_data.title} count {len(channel_data.votes)}")

    @staticmethod
    def validate_same_directors(channel_data: ChannelData):
        if len(channel_data.votes) != len(set(channel_data.votes)):
            print(f"{channel_data.title} has same directors")

    @staticmethod
    def validate(channel_data: ChannelData):
        ChannelDataValidator.validate_directors_count(channel_data)
        ChannelDataValidator.validate_same_directors(channel_data)
