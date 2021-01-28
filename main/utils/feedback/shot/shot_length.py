def get_shot_length_recommendation_wrapper(shot_lengths):

    results = []

    for shot_length in shot_lengths:
        results.append(get_shot_length_recommendation(shot_length))

    return results


def get_shot_length_recommendation(shot_length):

    results = [
        "Shot length recommended", "Shot length rating",
        " Shot length feedback"
    ]

    return results