import util, discord, json, datetime
from discord.ext import commands, tasks

class loop(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.watch.start()

#============================================================================================================#

    def cog_unload(self):
        self.watch.cancel()

#============================================================================================================#

    @tasks.loop(seconds=5.0) # DAUER UMSTELLEN
    async def watch(self):
        util.log("LOOP", "Beginn")
        # Import
        try:
            file_rekrutenjson = open("/var/www/html/bots/rekrut/rekruten.json", "r")
            rekrutenjson = file_rekrutenjson.read()
            file_rekrutenjson.close()
            rekrutendict = json.loads(rekrutenjson)
            copy_rekrutendict = json.loads(rekrutenjson)
        except Exception as e:
            util.log("LOOP", "Error: " + str(e))
        # Edit
        for rekrut, timer in copy_rekrutendict.items():
            timer = datetime.datetime.strptime(timer, '%Y-%m-%d %H:%M:%S.%f')
            if(datetime.datetime.now() > timer):
                try:
                    myguild = self.client.get_guild(692526341987369021) # ID ÄNDERN
                    rolle_rekrut = myguild.get_role(706147399587987496) # ID ÄNDERN
                    rolle_soldat = myguild.get_role(706147419783692308) # ID ÄNDERN
                    member = myguild.get_member(int(rekrut))
                    await member.remove_roles(rolle_rekrut)
                    await member.add_roles(rolle_soldat)
                except Exception as e:
                    util.log("LOOP", "Error: " + str(e))
                    return
                kanal = myguild.get_channel(692549958834061373) # ID ÄNDERN
                await kanal.send("{} (``{}``) ist nun ein Soldat.".format(member.mention, rekrut))
                util.log("REKRUTEN", "``{}`` (``{}``) ist nun ein Soldat.".format(member, rekrut))
                rekrutendict.pop("{}".format(rekrut))
        # Export
        rekrutenjson = json.dumps(rekrutendict)
        file_rekrutenjson = open("/var/www/html/bots/rekrut/rekruten.json", "w")
        file_rekrutenjson.write(rekrutenjson)
        file_rekrutenjson.close()
        util.log("LOOP", "Abschluss")

#============================================================================================================#

    @watch.before_loop
    async def before_loop(self):
        util.log("LOOP", "Wating until ready...")
        await self.client.wait_until_ready()

#============================================================================================================#

def setup(client):
    client.add_cog(loop(client))
    util.log("Initialized loop")
