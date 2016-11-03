import os
from slackclient import SlackClient

BOT_NAME = "holidaybot"

slackclient = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == "__main__":
   apiCall = slackclient.api_call("users.list")

   if apiCall.get('ok'):

      #get all users so we can see if our bot is in this list.
      users = apiCall.get('members')

      for user in users:
         if 'name' in user and user.get('name') == BOT_NAME:
            print ("Bot ID for '" + user.get('name') + "' is " + user.get('id'))

   else:
      print ("Could not find user with the name: " + BOT_NAME)