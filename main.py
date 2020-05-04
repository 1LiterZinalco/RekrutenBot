import util, os, discord, dotenv
from discord.ext import commands
from dotenv import load_dotenv

##############################################################################################################
### Initial stuff ############################################################################################
##############################################################################################################

# Startup
util.log("STARTUP...")
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
client = commands.Bot(command_prefix = "!")

# Removing the standard "help" command
client.remove_command("help")

# Loading Cogs:
client.load_extension("cogs.sentry")
client.load_extension("cogs.interface")
client.load_extension("cogs.loop")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="PlanetSide 2"))

# Starting the Bot
util.log("STARTUP CLEAR, RUNNING BOT")
client.run(TOKEN)
