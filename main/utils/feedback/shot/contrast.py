def get_contrast_recommendation_wrapper(contrasts):

    results = []

    for contrast in contrasts:
        results.append(get_contrast_recommendation(contrast))

    return results


def get_contrast_recommendation(contrast):

    results = ["Contrast recommended", "Contrast rating", " Contrast feedback"]

    return results