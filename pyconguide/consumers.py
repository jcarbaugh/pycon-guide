import logging
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.conf import settings
from .models import Interest, Presentation

logger = logging.getLogger('ws')


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group(f'user-{message.user.username}').add(message.reply_channel)


@channel_session_user
def ws_message(message):
    msg = message.content.get('text')
    action, presentation_id = msg.split(':')

    if action == 'disinterested':

        interest = Interest.objects.get(
            user=message.user,
            presentation__presentation_id=int(presentation_id),
            presentation__pycon__year=settings.PYCON_YEAR)
        interest.delete()

        resp = {'text': 'success'}
        Group(f'user-{message.user.username}').send({'text': msg})

    elif action == 'interested':

        presentation = Presentation.objects.get(
            presentation_id=int(presentation_id),
            pycon__year=settings.PYCON_YEAR)
        Interest.objects.create(
            user=message.user, presentation=presentation)

        resp = {'text': 'success'}
        Group(f'user-{message.user.username}').send({'text': msg})

    else:
        resp = {'text': 'failure'}
    message.reply_channel.send(resp)


@channel_session_user
def ws_disconnect(message):
    Group(f'user-{message.user.username}').discard(message.reply_channel)
