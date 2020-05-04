import util, discord
from discord.ext import commands

class sentry(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

#============================================================================================================#

    # Handling Messages
    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        channel = message.channel

        try: # Channel is channel
            channel_name = channel.name
            channel_id = str(channel.id)
        except: # Channel is dm with user
            channel_name = "Direct Message with " + str(channel.recipient)
            channel_id = str(channel.recipient.id)

        if(int(author.id) == 706086027542134816):
            util.log("BOT", "@ {} ({}) 💬 {}".format(channel_name, channel_id, message.content))
        elif(message.content.startswith("!")):
            util.log("COMMAND", "{} ({}) @ {} ({}) 💬 {}".format(str(author), str(author.id), channel_name, channel_id, message.content))
        else:
            pass

#============================================================================================================#

def setup(client):
    client.add_cog(sentry(client))
    util.log("Initialized sentry")
