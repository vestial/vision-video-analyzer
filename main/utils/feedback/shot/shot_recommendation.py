from main.utils.feedback.shot.shot_length import get_shot_length_recommendation_wrapper
from main.utils.feedback.shot.background import get_background_recommendation_wrapper
from main.utils.feedback.shot.contrast import get_contrast_recommendation_wrapper
from main.utils.feedback.shot.exposure import get_exposure_recommendation_wrapper


def get_shot_recommendation(exposures, shot_lengths, contrasts, backgrounds):

    exposure_recommendation = get_exposure_recommendation_wrapper(exposures)
    shot_length_recommendation = get_shot_length_recommendation_wrapper(
        shot_lengths)
    contrast_recommendation = get_contrast_recommendation_wrapper(contrasts)
    background_recommendation = get_background_recommendation_wrapper(
        backgrounds)

    results = [
        exposure_recommendation, shot_length_recommendation,
        contrast_recommendation, background_recommendation
    ]

    return results
