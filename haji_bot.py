import os
import discord
from discord.ext import commands
import logging
from zh import team
import asyncio

from dotenv import load_dotenv, find_dotenv

def split_teams(str):
	str = str.lower() # convert to lowercase to handle 'vs' in any case
	teams = str.split('vs')   # splitting string by 'vs'

	# splitting each team's members and capitalizing the first letter of each name
	team1 = [name.strip().capitalize() for name in teams[0].split()]
	team2 = [name.strip().capitalize() for name in teams[1].split()]

	# checking if the number of names are equal before and after the 'vs'
	if len(team1) == len(team2):
		# if the number of names are equal, we return the names of each team as lists
		return team1, team2
	else:
		raise ValueError("Number of team members are not equal.")


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "credentials.env"))
load_dotenv(find_dotenv())

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.hybrid_command(name="haji", help= "The command to generate--> haj! \"name1 name2 vs name3 name4 \" ")
async def generate(ctx, *, arg):
	try:
		makke, madineh = split_teams(arg)
	except ValueError as e:
		logging.WARNING("wrong command format")
		print(e)
		return await ctx.send("The input string is not formatted properly! \n the command to generate--> \n haj! **<name1>**; **<name2>**; **<vs>**; **<name3>;...**")


	# creating the teams
	team1 = team("Makke",len(makke))
	team2 = team("Madineh",len(madineh))

	for member in makke:
		team1.add_player(member)
	for member in madineh:
		team2.add_player(member)
	
	team1.calculate_rates(team2)
	text = [team1.print()]
	text.append(team2.print())
	text2=[team1.report()]
	text2.append(team2.report())

	text_pretty = "**{}** {}".format(ctx.current_argument, ctx.author.mention)
	await ctx.reply(text_pretty)
	logging.info(text_pretty)
	for line in "\n".join(text):
		text_pretty = "```{}```".format(line)
		await ctx.reply(text_pretty)
		await asyncio.sleep(0.8)  # delay for 1 second
	for line in "\n".join(text2):
		text_pretty = "```{}```".format(line)
		await ctx.reply(text_pretty)
		await asyncio.sleep(0.4)  # delay for 1 second

bot.run(DISCORD_TOKEN)
