#!/bin/env python3
import discord
import asyncio
import argparse
import traceback
import subprocess
import sys
from io import StringIO


client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
    
stack = ""
@client.event
async def on_message(message):
	global stack
	print('msg by ' + message.author.name + ": " + message.content)
	if message.content.startswith('+hug'):
		for user in message.mentions:
			await client.send_message(message.channel,  user.mention + " u received a hug from @" +   message.author.name)
#	if message.content.startswith('::bash'):



bashing = None

#async def check_bash():
	
	

parser = argparse.ArgumentParser(description='selfbot')
parser.add_argument('token')
args = parser.parse_args()
client.run(args.token)

