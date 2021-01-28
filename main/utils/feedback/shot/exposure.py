def get_exposure_recommendation_wrapper(exposures):

    results = []

    for exposure in exposures:
        results.append(get_exposure_recommendation(exposure))

    return results


def get_exposure_recommendation(exposure):

    results = ["Exposure recommended", "Exposure rating", " Exposure feedback"]

    return results
