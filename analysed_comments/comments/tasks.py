import logging

from django.conf import settings
from celery.task import task
from watson_developer_cloud import ToneAnalyzerV3, WatsonApiException

from comments.models import Comment


log = logging.getLogger(__file__)


@task
def analyse_comment(comment_id):
    """
    Make a call to the Watson API to determine if the comment with `comment_id` is positive.

    If the API call fails or no tone can be determined set the comment status to 'failed'

    :param comment_id:
    :return:
    """
    log.debug('Analysing comment with id %s', comment_id)
    comment = Comment.objects.get(id=comment_id)
    tone_analyzer = ToneAnalyzerV3(
        version=settings.TONE_ANALYSER_VERSION,
        username=settings.TONE_ANALYSER_USERNAME,
        password=settings.TONE_ANALYSER_PASSWORD,
        url=settings.TONE_ANALYSER_ENDPOINT
    )

    try:
        analysis = tone_analyzer.tone(
            {'text': comment.text},
            'application/json',
            sentences=False
        ).get_result()
    except WatsonApiException as ex:
        # Fail if the watson call failed
        log.error('Failed to analyse comment with ID %s - %s', comment.id, ex)
        comment.status = comment.STATUS_FAILED
        comment.save()
        return

    # Create a dictionary of score -> tone key value pairs
    tones = dict((t['score'], t['tone_id']) for t in analysis['document_tone']['tones']
                 if t['tone_id'] != 'analytical')

    # Fail if no tones found
    if len(tones) == 0:
        log.error('Failed to analyse comment with ID %s - %s', comment.id, ex)
        comment.status = comment.STATUS_FAILED
        comment.save()
        return

    # Use the tone with the highest likelihood score
    likely_tone = tones[max(tones.keys())]

    # Due to time constraints I'm going to say 'joy' and 'confident' tones are positive
    # and 'anger', 'fear', 'sadness', 'analytical' and 'tentative' are negative.
    comment.is_positive = likely_tone in ['joy', 'confident']
    comment.status = comment.STATUS_ANALYSED
    comment.save()

    log.debug('Comment with id %s analysed successfully', comment.id)
