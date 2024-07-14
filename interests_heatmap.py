import plotly.express as px
from utils.similarity import calculate_similarity
from raw_data_loader import RawDataLoader
from collections import OrderedDict


def main():
    chanel_infos = RawDataLoader.get_directors_info_from_folder(folder_name="./raw")
    channel_vectors = OrderedDict()
    for channel in chanel_infos:
        channel_vectors[channel.title] = [(vote.name, vote.rating) for vote in channel.votes]

    vector_of_vectors = []
    for channel_title_1, channel_vector_1 in channel_vectors.items():
        similarity_vector = []
        for channel_title_2, channel_vector_2 in channel_vectors.items():
            # Для построения без учёта рейтинга use_rating=False
            # Для построения с учётом рейтинга use_rating=False
            similarity = calculate_similarity(channel_vector_1, channel_vector_2, use_rating=True)
            # print(channel_title_1, channel_title_2, similarity)
            similarity_vector.append(similarity)
        vector_of_vectors.append(similarity_vector)

    fig = px.imshow(
        vector_of_vectors,
        text_auto=True,
        x=list(channel_vectors.keys()),
        y=list(channel_vectors.keys()),
        height=3000,
        width=3000,
    )
    fig.update_xaxes(side="bottom")
    fig.show()


if __name__ == "__main__":
    main()


