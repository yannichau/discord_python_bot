# Unique token code hiding in a vent!
from token_file import code

import discord
import random
from discord.ext import commands
import pandas as pd
import numpy as np
import pickle
import os
from collections import defaultdict

# Print Packages
from tabulate import tabulate

# Print Table
async def fprint(ctx, tab_name, temp_df):
	table_string = tabulate(temp_df, headers='keys', tablefmt='psql')
	await ctx.message.channel.send("""``` {}
{} ```""".format(tab_name, table_string))

# Manipulate tables.pkl or trash_index.pkl
def list_drop(path, item):
	infile = open(path,'rb')
	tab_list = pickle.load(infile)
	infile.close()
	tab_list.remove(item)
	outfile = open(path,'wb')
	pickle.dump(tab_list, outfile)
	outfile.close()

def list_append(path, item):
	infile = open(path,'rb')
	tab_list = pickle.load(infile)
	infile.close()
	tab_list.append(item)
	outfile = open(path,'wb')
	pickle.dump(tab_list, outfile)
	outfile.close()

# Check if there's already a file with the same name.
def file_exists(ID, name):
	list_path = 'tables/' + str(ID) + '/tables.pkl'
	trash_path = 'tables/' + str(ID) + '/trash/trash_index.pkl'
	list_file = open(list_path,'rb')
	trash_file = open(trash_path,'rb')
	tab_list = pickle.load(list_file)
	trash_list = pickle.load(trash_file)
	if name in tab_list or name in trash_list:
		return True
	else:
		return False

# Save Table
def save_file(df, folder, name):
	df.to_pickle("tables/" + str(folder) + "/" + name + ".pkl")

# Open Table 
def open_file(folder, name):
	df = pd.read_pickle("tables/" + str(folder) + "/" + name + ".pkl")
	return df

# Append to table's file history
def dict_append(df_dict, df):
	if len(df_dict) == 10:
		df_dict.pop(0)
	df_dict.append(df)
	print(str(df_dict))
	return df_dict

