import json
import logging
import re

logger = logging.getLogger(__name__)

QUESTION = 'is it'
QUESTION_WHEN = ["when is", "how long", "how many days"]

DIE_COMMAND = "no tears now, only dreams"

class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):

            command = event['text']
            channel = event['channel']

            if QUESTION in command:
                self.msg_writer.handleQuestion(command, channel)

            else:
                for when in QUESTION_WHEN:
                    if when in command:
                        self.msg_writer.handleWhen(command, channel)

            if DIE_COMMAND in command:
                #Only enable when not hosted.
                #self.msg_writer.handleDeath(command, channel)
