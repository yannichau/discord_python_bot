# Unique token code hiding in a vent!
from token_file import code

import discord
import random
from discord.ext import commands
import pandas as pd
import numpy as np
import pickle

from PIL import Image, ImageDraw, ImageFont
import textwrap

# Print Packages
from tabulate import tabulate
from pprint import pprint

async def fprint(ctx, tab_name, temp_df):
	table_string = tabulate(temp_df, headers='keys', tablefmt='psql')
	await ctx.message.channel.send("""``` {} ```""".format(table_string))

def check_list(name):
	infile = open('tables.pkl','rb')
	tab_list = pickle.load(infile)
	infile.close()
	if name not in tab_list:
		tab_list.append(name)
	outfile = open('tables.pkl','wb')
	pickle.dump(tab_list, outfile)
	outfile.close()

def save_file(df, name):
	df.to_pickle("tables/" + name + ".pkl")

def open_file(name):
	df = pd.read_pickle("tables/" + name + ".pkl")
	# df = pd.read_pickle("tables/" + folder + "/" + name + ".pkl")
	return df

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
	no_category = 'Commands!'
)

class cluelessBot(commands.Bot):

	# FLAGS in each server
	file_dict = dict()
	appending_dict = dict()
	df_dict = dict()

	# TEMP VARIABLES
	file_name = "null"
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
		for guild in client.guilds:
			print(id)
			id = guild.id
			self.file_dict[id] = "null"
			self.appending_dict[id] = False
			self.df_dict[id] = pd.DataFrame()
	
	async def on_disconnect(self):
		general_channel = commands.Bot.get_channel(self, 795339542764585032)
		await general_channel.send(self, 'Bye bye world!')

	async def on_command_error(self, context, error):
		await context.send("Gulp! {}".format(str(error)))
	
	def add_commands(self):

		########## FILE OPERATION COMMANDS ##########			

		@self.command(name = 'create', pass_context=True, help = '[filename] [column names]')
		async def _create(context, *args):
			if len(args) == 0:
				await context.message.channel.send('Command usage: ^create [filename] [column names]')
			else:
				self.appending = True
				self.file_name = str(args[0])
				self.df = pd.DataFrame(columns = args[1:], index = ['null'])
				save_file(self.df[context.guild.id], self.file_name)
				check_list(self.file_name)
				await context.message.channel.send('Created table with name: ' + self.file_name)
				await fprint(context, self.file_name, self.df)

				self.file_dict[context.guild.id] = self.file_name
				self.appending_dict[context.guild.id] = self.appending
				self.df_dict[context.guild.id] = self.df
				     
		@self.command(name = 'open', pass_context=True, help = ' [filename]')
		async def _open(context, *args):
			if len(args) == 0:
				await context.message.channel.send('Command usage: ^open [filename] ')
			elif self.appending_dict[context.guild.id] == False:
				try:
					self.file_name = str(args[0])
					self.df = open_file(self.file_name)
					check_list(self.file_name)
					await context.message.channel.send('📂 You are opening the table ' + self.file_name)
					await fprint(context, self.file_name, self.df)
					self.appending = True

					self.file_dict[context.guild.id] = self.file_name
					self.appending_dict[context.guild.id] = self.appending
					self.df_dict[context.guild.id] = self.df
				except Exception as e:
					await context.message.channel.send('❌ File not found. System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You have a table opened already.')               

		@self.command(name = 'close', pass_context=True, help = '[filename]')
		async def _close(context):
			if self.appending_dict[context.guild.id] == True:
				self.appending_dict[context.guild.id] = False
				save_file(self.df_dict[context.guild.id], self.file_dict[context.guild.id])
				await context.message.channel.send('📂 You have saved and closed the table: ' + self.file_dict[context.guild.id])
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'save', pass_context=True, help = '[filename]')
		async def _save(context):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]

				save_file(self.df, self.file_name)

				self.df_dict[context.guild.id] = self.df 
				await context.message.channel.send('📂 You have saved the table: ' + self.file_name)			
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'print', pass_context=True, help = '[filename]')
		async def _print(context, *, args):
			try:
				self.file_name = str(args)
				self.df = open_file(self.file_name)
				await context.message.channel.send("🖨 Printing the table: " + self.file_name)
				await fprint(context, self.file_name, self.df)
			except Exception as e:
				await context.message.channel.send('❌ File not found. System error: ' + str(e))

		@self.command(name = 'list', pass_context=True, help = 'returns all available tables on my computer!')
		async def _list(context):
			infile = open('tables.pkl','rb')
			tab_list = pickle.load(infile)
			infile.close()
			await context.message.channel.send('📝 List of tables saved on system: ' + str(tab_list))

		########## PANDA COMMANDS ##########

		@self.command(name = 'append', pass_context=True, help = '[row name or index label] [values in order of columns]')
		async def _append(context, *args):
			if self.appending_dict[context.guild.id] == True:
				try:
					self.file_name = self.file_dict[context.guild.id]
					self.appending = self.appending_dict[context.guild.id]
					self.df = self.df_dict[context.guild.id]

					self.df.loc[args[0]] = args[1:]
					save_file(self.df, self.file_name)
					await context.message.channel.send("👇 Appended new row to the table: " + self.file_name)
					await fprint(context, self.file_name, self.df)

					self.df_dict[context.guild.id] = self.df
				except Exception as e:
					await context.message.channel.send('❌ Incorrect number of arguments. You must fill every column of the new row. System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')
		
		@self.command(name = 'appendcol', pass_context=True, help = '[names of columns to be added]')
		async def _appendcol(context, *args):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.appending = self.appending_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]
				try:
					for arg in args:
						self.df[str(arg)] = np.nan
					save_file(self.df, self.file_name)
					await context.message.channel.send("👉🏼 Appended new columns " + str(args) + " to the table: " + self.file_name)
					await fprint(context, self.file_name, self.df)

					self.df_dict[context.guild.id] = self.df
				except Exception as e:
					await context.message.channel.send('❌ System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'appendtotal', pass_context=True, help = 'append total of column to bottom row')
		async def _appendtotal(context):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.appending = self.appending_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]
				try:
					sum_df = self.df.copy()
					cols = sum_df.columns.tolist()
					total = []
					for col in cols:
						sum_df[col] = pd.to_numeric(sum_df[col], errors='coerce')
						total.append(sum_df[col].sum())
					print(total)
					self.df.loc["Sum"] = total
					save_file(self.df, self.file_name)
					await context.message.channel.send("Totals of table: " + self.file_name)
					await fprint(context, self.file_name, self.df)

					self.df_dict[context.guild.id] = self.df
				except Exception as e:
					await context.message.channel.send('❌ System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')
		
		@self.command(name = 'drop', pass_context=True, help = '[names/ indexes of row(s) to remove]')
		async def _drop(context, *args):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.appending = self.appending_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]
				try:
					row_names = list(args)
					self.df = self.df.drop(row_names)
					save_file(self.df, self.file_name)
					await context.message.channel.send("🗑 Deleted rows " + str(row_names) + " from table: " + self.file_name)
					await fprint(context, self.file_name, self.df)

					self.df_dict[context.guild.id] = self.df
				except Exception as e:
					await context.message.channel.send('❌ Rows not found. System error: ' + str(e))
			else:
				await context.message.channel.send('You don\'t have a table opened.')
		
		@self.command(name = 'dropcol', pass_context=True, help = '[names/ indexs of cols(s) to remove]')
		async def _dropcol(context, *args):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.appending = self.appending_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]
				try:
					col_names = list(args)
					self.df = self.df.drop(col_names, axis=1)
					save_file(self.df, self.file_name)
					await context.message.channel.send("🗑  Deleted columns " + str(col_names) + " from table: " + self.file_name)
					await fprint(context, self.file_name, self.df)

					self.df_dict[context.guild.id] = self.df
				except Exception as e:
					await context.message.channel.send('❌ Columns not found. System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'sel', pass_context=True, help = '[selected names of rows to view]')
		async def _sel(context, *args):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.appending = self.appending_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]
				try:
					row_names = list(args)
					await context.message.channel.send("🖨 Printing rows " + str(row_names) + " from table: " + self.file_name)
					await fprint(context, self.file_name, self.df.loc[row_names])
				except Exception as e:
					await context.message.channel.send('❌ Rows not found. System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')    

		@self.command(name = 'selcol', pass_context=True, help = '[selected names of columns to view]')
		async def _selcol(context, *args):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.appending = self.appending_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]
				try:
					col_names = list(args)
					await context.message.channel.send("🖨 Printing columns " + str(col_names) + " from table: " + self.file_name)
					await fprint(context, self.file_name, self.df[col_names])
				except Exception as e:
					await context.message.channel.send('❌ Columns not found. System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')    

		@self.command(name = 'total', pass_context=True, help = 'returns sum of every single cell for each column')
		async def _total(context):
			if self.appending_dict[context.guild.id] == True:
				self.file_name = self.file_dict[context.guild.id]
				self.appending = self.appending_dict[context.guild.id]
				self.df = self.df_dict[context.guild.id]
				try:
					sum_df = self.df.copy()
					cols = sum_df.columns.tolist()
					total = []
					for col in cols:
						sum_df[col] = pd.to_numeric(sum_df[col], errors='coerce')
						total.append(sum_df[col].sum())
					sum_df.loc["Sum"] = total
					await context.message.channel.send("Totals of table: " + self.file_name)
					await fprint(context, self.file_name, sum_df)
				except Exception as e:
					await context.message.channel.send('❌ System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		########## GENERAL COMMANDS ##########
		@self.command(name = 'about', pass_context=True, help = 'check out a couple details about clueless-bot')
		async def _about(context):
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

		@self.command(name = 'ping', pass_context=True, help = 'pong [your crazy thoughts]')
		async def _ping(context, *, arg):
			if arg == None:
				await context.message.channel.send('You forgot to include an argument')
			else:
				await context.message.channel.send(str(context.author.mention)+ " " + str(arg))

# Run Client
client = cluelessBot(command_prefix="^", self_bot=False)
client.run(code)