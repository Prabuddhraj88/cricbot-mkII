import os
auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot_prefix = os.environ.get('BOT_PREFIX')
if bot_prefix == None: bot_prefix = "cb "
STATUS_REFRESH_TIME = 10
TRACK_MATCH = os.environ.get('TRACK_MATCH')
arrows_emojis=['⬆️', '⬇️', '➡️', '⬅️', '🔄']
num_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
