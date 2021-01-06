from main.utils.histogram_analyzer import get_exposure_histogram
from main.utils.shots_analyzer import get_background, get_contrast, get_shot_screenshot, get_shots, get_shots_length
from celery import chain


#Use celery to execute tasks sequentially
def celery_analyze_shots(video):
    result = []
    celery_chain = chain(get_shots.si(video), get_exposure_histogram.si(video),
                         get_shots_length.si(video), get_contrast.si(video),
                         get_background.si(video),
                         get_shot_screenshot.si(video))()
    result.append(celery_chain.parent.parent.parent.get())
    result.append(celery_chain.parent.parent.get())
    result.append(celery_chain.parent.get())
    result.append(celery_chain.get())
    return result
