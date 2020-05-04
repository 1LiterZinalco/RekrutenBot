import util, discord, datetime, json, asyncio
from discord.ext import commands

class interface(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

#============================================================================================================#

    @commands.command()
    async def status(self, ctx):
        embed=discord.Embed(title="Status")
        embed.add_field(name="ClientUser", value=str(self.client.user), inline=True)
        embed.add_field(name="Websocket Gateway", value=str(self.client.ws), inline=True)
        embed.add_field(name="Latency", value=str(self.client.latency), inline=True)
        await ctx.send(embed=embed)

#============================================================================================================#

    @commands.command()
    async def rekrut(self, ctx, *args):
        if(len(args) != 1):
            await ctx.send(":warning: Du verwendest eine falsche Syntax: `!rekrut <@Erwähnung, Name oder ID des neuen Rekruten>`")
            return
        if(args[0].isnumeric() == True):
            # User ID was given
            neuer_rekrut = ctx.message.guild.get_member(int(args[0]))
            if(neuer_rekrut == None):
                await ctx.send(":warning: Ich konnte kein Servermitglied mit der ID ``{}`` finden.".format(args[0]))
                return
        else:
            neuer_rekrut = ctx.message.guild.get_member_named(args[0])
            if(neuer_rekrut == None):
                try:
                    neuer_rekrut = ctx.message.mentions[0]
                except:
                    await ctx.send(":warning: Ich konnte kein Servermitglied namens ``{}`` finden. Überprüfe die Schreibweise (Namen, die ein Leerzeichen beinhalten müssen in Anführungszeichen stehen) oder versuche es mit `Username#Zahl` *(z.B. 1LiterZinalco#0001)* oder der eindeutigen ID *(<https://cutt.ly/Fyja78Y>)*".format(args[0]))
                    return

        # Importing existing
        try:
            file_rekrutenjson = open("/var/www/html/bots/rekrut/rekruten.json", "r")
            rekrutenjson = file_rekrutenjson.read()
            file_rekrutenjson.close()
            rekrutendict = json.loads(rekrutenjson)
        except:
            rekrutendict = {}
        # Add new
        rekrutendict[neuer_rekrut.id] = "{}".format(str(datetime.datetime.now() + datetime.timedelta(seconds=30))) # DAUER UMSTELLEN
        # Export
        rekrutenjson = json.dumps(rekrutendict)
        file_rekrutenjson = open("/var/www/html/bots/rekrut/rekruten.json", "w")
        file_rekrutenjson.write(rekrutenjson)
        file_rekrutenjson.close()
        kanal = ctx.message.guild.get_channel(692549958834061373) # ID ÄNDERN
        rolle_rekrut = ctx.message.guild.get_role(706147399587987496) # ID ÄNDERN
        await neuer_rekrut.add_roles(rolle_rekrut)
        await kanal.send("{} (``{}``) beginnt nun die 30-tägige Phase als Rekrut.".format(neuer_rekrut.mention, neuer_rekrut.id))
        util.log("REKRUTEN", "``{}`` (``{}``) beginnt nun die 30-tägige Phase als Rekrut.".format(neuer_rekrut, neuer_rekrut.id))
        await ctx.message.add_reaction("✅")

#============================================================================================================#

def setup(client):
    client.add_cog(interface(client))
    util.log("Initialized interface")
