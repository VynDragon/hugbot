#!/bin/env python3
import discord
import asyncio
import argparse
import traceback
import subprocess
import random
import mimetypes
import http.server
import os.path
import shutil
import sys
import io

loop = asyncio.get_event_loop()
client = discord.Client(loop=loop)

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

errorPath = "./data/error/"

class RequestHandler(http.server.BaseHTTPRequestHandler):
	def handleHeaders(self, response):
		self.send_response(response)
		self.end_headers()

	def handleError(self, error):
		self.handleHeaders(error)
		with open(errorPath+str(error)+".html", 'rb') as  filee:
					shutil.copyfileobj(filee, self.wfile)
					self.wfile.flush()

	def parseStream(self, stream):
		return stream.read()

	def do_GET(self):
		try:
			with io.open("./client"+self.path, 'rb') as  filee:
				filetype, encoding = mimetypes.guess_type("./client"+self.path, strict=False)
				self.send_response(200)
				self.send_header("Content-Type", filetype)
				self.end_headers()
				shutil.copyfileobj(filee, self.wfile)
				self.wfile.flush()
		except FileNotFoundError:
			self.handleError(404)

def recallHandle(server, loop, time):
	server.handle_request()
	loop.call_later(time, recallHandle, server, loop, time)

parser = argparse.ArgumentParser(description='selfbot')
parser.add_argument('token')
parser.add_argument('serverip')
args = parser.parse_args()
random.seed()

server = http.server.HTTPServer((args.serverip, 8001), RequestHandler)
server.timeout = 0.5

loop.call_later(0.5, recallHandle, server, loop, 0.5)

try:
	loop.run_until_complete(client.start(args.token))
except KeyboardInterrupt:
	server.shutdown()
	loop.run_until_complete(client.logout())
finally:
	loop.close()


