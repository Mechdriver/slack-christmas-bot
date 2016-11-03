import os
import sys
import time
import random
from datetime import datetime
from slackclient import SlackClient

#Get the ID from the env variable
BOT_ID = os.environ.get("BOT_ID")

AT_BOT = "<@" + BOT_ID + ">"

CHRISTMAS_COMMAND = "christmas"
XMAS_COMMAND = "xmas"

DIE_COMMAND = "no tears now, only dreams"

QUESTION = 'is it'
QUESTION_WHEN = ["when is", "how long"]

HOLIDAYS_LIST = [CHRISTMAS_COMMAND, XMAS_COMMAND]
HOLIDAYS_DATES = {CHRISTMAS_COMMAND: "12/25/2016", XMAS_COMMAND: "12/25/2016"}

DATE_FORMAT = "%m/%d/%Y"
TODAY = time.strftime(DATE_FORMAT)

# start the slack client
slackClient = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))

def messageChannel(response, channel):
   slackClient.api_call("chat.postMessage", channel = channel, text = response, as_user = True)

def handleQuestion(command, channel):
   for holiday in HOLIDAYS_LIST:
      if holiday in command:
         response = "No."

         if TODAY == HOLIDAYS_DATES[holiday]:
            if holiday == XMAS_COMMAND or holiday == CHRISTMAS_COMMAND:
               response = "Yes! Merry Christmas! :christmas_tree:"

         messageChannel(response, channel)

def handleWhen(command, channel):
   for holiday in HOLIDAYS_LIST:
      if holiday in command:
         holidayDate = datetime.strptime(HOLIDAYS_DATES[holiday], DATE_FORMAT)

         dateDiff = holidayDate - datetime.strptime(TODAY, DATE_FORMAT)

         response = "Only " + str(dateDiff.days) + " more days until " + holiday + "!"

         messageChannel(response, channel)

def handleDeath(command, channel):
   responses = ["But why, father?", "Someday, you will die as well."]

   response = responses[random.randrange(0,2)]

   messageChannel(response, channel)
   sys.exit()

'''
Takes in commands and determines what to do with them.
'''
def handleCommand(command, channel):
   if QUESTION in command:
      handleQuestion(command, channel)

   else:
      for when in QUESTION_WHEN:
         if when in command:
            handleWhen(command, channel)

   if DIE_COMMAND in command:
      #Only enable when not hosted.
      #handleDeath(command, channel)

def parseSlackOutput(slackRtmOutput):
   outputList = slackRtmOutput

   if outputList and len(outputList) > 0:
      for output in outputList:
         if output and 'text' in output and AT_BOT in output['text']:
            return output['text'].split(BOT_ID)[1].strip().lower(), output['channel']

   return None, None

if __name__ == '__main__':
   #delay for reading from the firehose
   READ_WEB_SOCKET_DELAY = 1

   if slackClient.rtm_connect():
      print("Ready to ring in the Holidays!")

      while True:
         command, channel = parseSlackOutput(slackClient.rtm_read())

         if command and channel:
            handleCommand(command, channel)
         time.sleep(READ_WEB_SOCKET_DELAY)

   else:
      print("There might be something wrong with my Token or ID.")