class cluelessBot(commands.Bot):

	# FLAGS in each server
	file_dict = dict()          # Name of table currently being accessed in each server
	appending_dict = dict()     # Appending status of each server
	df_dict = defaultdict(list) # Table currently being accessed in each server

	# TEMP VARIABLES
	file_name = "null"
	appending = False
	df = pd.DataFrame()
	ID = 0

	########## INITIALISE and EVENTS ##########
	def __init__(self, command_prefix, self_bot):
		commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)
		self.message1 = "[INFO]: Panxcel is now online"
		self.add_commands()

	async def on_ready(self):
		print(self.message1)
		for guild in client.guilds:
			self.ID = guild.id
			newpath = "tables/" + str(self.ID)
			trashpath = "tables/" + str(self.ID) + "/trash"

			# Initialise folder for server: list of tables, and folder for trash
			if not os.path.exists(newpath):

				self.file_dict[self.ID] = "null"
				self.appending_dict[self.ID] = False
				# self.df_dict[self.ID] = []

				os.makedirs(newpath)
				os.makedirs(trashpath)

				# Create Table List
				temp_list = []
				temp_list.append("null")
				tablist_file = open('tables/' + str(self.ID) + '/tables.pkl','wb')
				pickle.dump(temp_list, tablist_file)
				tablist_file.close()

				# Create Trash List
				trashlist_file = open('tables/' + str(self.ID) + '/trash/trash_index.pkl','wb')
				pickle.dump(temp_list, trashlist_file)
				trashlist_file.close()
				print("Initialised empty table list and empty trash list for " + str(self.ID))

	async def on_guild_join(self, guild):
		for guild in client.guilds:
			self.ID = guild.id
			newpath = "tables/" + str(self.ID)
			trashpath = "tables/" + str(self.ID) + "/trash"

			# Initialise folder for server: list of tables, and folder for trash
			if not os.path.exists(newpath):

				self.file_dict[self.ID] = "null"
				self.appending_dict[self.ID] = False
				# self.df_dict[self.ID] = []

				os.makedirs(newpath)
				os.makedirs(trashpath)

				# Create Table List
				temp_list = []
				temp_list.append("null")
				tablist_file = open('tables/' + str(self.ID) + '/tables.pkl','wb')
				pickle.dump(temp_list, tablist_file)
				tablist_file.close()

				# Create Trash List
				trashlist_file = open('tables/' + str(self.ID) + '/trash/trash_index.pkl','wb')
				pickle.dump(temp_list, trashlist_file)
				trashlist_file.close()
				print("Initialised empty table list and empty trash list for " + str(self.ID))

	async def on_command_error(self, context, error):
		await context.send("Gulp! {}".format(str(error)))
	
	def add_commands(self):

		########## FILE OPERATION COMMANDS ##########			

		@self.command(name = 'create', pass_context=True, help = '[filename] [column names]')
		async def _create(context, *args):
			self.ID = context.guild.id
			if len(args) == 0:
				await context.message.channel.send('Command usage: ^create [filename] [column names]')
			elif file_exists(self.ID, args[0]):
				await context.message.channel.send('👯‍♂️ There is already a file with the same name.')
			else:
				self.appending = True
				self.file_name = str(args[0])
				self.df = pd.DataFrame(columns = args[1:], index = ['null'])
				list_append('tables/' + str(self.ID) + '/tables.pkl', self.file_name)	
				save_file(self.df, self.ID, self.file_name)
				await context.message.channel.send('Created table with name: ' + self.file_name)
				await fprint(context, self.file_name, self.df)

				# Amend flags
				self.file_dict[self.ID] = self.file_name
				self.appending_dict[self.ID] = self.appending
				self.df_dict[self.ID] = dict_append(self.df_dict[self.ID], self.df)
				     
		@self.command(name = 'open', pass_context=True, help = ' [filename]')
		async def _open(context, *args):
			if len(args) == 0:
				await context.message.channel.send('Command usage: ^open [filename] ')
			else:
				try:
					self.ID = context.guild.id
					self.file_name = str(args[0])
					self.df = open_file(self.ID, self.file_name)
					list_append('tables/' + str(self.ID) + '/trash/trash_index.pkl', self.file_name)	
					await context.message.channel.send('📂 You are opening the table ' + self.file_name)
					await fprint(context, self.file_name, self.df)
					self.appending = True

					# Amend flags
					self.file_dict[self.ID] = self.file_name
					self.appending_dict[self.ID] = self.appending
					print("amended appending flag")
					self.df_dict[self.ID] = dict_append(self.df_dict[self.ID], self.df)
				except Exception as e:
					await context.message.channel.send('❌ File not found. System error: ' + str(e))             

		@self.command(name = 'close', pass_context=True, help = 'close currently opened file')
		async def _close(context):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				self.appending_dict[self.ID] = False
				save_file(self.df, self.ID, self.file_dict[self.ID])
				await context.message.channel.send('📂 You have saved and closed the table: ' + self.file_dict[self.ID])
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'save', pass_context=True, help = '[filename]')
		async def _save(context):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				save_file(self.df, self.ID, self.file_dict[self.ID])
				await context.message.channel.send('📂 You have saved the table: ' + self.file_dict[self.ID])			
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'undo', pass_context=True, help = 'undo action.')
		async def _undo(context):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				self.file_name = self.file_dict[self.ID]
				
				if len(self.df_dict[self.ID]) == 1:
					await context.message.channel.send('🤚 You do not have anything (or anything left) to undo.')
				else:
					newest = self.df_dict[self.ID][-1]
					self.df_dict[self.ID].insert(0, newest)
					self.df_dict[self.ID].pop(-1)
					self.df = self.df_dict[self.ID][-1]
					await context.message.channel.send('⏪ Undo performed.')
					await fprint(context, self.file_name, self.df)
					save_file(self.df, self.ID, self.file_dict[self.ID])
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')
		
		#TODO: Determine redo/ undo depth
		@self.command(name = 'redo', pass_context=True, help = 'redo action.')
		async def _redo(context):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				self.file_name = self.file_dict[self.ID]
				
				if len(self.df_dict[self.ID]) == 1:
					await context.message.channel.send('🤚 You do not have anything (or anything left) to redo.')
				else:
					oldest = self.df_dict[self.ID][0]
					self.df_dict[self.ID].append(oldest)
					self.df_dict[self.ID].pop(0)
					self.df = self.df_dict[self.ID][-1]
					await context.message.channel.send('⏩ Redo performed.')
					await fprint(context, self.file_name, self.df)
					save_file(self.df, self.ID, self.file_dict[self.ID])
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')
		
		@self.command(name = 'print', pass_context=True, help = '[filename]')
		async def _print(context, *args):
			try:
				self.file_name = str(args[0])
				self.df = open_file(context.guild.id, self.file_name)
				await context.message.channel.send("🖨 Printing the table: " + self.file_name)
				await fprint(context, self.file_name, self.df)
			except Exception as e:
				await context.message.channel.send('❌ File not found. System error: ' + str(e))

		@self.command(name = 'list', pass_context=True, help = 'returns all available tables on my computer!')
		async def _list(context):
			try:
				infile = open('tables/' + str(context.guild.id) + '/tables.pkl','rb')
				tab_list = pickle.load(infile)
				infile.close()
				await context.message.channel.send('📝 List of tables saved on system: ' + str(tab_list))
			except Exception as e:
				await context.message.channel.send('❌ System error: ' + str(e))

		@self.command(name = 'renamefile', pass_context=True, help = '[old filename] [new filename]', cog_name = 'file operation')
		async def _renamefile(context, *args):
			self.ID = context.guild.id
			try:
				if len(args) != 2:
					await context.message.channel.send('❌ Command usage: ^rename [old_name] [new_name]')
				else:
					# Rename in file system
					folder = str(self.ID)
					old_file = str(args[0])
					new_file = str(args[1])
					os.rename("tables/" + folder + "/" + old_file + ".pkl", "tables/" + str(self.ID) + "/" + new_file + ".pkl")
					
					# Rename in tables.pkl
					list_drop('tables/' + folder + '/tables.pkl', old_file)
					list_append('tables/' + folder + '/tables.pkl', new_file)		
					await context.message.channel.send('🖋 Renamed the table ' + old_file + ' to ' + new_file)
			except Exception as e:
				await context.message.channel.send('❌ File not found . System error: ' + str(e))

		@self.command(name = 'trashlist', pass_context=True, help = 'lists all files deleted')
		async def _trashlist(context):
			try:
				infile = open('tables/' + str(context.guild.id) + '/trash/trash_index.pkl','rb')
				trash_list = pickle.load(infile)
				infile.close()
				await context.message.channel.send('🚮 Trash list: ' + str(trash_list))
			except Exception as e:
				await context.message.channel.send('❌ System error: ' + str(e))
		
		@self.command(name = 'trash', pass_context=True, help = '[filename]')
		async def _trash(context, *args):
			try:
				if len(args) < 1:
					await context.message.channel.send('❌ Command usage: ^trash [file_name]')
				else:
					# Rename in file system
					folder = str(context.guild.id)
					f_name = str(args[0])
					os.rename("tables/" + folder + "/" + f_name + ".pkl", "tables/" + folder + "/trash/" + f_name + ".pkl")
					
					# Remove from tables.pkl, add to trash_index.pkl
					list_drop('tables/' + folder + '/tables.pkl', f_name)
					list_append('tables/' + folder + '/trash/trash_index.pkl', f_name)		
					await context.message.channel.send('😢 Table ' + f_name + ' sent to trash.')				
			except Exception as e:
				await context.message.channel.send('❌ File not found . System error: ' + str(e))		
		
		@self.command(name = 'recycle', pass_context=True, help = '[filename]')
		async def _recycle(context, *args):
			try:
				if len(args) < 1:
					await context.message.channel.send('❌ Command usage: ^trash [file_name]')
				else:
					# Rename in file system
					folder = str(context.guild.id)
					f_name = str(args[0])
					os.rename("tables/" + str(context.guild.id) + "/trash/" + f_name + ".pkl", "tables/" + folder + "/" + f_name + ".pkl")
					
					# Remove from trash_index.pkl, add to tables.pkl
					list_drop('tables/' + folder + '/trash/trash_index.pkl', f_name)
					list_append('tables/' + folder + '/tables.pkl', f_name)
					await context.message.channel.send('♻️ You\'ve picked up ' + f_name + ' from trash.')						
			except Exception as e:
				await context.message.channel.send('❌ File not found in trash. System error: ' + str(e))	

		########## PANDA COMMANDS ##########

		@self.command(name = 'append', pass_context=True, help = '[row name or index label] [values in order of columns]')
		async def _append(context, *args):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				try:
					self.file_name = self.file_dict[self.ID]
					self.appending = self.appending_dict[self.ID]
					self.df = self.df_dict[self.ID][-1]

					self.df.loc[args[0]] = args[1:]

					save_file(self.df, self.ID, self.file_name)
					await context.message.channel.send("👇 Appended new row to the table: " + self.file_name)
					await fprint(context, self.file_name, self.df)
					self.df_dict[self.ID] = dict_append(self.df_dict[self.ID], self.df)
				except Exception as e:
					await context.message.channel.send('❌ Incorrect number of arguments. You must fill every column of the new row. System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')
		
		@self.command(name = 'appendcol', pass_context=True, help = '[names of columns to be added]')
		async def _appendcol(context, *args):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				self.file_name = self.file_dict[self.ID]
				self.appending = self.appending_dict[self.ID]
				self.df = self.df_dict[self.ID][-1]
				try:
					for arg in args:
						self.df[str(arg)] = np.nan
					save_file(self.df, self.ID, self.file_name)
					await context.message.channel.send("👉🏼 Appended new columns " + str(args) + " to the table: " + self.file_name)
					await fprint(context, self.file_name, self.df)

					self.df_dict[self.ID] = dict_append(self.df_dict[self.ID], self.df)
				except Exception as e:
					await context.message.channel.send('❌ System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'drop', pass_context=True, help = '[optional: -c/-r] [names of rows/cols to remove]')
		async def _drop(context, *args):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				# Import Files
				self.file_name = self.file_dict[self.ID]
				self.df = self.df_dict[self.ID][-1]

				# By default second and onward arguments are names
				names = list(args).pop(0)
				error = False
				stype = "unknown"

				# Delete depending on -c, -r or guess
				if args[0] == "-c": # drop columns
					try:
						self.df = self.df.drop(names, axis=1)
						stype = "columns"
					except Exception as e:
						error = True
						await context.message.channel.send('❌ Columns not found. System error: ' + str(e))
				elif args[0] == "-r": # drop rows
					try:
						self.df = self.df.drop(names)
						stype = "rows"
					except Exception as e:
						error = True
						await context.message.channel.send('❌ Rows not found. System error: ' + str(e))
				else: # guess drop columns or rows
					names = list(args)
					try:
						self.df = self.df.drop(names, axis=1)
						stype = "columns"
					except Exception as e:
						try:
							self.df = self.df.drop(names)
							stype = "rows"
						except Exception as e:
							error = True
							await context.message.channel.send('❌ Columns or rows not found. System error: ' + str(e))

				# Save and print if no errors
				if error == False:
					save_file(self.df, self.ID, self.file_name)
					await context.message.channel.send("🗑 Deleted " + stype + " " + str(names) + " from table: " + self.file_name)
					await fprint(context, self.file_name, self.df)
					self.df_dict[self.ID] = dict_append(self.df_dict[self.ID], self.df)
			else:
				await context.message.channel.send('You don\'t have a table opened.')

		@self.command(name = 'sel', pass_context=True, help = '[optional: -c/-r] [names of selected cols/rows to view]')
		async def _sel(context, *args):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				# Import files
				self.file_name = self.file_dict[self.ID]
				self.appending = self.appending_dict[self.ID]
				self.df = self.df_dict[self.ID][-1]

				# By default second and onward arguments are names
				names = list(args).pop(0)
				print_df = pd.DataFrame()
				error = False
				stype = "unknown"

				# Select depending on -c, -r or guess
				if args[0] == "-c":
					try:
						print_df = self.df[names]
						stype = "columns"
					except Exception as e:
						error = True
						await context.message.channel.send('❌ Columns not found. System error: ' + str(e))
				elif args[0] == "-r":
					try:
						print_df = self.df.loc[names]
						stype = "rows"
					except Exception as e:
						error = True
						await context.message.channel.send('❌ Rows not found. System error: ' + str(e))
				else:
					names = list(args)
					try:
						print_df = self.df[names]
						stype = "columns"
					except Exception as e:
						try:
							print_df = self.df.loc[names]
							stype = "rows"
						except Exception as e:
							error = True
							await context.message.channel.send('❌ Rows or columns not found. System error: ' + str(e))
				if error == False:
					await context.message.channel.send("🖨 Printing " + stype + " " + str(names) + " from table: " + self.file_name)
					await fprint(context, self.file_name, print_df)
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')    

		@self.command(name = 'total', pass_context=True, help = 'returns sum of every single cell for each column')
		async def _total(context, *args):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				# Import table
				self.file_name = self.file_dict[self.ID]
				self.df = self.df_dict[self.ID][-1]
				try:
					sum_df = self.df.copy()
					print_df = self.df.copy()
					cols = sum_df.columns.tolist()
					total = []
					for col in cols:
						sum_df[col] = pd.to_numeric(sum_df[col], errors='coerce')
						total.append(sum_df[col].sum())
					print_df.loc["Sum"] = total

					# Save if "-a" flag mentioned
					if len(args) > 0 and args[0] == "-a":
						self.df.loc["Sum"] = total
						save_file(self.df, self.ID, self.file_name)
					
					# Always print table
					await context.message.channel.send("🖨 Printing totals of table: " + self.file_name)
					await fprint(context, self.file_name, print_df)
				except Exception as e:
					await context.message.channel.send('❌ System error: ' + str(e))
			else:
				await context.message.channel.send('❓ You don\'t have a table opened.')

		@self.command(name = 'sort', pass_context=True, help = '[optional: -c/-r] [col/row]')
		async def _sort(context, *args):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				# Load files
				self.file_name = self.file_dict[self.ID]
				self.df = self.df_dict[self.ID][-1]
				error = False
				name = "null"
				stype = "null"

				# Forced row/col or guessed sorting
				if args[0] == "-c":
					name = args[1]
					try:
						self.df =self.df.sort_values(by=name)
						stype = "column"
					except Exception as e:
						error = True
						await context.message.channel.send('❌ Column not found. System error: ' + str(e))
				if args[0] == "-r":
					name = args[1]
					try:
						self.df =self.df.sort_values(by=name, axis=1)
						stype = "row"
					except Exception as e:
						error = True
						await context.message.channel.send('❌ Row not found. System error: ' + str(e))
				else:
					name = args[0]
					try:
						self.df = self.df.sort_values(by=name)
						stype = "column"
					except Exception as e:
						try:
							self.df = self.df.sort_values(by=name, axis=1)
							stype = "row"
						except Exception as e:
							error = True
							await context.message.channel.send('❌ Row or column not found. System error: ' + str(e))
				
				# Save and print if no errors found
				if error == False:
					save_file(self.df, self.ID, self.file_name)
					await context.message.channel.send("🎲 Sorted " + self.file_name + " by " + stype + " " + name)
					await fprint(context, self.file_name, self.df)
					self.df_dict[self.ID] = dict_append(self.df_dict[self.ID], self.df)
			else:
				await context.message.channel.send('You don\'t have a table opened.')

		# TODO: Fix -c and -r flags; Seperate commands into cogs
		@self.command(name = 'rename', pass_context=True, help = ' [optional: -c/-r] [old col/row] [new col/row]')
		async def _rename(context, *args):
			self.ID = context.guild.id
			if self.appending_dict[self.ID] == True:
				# Load files
				self.file_name = self.file_dict[self.ID]
				self.df = self.df_dict[self.ID][-1]

				# By default second and third arguments are old and new col/row names
				error = False

				# Forced row/col or guessed renaming
				if args[0] == "-c" or args[0] == "-r": # Force rename column
					old, new = args[1], args[2]
					self.df.rename({old:new}, inplace = True)
					self.df.rename(columns = {old:new}, inplace = True)
				else: # Try amend row, then try amend column
					old, new = args[0], args[1]
					self.df.rename({old:new}, inplace = True)
					self.df.rename(columns = {old:new}, inplace = True)

				# If no errors save and print table
				if error == False:
					save_file(self.df, self.ID, self.file_name)
					await context.message.channel.send("🎉 Renamed " + str(old) + " to " + str(new) + " in table: " + self.file_name)
					await fprint(context, self.file_name, self.df)
					self.df_dict[self.ID] = dict_append(self.df_dict[self.ID], self.df)
			else:
				await context.message.channel.send('You don\'t have a table opened.')
		
# INITIALISE CLIENT
client = cluelessBot(command_prefix="^", self_bot=False)
client.remove_command('help')
client.load_extension('help_cmd')
client.load_extension('misc')

# Run Client
client.run(code)