# Get the rating and recommendation based on the audio sample rate.
def get_sample_rate_recommendation(video):
    rating = ""
    recommendation = ""
    sample_rate = float(video.sample_rate)
    if sample_rate >= 44.1 and sample_rate <= 48:
        rating = "Great!"
        recommendation = "Great audio sample rate!"
    elif sample_rate > 48:
        rating = "Good"
        recommendation = "Good sample rate. However, audio sample rate above 48.0 kHz has diminishing returns. Try lowering it to 48.0 kHz to minimize data usage"
    else:
        rating = "Bad"
        recommendation = "Your sample rate is too low. Try increasing it to at least 44.1 kHz to prevent sound distortion."
    return (rating, recommendation)
