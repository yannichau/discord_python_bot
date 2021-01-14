import discord
import random
from discord.ext import commands
import pandas as pd
import pickle

# Print Packages
from tabulate import tabulate
from pprint import pprint

async def fprint(ctx, tab_name, temp_dt):
    table_string = tabulate(temp_dt.transpose(), headers='keys', tablefmt='psql')
    await ctx.message.channel.send("""```{}```""".format(table_string))

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands!'
)

class cluelessBot(commands.Bot):

    # FLAGS
    file_name = 'null'
    new_entry = False
    appending = False
    df = pd.DataFrame()

    ########## INITIALISE and EVENTS ##########
    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
        self.message1 = "[INFO]: Bot now online"
        self.message2 = "Bot still online"
        self.add_commands()
        self.help_command =  help_command

    async def on_ready(self):
        print(self.message1)
        await commands.Bot.change_presence(
            self,
            status=discord.Status.online,
            activity=discord.Game('you are clueless')
        )
    
    async def on_disconnect(self):
        general_channel = commands.Bot.get_channel(self, 795339542764585032)
        await general_channel.send(self, 'Bye bye world!')

    def add_commands(self):
        ########## FILE OPERATION COMMANDS ##########

        @self.command(name = 'create', pass_context=True, help = '[filename] [column names]')
        async def _create(context, *args):
            if len(args) == 0:
                await context.message.channel.send('Command usage: ^create [filename] [column names]')
            else:
                self.appending = True
                self.file_name = str(args[0])
                keys = args[1:]
                self.df = pd.DataFrame({'keys': keys})
                self.df.set_index('keys', inplace=True)
                self.df.to_pickle(self.file_name + ".pkl")
                await context.message.channel.send('Created table with name: ' + self.file_name)
                await fprint(context, self.file_name, self.df)     

        @self.command(name = 'open', pass_context=True, help = ' [filename]')
        async def _open(context, *, arg):
            if arg == None:
                await context.message.channel.send('Command usage: ^open [filename] ')
            elif self.appending == False:
                try:
                    self.file_name = str(arg)
                    self.appending = True
                    self.df = pd.read_pickle(self.file_name + '.pkl')
                    await context.message.channel.send('You are opening the table ' + self.file_name)
                    await fprint(context, self.file_name, self.df)
                except Exception as e:
                    await context.message.channel.send('File not found. System error: ' + str(e))
            else:
                await context.message.channel.send('You have a table opened already.')               

        @self.command(name = 'close', pass_context=True, help = '[filename]')
        async def _close(context):
            if self.appending == True:
                self.appending = False
                self.df.to_pickle(self.file_name + ".pkl")
                await context.message.channel.send('You have saved and closed the table: ' + self.file_name)
            else:
                await context.message.channel.send('You don\'t have a table opened.')

        @self.command(name = 'save', pass_context=True, help = '[filename]')
        async def _save(context):
            if self.appending == True:
                self.df.to_pickle(self.file_name + ".pkl")
                await context.message.channel.send('You have saved the table: ' + self.file_name)
            else:
                await context.message.channel.send('You don\'t have a table opened.')

        @self.command(name = 'print', pass_context=True, help = '[filename]')
        async def _print(context, *, args):
            try:
                self.file_name = str(args)
                self.df = pd.read_pickle(self.file_name + '.pkl')
                await context.message.channel.send("Printing the table: " + self.file_name)
                await fprint(context, self.file_name, self.df)
            except Exception as e:
                await context.message.channel.send('File not found. System error: ' + str(e))

        ########## PANDA COMMANDS ##########

        @self.command(name = 'append', pass_context=True, help = ' [row_key] [values in order]')
        async def _append(context, *args):
            if self.appending == True:
                self.df[str(args[0])] = args[1:]
                self.df.to_pickle(self.file_name + ".pkl")
                await context.message.channel.send("Appended new row to the table: " + self.file_name)
                await fprint(context, self.file_name, self.df)
            else:
                await context.message.channel.send('You don\'t have a table opened.')

        ########## GENERAL COMMANDS ##########
        @self.command(name = 'version', pass_context=True, help = 'duh!')
        async def _version(context):
            myEmbed = discord.Embed(
                title = "Current Version",
                description = "The bot is in version 1.0",
                color = 0x00ff00
            )
            myEmbed.add_field(
                name = "Version Code:",
                value = "1.0",
                inline = False
            )
            myEmbed.add_field(
                name = "Date Released:",
                value = "7 Jan 2021",
                inline = False
            )
            myEmbed.set_footer(
                text = "from clueless"
            )
            myEmbed.set_author(
                name = "cluelessyanni"
            )
            await context.message.channel.send(embed = myEmbed)

        @self.command(name = 'ping', pass_context=True, help = 'echoes your crazy voice')
        async def _ping(context, *, arg):
            if arg == None:
                await context.message.channel.send('You forgot to include an argument')
            else:
                await context.message.channel.send(str(context.author.mention)+ " " + str(arg))

# Run Client
client = cluelessBot(command_prefix="^", self_bot=False)
client.run('Nzk2NTg3OTU5MTYzMjg5NjIw.X_aGWQ._8sHavOJ_C77wPAiZz3ixQZ9nwQ')