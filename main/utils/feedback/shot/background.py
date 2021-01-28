def get_background_recommendation_wrapper(backgrounds):

    results = []

    for background in backgrounds:
        results.append(get_background_recommendation(background))

    return results


def get_background_recommendation(background):

    results = [
        "Background recommended", "Background rating", " Background feedback"
    ]

    return results