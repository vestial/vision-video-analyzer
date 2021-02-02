def get_exposure_recommendation_wrapper(exposures):

    results = []

    for exposure in exposures:
        results.append(get_exposure_recommendation(exposure))

    return results


def get_exposure_recommendation(exposure):

    recommended = "Neither under- nor overexposed."
    rating = ""
    feedback = ""

    if (exposure == "Shot is underexposed!"):
        rating = "Bad"
        feedback = "Try increasing the brightness of the shot by using brighter lights and using lighter colored backgrounds."
    elif (exposure == "Shot is overexposed!"):
        rating = "Bad"
        feedback = "Try reducing the brightness of the shot by avoiding strong lights and using darker colored backgrounds."
    elif (exposure == "Exposure is normal."):
        rating = "Great"
        feedback = "Your exposure is already great!"
    else:
        rating = "Bad"
        feedback = "Try increasing the brightness of the underexposed/dark shot by using brighter lights and using lighter colored backgrounds. Also, Try reducing the brightness of the overexposed/bright shot by avoiding strong lights and using darker colored backgrounds."

    return [recommended, rating, feedback]
