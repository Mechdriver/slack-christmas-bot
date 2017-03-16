# -*- coding: utf-8 -*-

import logging
import random
import time
import sys
import os
from datetime import datetime

logger = logging.getLogger(__name__)

#Set timezone to Pacific
os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()

CHRISTMAS_NAME = "christmas"
XMAS_NAME = "xmas"

DIE_COMMAND = "no tears now, only dreams"

HOLIDAYS_LIST = [CHRISTMAS_NAME, XMAS_NAME]
HOLIDAYS_DATES = {CHRISTMAS_NAME: "12/25/2017", XMAS_NAME: "12/25/2017"}

DATE_FORMAT = "%m/%d/%Y"
DATE_TIME_FORMAT = "%m/%d/%Y %X"

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
        todayDate = time.strftime(DATE_FORMAT)
        negate = negCount % 2 == 1 and negCount > 0
        response = "I don't know. :("

        for holiday in HOLIDAYS_LIST:
            if holiday in command:
                if todayDate == HOLIDAYS_DATES[holiday]:
                    if holiday == XMAS_NAME or holiday == CHRISTMAS_NAME:
                        response = "Yes! Merry Christmas! :christmas_tree:"
                        if negate:
                            response = "No."

                else:
                    response = "No."

                    if negate:
                        response = "Yes."


        self.send_message(response, channelId)

    def handleWhen(self, command, channelId, negCount):
        todayDateTime = time.strftime(DATE_TIME_FORMAT)
        negate = negCount % 2 == 1 and negCount > 0

        for holiday in HOLIDAYS_LIST:
            if holiday in command:
                if negate:
                    response = "Every day except for " + HOLIDAYS_DATES[holiday] + " is not " + holiday + " this year!"

                else:
                    holidayDate = datetime.strptime(HOLIDAYS_DATES[holiday], DATE_FORMAT)

                    dateDiff = holidayDate - datetime.strptime(todayDateTime, DATE_TIME_FORMAT)

                    response = "Only " + str(dateDiff.days) + " more days until " + holiday + "!"

                self.send_message(response, channelId)


    def handleDeath(self, command, channelId):
        responses = ["But why, father?", "Someday, you will die as well.", "Thanks for killing the Holly Daise."]

        response = responses[random.randrange(0,len(responses))]

        self.send_message(response, channelId)
        sys.exit()
