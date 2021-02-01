def get_contrast_recommendation_wrapper(contrasts):

    results = []

    for contrast in contrasts:
        results.append(get_contrast_recommendation(contrast))

    return results


def get_contrast_recommendation(contrast):

    recommended = "Between 15 and 30 seconds."
    rating = ""
    feedback = ""
    #Temporary set values
    if (contrast >= 0.3):
        rating = "Great!"
        feedback = "The contrast of your shot is great!"
    elif (contrast < 0.3):
        rating = "Bad"
        feedback = "Try to increase your RMS contrast to at least 0.3. You can do this by either changing your settings or by choosing video backgrounds with colors which contrast with the subject. "
    else:
        rating = "Unknown"
        feedback = "Unknown"

    return [recommended, rating, feedback]