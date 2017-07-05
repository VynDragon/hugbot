#!/bin/env python3
import discord
import asyncio
import argparse
import traceback
import subprocess
import random
import http.server
import os.path
import shutil
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
			await client.send_message(message.channel,  user.mention + " u received a hug from @" +   message.author.name + " " + hug_images[random.randrange(0, len(hug_images), 1)])
	if message.content.startswith('+pat'):
		for user in message.mentions:
			await client.send_message(message.channel,  user.mention + " u received a hug from @" +   message.author.name)


class RequestHandler(http.server.BaseHTTPRequestHandler):
	def handleHeaders(self, response):
		self.send_response(response)
		self.end_headers()

	def handleError(self, error):
		self.handleHeaders(error)
		with open(errorPath+str(error)+".html", 'rb') as  filee:
					shutil.copyfileobj(filee, self.wfile)
					self.wfile.flush()
	def do_GET(self):
		try:
			with open("./client"+self.path, 'rb') as  filee:
				self.handleHeaders(200)
				self.end_headers()
				shutil.copyfileobj(filee, self.wfile)
				self.wfile.flush()
		except FileNotFoundError:
			self.handleError(404)
	

parser = argparse.ArgumentParser(description='selfbot')
parser.add_argument('token')
parser.add_argument('serverip')
args = parser.parse_args()
random.seed()
client.run(args.token)
server = http.server.HTTPServer((args.serverip, 8001), RequestHandler)
server.serve_forever()
