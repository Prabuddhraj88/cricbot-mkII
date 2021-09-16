import os
auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot_prefix = os.environ.get('BOT_PREFIX')
if bot_prefix == None: bot_prefix = "cb "
STATUS_REFRESH_TIME = 10
TRACK_MATCH = os.environ.get('TRACK_MATCH')
