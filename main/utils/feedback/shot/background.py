def get_background_recommendation_wrapper(backgrounds):

    results = []

    for background in backgrounds:
        results.append(get_background_recommendation(background))

    return results


def get_background_recommendation(background):

    recommended = "Colors that are not black or strong (red, yellow, or bright green).."
    rating = ""
    feedback = ""

    return [recommended, rating, feedback]


def color_picker(rgb):
    result = ""
    if rgb[0] <= 255 and rgb[0] >= 200 and rgb[1] <= 50 and rgb[
            2] <= 50:  #Bright red
        result = "red"

    return result
