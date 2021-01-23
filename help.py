from discord.ext import commands
import discord

fileop_list = [
    {
        "name": "close",
        "arguments": "",
        "description": "📁save and close the current table",
    },
    {
        "name": "create",
        "arguments": "",
        "description": "🆕 create a new table",
    },
    {
        "name": "list",
        "arguments": "[filename]",
        "description": "📖 list all tables on the server",
    },{
        "name": "open",
        "arguments": "[filename]",
        "description": "📂 open a previously created table",
    },{
        "name": "print",
        "arguments": "[filename]",
        "description": "🖨 print in a tabular format",
    },{
        "name": "redo",
        "arguments": "",
        "description": "⏩ reverse undo",
    },{
        "name": "renamefile",
        "arguments": "[old filename] [new filename]",
        "description": "📝 rename table",
    },{
        "name": "save",
        "arguments": "[filename]",
        "description": "🗃 save changes to current table",
    },{
        "name": "undo",
        "arguments": "",
        "description": "⏪ revert up to last 10 changes",
    },
]

trash_list = [
    {
        "name": "recycle",
        "arguments": "[filename]",
        "description": "♻️ retrieve a table from trash list",
    },
        {
        "name": "trash",
        "arguments": "[filename]",
        "description": "🗑 send table to trash",
    },
        {
        "name": "trashlist",
        "arguments": "",
        "description": "📝 list all tables in trash list",
    },
]

misc_list = [
    {
        "name": "about",
        "arguments": "",
        "description": "🐼 read about Panxcel",
    },
        {
        "name": "help",
        "arguments": "[optional: command]",
        "description": "❓ shows the help message",
    },
        {
        "name": "ping",
        "arguments": "[your crazy thoughts]",
        "description": "🏓 pong your crazy thoughts",
    },
]

panda_list = [
    {
        "name": "append",
        "arguments": "[row] [values in all cols]",
        "description": "+ append a new row with all cols filled",
    },
        {
        "name": "appendcol",
        "arguments": "[cols]",
        "description": "++ append new empty col(s)",
    },
        {
        "name": "drop",
        "arguments": "<-c/-r> [cols/rows]",
        "description": "🚮 drop specified col(s) or row(s)",
    },
    {
        "name": "rename",
        "arguments": "<-c/-r> [old col/row] [new col/row]",
        "description": "🖊 rename specified col or row",
    },
    {
        "name": "sel",
        "arguments": "<-c/-r> [cols/rows]",
        "description": "👉🏼 view selected col(s) or row(s)",
    },
        {
        "name": "sort",
        "arguments": "<-c/-r> [cols/rows]",
        "description": "🎲 sort table by selected col or row",
    },
        {
        "name": "total",
        "arguments": "<-a> ",
        "description": "🧮 compute totals for each col. <-a> to append total row to bottom of table",
    },
]

all_list = fileop_list + trash_list + misc_list + panda_list

def create_help_list(cmd_list):
    output_string = ""
    for item in cmd_list:
        cmd = """```{} {} ```{}""".format(item['name'], item['arguments'], item['description'])
        temp = (output_string, cmd)
        output_string = "\n \n".join(temp)
    return output_string

fileop_dict = create_help_list(fileop_list)
panda_dict  = create_help_list(panda_list)
trash_dict = create_help_list(trash_list)
misc_dict = create_help_list(misc_list)

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ########## GENERAL COMMANDS ##########
    @commands.command(name = 'help', pass_context=True)
    async def _help(self, context, *args):
        if len(args) == 0:
            Embed1 = discord.Embed(
                title = "Help 1: Table Manipulations 📝",
                url = "https://github.com/cluelesselectrostar/discord_python_bot",
                description = "-c or -r are optional arguments to force operation on column/ row",
                color = 0x93CEBA
            )
            for item in panda_list:
                Embed1.add_field(
                    name = """```{} {}```""".format(item["name"], item["arguments"]),
                    value = item["description"],
                    inline = False
                )
            Embed1.set_footer(
                text = """Type ^help [command] to check out more details
Page 1/4"""
            )
            await context.message.channel.send(embed = Embed1)

            Embed2 = discord.Embed(
                title = "Help 2: File Operations 🗄",
                url = "https://github.com/cluelesselectrostar/discord_python_bot",
                color = 0x93CEBA
            )
            for item in fileop_list:
                Embed2.add_field(
                    name = """```{} {}```""".format(item["name"], item["arguments"]),
                    value = item["description"],
                    inline = False
                )
            Embed2.set_footer(
                text = """Type ^help [command] to check out more details
Page 2/4"""
            )
            await context.message.channel.send(embed = Embed2) 

            Embed3 = discord.Embed(
                title = "Help 3: Deal with Trash 🗑",
                url = "https://github.com/cluelesselectrostar/discord_python_bot",
                color = 0x93CEBA
            )
            for item in trash_list:
                Embed3.add_field(
                    name = """```{} {}```""".format(item["name"], item["arguments"]),
                    value = item["description"],
                    inline = False
                )
            Embed3.set_footer(
                text = """Type ^help [command] to check out more details
Page 3/4"""
            )
            await context.message.channel.send(embed = Embed3)

            Embed4 = discord.Embed(
                title = "Help 4: Miscellaneous Operations 😆",
                url = "https://github.com/cluelesselectrostar/discord_python_bot",
                color = 0x93CEBA
            )
            for item in trash_list:
                Embed4.add_field(
                    name = """```{} {}```""".format(item["name"], item["arguments"]),
                    value = item["description"],
                    inline = False
                )
            Embed4.set_footer(
                text = """Type ^help [command] to check out more details
Page 4/4"""
            )
            await context.message.channel.send(embed = Embed4) 

        else:
            print("trying to find command")
            cmd = args[0]
            cmd_dict = dict()

            for item in all_list:
                if item['name'] == cmd:
                    cmd_dict = item
                    break

            if cmd_dict == dict():
                await context.message.channel.send("🙅‍♂️ This command does not exist.") 
            else:
                Embed3 = discord.Embed(
                    title = "Help for command ^" + cmd,
                    url = "https://github.com/cluelesselectrostar/discord_python_bot",
                    description = """```^{} {}```
{}""".format(item["name"], item["arguments"], item["description"]),
                    color = 0x93CEBA
                )
                Embed3.set_footer(
                    text = """Type ^help to check out all commands.
If applicable, -c or -r are optional arguments to force operation on column/ row"""
                )
                await context.message.channel.send(embed = Embed3) 


def setup(bot):
    bot.add_cog(Help(bot))