import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from structures import ChannelData, DirectorsInfoStatistics
from raw_data_loader import RawDataLoader
from collections import OrderedDict, defaultdict
from main_statistics import count_statistics, sort_directors_info_by_rating


def get_simple_data_frame(directors_statistics: list[DirectorsInfoStatistics]):
    names = []
    marks = []
    counts = []
    marks_totals = []

    for index, directors_statistic in enumerate(directors_statistics[:105], start=1):
        name = directors_statistic.name
        for score, count in directors_statistic.rating_dict.items():
            names.append(f"{name} [{index}] ")
            marks.append(score)
            counts.append(count)
            marks_totals.append(score * count)

    data = {
        "marks": marks,
        "counts": counts,
        "names": names,
        "marks_totals": marks_totals,
    }
    return data, names


def show_marks_count_graphics(directors_statistics: list[DirectorsInfoStatistics]):
    # распределение по количеству оценок
    data, names = get_simple_data_frame(directors_statistics)
    data_frame = pd.DataFrame(data=data, index=names)
    dfs = data_frame.groupby('names').sum()
    marks_diagram = px.bar(
        data_frame,
        y="names",
        x="counts",
        color="marks",
        barmode="stack",
        color_continuous_scale='portland',
        text=[f"[{data['marks'][i]}]: {data['counts'][i]}" for i in range(len(names))],
        height=3000,
        width=3000,
        category_orders={
            "names": names
        },
    ).update_traces(textangle=0)
    marks_diagram.add_trace(go.Scatter(
        y=dfs.index,
        x=dfs['counts'],
        text=dfs['counts'],
        mode='text',
        textfont=dict(
            size=12,
        ),
        textposition="middle right",
        showlegend=False
    ))
    # marks_diagram.update_layout(yaxis={'categoryorder': 'total ascending'})
    marks_diagram.show()


def show_places_graphics(directors_statistics: list[DirectorsInfoStatistics]):
    names = []
    places = []
    counts = []

    for index, directors_statistic in enumerate(directors_statistics[:100], start=1):
        name = directors_statistic.name
        for place, count in directors_statistic.places_dict.items():
            names.append(f"{name} [{index}]")
            places.append(place)
            counts.append(count)

    data = {
        "places": places,
        "counts": counts,
        "names": names,
    }
    df = pd.DataFrame(data=data, index=names)
    scores_diagram = px.bar(
        data_frame=df,
        y="names",
        x="counts",
        color="places",
        barmode="group",
        text=[f"{places[i]}М: {counts[i]}" for i in range(len(names))],
        category_orders={
            "names": names
        },
        color_continuous_scale='portland',
        height=3000,
        width=3000,
    )
    scores_diagram.show()


def main():
    chanel_infos = RawDataLoader.get_directors_info_from_folder(folder_name="./raw")
    stats = count_statistics(chanel_infos)
    sorted_stat = sort_directors_info_by_rating(stats)
    show_marks_count_graphics(sorted_stat)


if __name__ == "__main__":
    main()
