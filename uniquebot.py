#!/usr/bin/env python3

import sys
import json
import os
import discord
import asyncio
from discord.ext import commands
import botConfig

bot = commands.Bot(command_prefix=botConfig.botPrefix)

unsilenceTime = botConfig.unsilenceTime

msgCache = botConfig.msgCache

deathCache = botConfig.deathCache

commanderRoleId = botConfig.commanderRoleID

silencedRoleName = botConfig.silencedRoleName

easterEggs = botConfig.easterEggs

commandList = botConfig.commandList

TOKEN = botConfig.botToken

@bot.event
async def on_ready():
    print("\n-----------------------")
    print("Connected to Discord as")
    print(bot.user.name)
    print(bot.user.id)
    print("Invite: https://discordapp.com/oauth2/authorize?&client_id={0}&scope=bot&permissions=0".format(bot.user.id))
    print("-----------------------\n")
    bot.remove_command("help") #remove this if you want to keep the help command

try: #check if the file holding messages exists and create it if it doesn't
    data = open(msgCache, "r+")
    data.close()
except FileNotFoundError as err:
    print(err)
    confirm = input("Would you like to create the file '{0}'? [Y/n]\n".format(msgCache))
    if confirm.lower() == "y":
        try:
            tempFile = open(msgCache, "a+")
            tempFile.write("{}")
            tempFile.close()
        except IOError as err:
            sys.exit(err)
        else:
            sys.exit("Please restart the bot now.")
    else:
        sys.exit()
except IOError as err:
    sys.exit(err)

try: #load messages into a dictionary upon bot startup
    data = open(msgCache, "r+")
    dataStore = data.read()
    dataDict = json.loads(dataStore)
    data.close()
except IOError as err:
    sys.exit(err)

try: #check if the file holding messages exists and create it if it doesn't
    death = open(deathCache, "r+")
    death.close()
except FileNotFoundError as err:
    print(err)
    confirm = input("Would you like to create the file '{0}'? [Y/n]\n".format(deathCache))
    if confirm.lower() == "y":
        try:
            tempDeaths = open(deathCache, "a+")
            tempDeaths.write("{}")
            tempDeaths.close()
        except IOError as err:
            sys.exit(err)
        else:
            sys.exit("Please restart the bot now.")
    else:
        sys.exit()
except IOError as err:
    sys.exit(err)

try: #load deaths into a dictionary upon bot startup
    with open(deathCache, "r+") as deaths:
        deathStore = deaths.read()
        deathDict = json.loads(deathStore)
except IOError as err:
    sys.exit(err)

@bot.command(pass_context=True) #command to get the role ID to put under "commanderRoleId" in the config
async def userRoles(ctx, member: discord.Member = None):
    await bot.say("Please change the variable `commanderRoleId` in the config file to the id of the role you intend to give to those with power. (You have to have the role when you use this command.)")
    if member is None:
        member = ctx.message.author
    message = "{0.mention}'s roles:\n```\n".format(member)
    for roleObj in member.roles:
        message += "Name: {0.name}, ID: {0.id}\n".format(roleObj)
    message += "```"
    await bot.say(message)
    
@bot.command(pass_context=True) #command to upload the message file
async def upload(ctx):
    with open(msgCache, "rb") as messageFile:
        await bot.send_file(ctx.message.channel, messageFile)

@bot.command(pass_context=True) #command to get the death file (stored as user ID) or the death count of a person
async def deaths(ctx, member: discord.Member = None):
    if member is None:
        with open(deathCache, "rb") as deathFile:
            await bot.send_file(ctx.message.channel, deathFile)
    else:
        try:
            await bot.say("{0.name}'s death count is {1}.".format(member, deathDict[member.id]))
        except KeyError:
            await bot.say("{0.name} has not died yet (or has died before the death counter was implemented).".format(member))

@bot.group(pass_context=True) #a command group with "message" and "death" which clear the message cache/file and the death cache/file respectively
async def clear(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("{0.mention}, you must specify a subcommand.".format(ctx.message.author))

@clear.command(pass_context=True) #clear the message cache and file
async def message(ctx):
    if commanderRoleId in [roleObj.id for roleObj in ctx.message.author.roles]:
        await bot.say("Clearing message cache as per {0}'s request.".format(ctx.message.author.mention))
        try:
            with open(msgCache, "r+") as data:
                data.truncate()
                data.write("{}")
                dataDict.clear()
        except Exception as err:
            await bot.say(err)
    else:
        await bot.say("{0}, you are not able to clear the message cache.".format(ctx.message.author.mention))

@clear.command(pass_context=True) #clear the death cache and file
async def death(ctx):
    if commanderRoleId in [roleObj.id for roleObj in ctx.message.author.roles]:
        await bot.say("Clearing death cache as per {0}'s request.".format(ctx.message.author.mention))
        try:
            with open(deathCache, "r+") as data:
                data.truncate()
                data.write("{}")
                dataDict.clear()
        except Exception as err:
            await bot.say(err)
    else:
        await bot.say("{0}, you are not able to clear the death cache.".format(ctx.message.author.mention))

@bot.event #the main guts
async def on_message(message):
    msg = message.content
    usr = message.author.id
    if usr != bot.user.id and msg.startswith(tuple(commandList)) == False and msg != "" and msg.lower() not in easterEggs:
        if msg not in dataDict:
            dataDict.update({msg:1})
        else:
            if usr not in deathDict:
                deathDict.update({usr:1})
            else:
                deathDict[usr] += 1
            dataDict[msg] += 1
            role = discord.utils.get(message.server.roles, name=silencedRoleName)
            await bot.add_roles(message.author, role)
            await bot.send_message(message.channel, "{0}, you have been silenced for sending a message that's been sent previously.".format(message.author.mention))
            
            with open(msgCache, "r+") as dataFile:
                dataJson = json.dumps(dataDict)
                dataFile.write(dataJson)
            
            with open(deathCache, "r+") as deathFile:
                deathJson = json.dumps(deathDict)
                deathFile.write(deathJson)

            await asyncio.sleep(unsilenceTime)
            await bot.remove_roles(message.author, role)
            await bot.send_message(message.channel, "{0}, you have now been unsilenced.".format(message.author.mention))

    elif msg.lower() in easterEggs:
        await bot.send_message(message.channel, easterEggs[msg.lower()])
        role = discord.utils.get(message.server.roles, name=silencedRoleName)
        await bot.add_roles(message.author, role)
        await bot.send_message(message.channel, "{0} Looks like you've found an easter egg ^. Sorry, but you're still gonna be silenced.".format(message.author.mention))
        await asyncio.sleep(unsilenceTime)
        await bot.remove_roles(message.author, role)
        await bot.send_message(message.channel, "{0}, you have now been unsilenced.".format(message.author.mention))

    await bot.process_commands(message) #send message through the commands in case it was a command

@bot.event
async def on_member_join(member): #join message
    channel = member.server
    await bot.send_message(channel, "Welcome to {0.name}, {1.mention}. Have a fun time!".format(channel, member))

@bot.event
async def on_member_remove(member): #leave message
    channel = member.server
    await bot.send_message(channel, "{0.mention} has left I guess. Maybe they just couldn't handle the silencing?".format(member))

bot.run(TOKEN)
