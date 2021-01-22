from discord.ext import commands
import discord

class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ########## GENERAL COMMANDS ##########
    @commands.command(name = 'about', pass_context=True, help = 'check out a couple details about clueless-bot')
    async def _about(self, context):
        myEmbed = discord.Embed(
            title = "About clueless-bot",
            url = "https://github.com/cluelesselectrostar/discord_python_bot",
            description = "A couple details about me!",
            color = 0x93CEBA
        )
        myEmbed.add_field(
            name = "Version Code:",
            value = "0.1",
            inline = False
        )
        myEmbed.add_field(
            name = "Date Released:",
            value = "17 Jan 2021",
            inline = False
        )
        myEmbed.add_field(
            name = "GitHub Link:",
            value = "https://github.com/cluelesselectrostar/discord_python_bot",
            inline = False
        )
        myEmbed.set_footer(
            text = "from cluelessyanni"
        )
        myEmbed.set_author(
            name = "Requested by the nosy guy " + context.author.display_name, 
            icon_url = context.author.avatar_url
        )
        myEmbed.set_thumbnail(url="https://og.github.com/mark/github-mark@1200x630.png")

        await context.message.channel.send(embed = myEmbed)

    @commands.command(name = 'ping', pass_context=True, help = 'pong [your crazy thoughts]')
    async def _ping(self, context, *, arg):
        if arg == None:
            await context.message.channel.send('You forgot to include an argument')
        else:
            await context.message.channel.send(str(context.author.mention)+ " " + str(arg))


def setup(bot):
    bot.add_cog(Miscellaneous(bot))