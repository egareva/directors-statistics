def calculate_similarity(vector1: list[tuple[str, int]], vector2: list[tuple[str, int]], use_rating: bool):
    if use_rating:
        v1_dict = {v[0]: v[1] for v in vector1}
        v2_dict = {v[0]: v[1] for v in vector2}
    else:
        v1_dict = {v[0]: 1 for v in vector1}
        v2_dict = {v[0]: 1 for v in vector2}
    intersection = v1_dict.keys() & v2_dict.keys()
    square_sum = 0
    for key in intersection:
        square_sum += (v1_dict[key] * v2_dict[key])
    norm1 = 0
    for value in v1_dict.values():
        norm1 += value ** 2
    norm1 = norm1 ** 0.5
    norm2 = 0
    for value in v2_dict.values():
        norm2 += value ** 2
    norm2 = norm2 ** 0.5
    return round(square_sum / (norm1*norm2), 3)