import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)
load_dotenv()
TOKEN = os.getenv("TOKEN")

print("Bot made by Indysaurus#0001")

#Reads config file and splits into dictionary.
config = {}
with open('config.txt') as fileobj:
  for line in fileobj:
      key, value = line.rstrip("\n").split("=")
      config[key] = value

#Prints config to console.
print("Printing bot configurations...")
for key,val in config.items():
    print (key, "=>", val)

#Reads nono-words.txt the list of banned words and puts into a list + lowercase.
def nono():
    global bad_words
    test = []
    with open ('nono-words.txt', 'r+') as f:
        bad_words = f.read().splitlines()
        bad_words = [x.lower() for x in bad_words]

#Ready Check
print("\nAttempting to log in...")
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

#Command error Catching
@client.event
async def on_command_error(ctx, error):
    print(ctx.command.error, "Invoked Incorrectly!")
    print(error)

#!Purge # Command. must have manage message permissions.
if ('Purge', 'True') in config.items():
    @client.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(ctx, number):
        number = int(number)
        number += 1
        if number <= 0:
            return
        await ctx.channel.purge(limit=number)


#Chat filter. Filter located in nono_words
if ('Filter', 'True') in config.items():
    @client.event
    async def on_message(message):
        print(message)
        messageChannel = message.channel.id
        messageContent = message.content.lower()
        if len(messageContent) > 0 and message.channel.id != int(config.get('BotLogs')):
            if any(bad_word in messageContent for bad_word in bad_words):
                await message.delete()
                channel = client.get_channel(int(config.get('BotLogs')))
                report =(message.author.id, messageContent)
                await channel.send(report)
                msg = await message.channel.send('A filtered word was used. This incident has been logged.')
                await asyncio.sleep(8) #seconds
                await msg.delete()
        await client.process_commands(message)
        
if ('AutoRole', 'True') in config.items():
    @client.event
    async def on_member_join(member):
        roleAssign = get(member.guild.roles, name=config.get('RoleName'))
        await member.add_roles(roleAssign)

if __name__ == "__main__":
    nono()
    client.run(TOKEN)
