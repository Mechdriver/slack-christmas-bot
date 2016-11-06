# -*- coding: utf-8 -*-

import logging
import random
import time
import sys
from datetime import datetime

logger = logging.getLogger(__name__)

CHRISTMAS_COMMAND = "christmas"
XMAS_COMMAND = "xmas"

DIE_COMMAND = "no tears now, only dreams"

HOLIDAYS_LIST = [CHRISTMAS_COMMAND, XMAS_COMMAND]
HOLIDAYS_DATES = {CHRISTMAS_COMMAND: "12/25/2016", XMAS_COMMAND: "12/25/2016"}

DATE_FORMAT = "%m/%d/%Y"

class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, msg, channel_id):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def handleQuestion(self, command, channelId, negCount):
        TODAY = time.strftime(DATE_FORMAT)

        if negCount % 2 == 1 and negCount > 0:
            for holiday in HOLIDAYS_LIST:
                if holiday in command:
                    response = "Yes."

                if TODAY == HOLIDAYS_DATES[holiday]:
                    if holiday == XMAS_COMMAND or holiday == CHRISTMAS_COMMAND:
                       response = "No."

            self.send_message(response, channelId)

        else:
            for holiday in HOLIDAYS_LIST:
                if holiday in command:
                    response = "No."

                if TODAY == HOLIDAYS_DATES[holiday]:
                    if holiday == XMAS_COMMAND or holiday == CHRISTMAS_COMMAND:
                       response = "Yes! Merry Christmas! :christmas_tree:"

            self.send_message(response, channelId)

    def handleWhen(self, command, channelId, negCount):
        TODAY = time.strftime(DATE_FORMAT)
        
        if negCount % 2 == 1 and negCount > 0:
            for holiday in HOLIDAYS_LIST:
                if holiday in command:

                    response = "Every day except for " + HOLIDAYS_DATES[holiday] + " is not " + holiday + " this year!"

                    self.send_message(response, channelId)

        else:
            for holiday in HOLIDAYS_LIST:
                if holiday in command:
                    holidayDate = datetime.strptime(HOLIDAYS_DATES[holiday], DATE_FORMAT)

                    dateDiff = holidayDate - datetime.strptime(TODAY, DATE_FORMAT)

                    response = "Only " + str(dateDiff.days) + " more days until " + holiday + "!"

                    self.send_message(response, channelId)


    def handleDeath(self, command, channelId):
        responses = ["But why, father?", "Someday, you will die as well.", "Thanks for killing the Holly Daise."]

        response = responses[random.randrange(0,len(responses))]

        self.send_message(response, channelId)
        sys.exit()
