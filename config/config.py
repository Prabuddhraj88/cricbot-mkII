import os
auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot_prefix = os.environ.get('BOT_PREFIX')
if bot_prefix == None: bot_prefix = "cb "
