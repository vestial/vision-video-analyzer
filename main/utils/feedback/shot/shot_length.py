def get_shot_length_recommendation_wrapper(shot_lengths):

    results = []

    for shot_length in shot_lengths:
        results.append(get_shot_length_recommendation(shot_length))

    return results


def get_shot_length_recommendation(shot_length):

    recommended = "Between 15 and 30 seconds."
    rating = ""
    feedback = ""

    if (shot_length >= 15 and shot_length <= 30):
        rating = "Great!"
        feedback = "The length of your shot is great, since it is between 15 and 30 seconds."
    elif (shot_length < 15):
        rating = "Bad"
        feedback = "Try increasing the length of your shot to at least 15 seconds to enable audience to understand the information presented."
    else:
        rating = "Bad"
        feedback = "Try reducing the length of your shot to at least 30 seconds. Avoid too long shots that the audience cannot understand."

    return [recommended, rating, feedback]