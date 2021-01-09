import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)
load_dotenv()
TOKEN = os.getenv("TOKEN")

print("Bot made by Indy12323#1203")

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
nono = open('nono-words.txt')
bad_words = [line.strip() for line in nono]
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
        print("2")
        number = int(number)
        number += 1
        if number <= 0:
            return
        print("3")
        await ctx.channel.purge(limit=number)

#Chat filter. Filter located in nono_words
if ('Filter', 'True') in config.items():
    @client.event
    async def on_message(message):
        messageContent = message.content.lower()
        if len(messageContent) > 0:
            if any(bad_word in messageContent for bad_word in bad_words):
                    await message.delete()
                    await message.channel.send('Thats a nono word.')
        await client.process_commands(message)

if ('AutoRole', 'True') in config.items():
    @client.event
    async def on_member_join(member):
        roleAssign = get(member.guild.roles, name=config.get('RoleName'))
        await member.add_roles(roleAssign)


client.run(TOKEN)
