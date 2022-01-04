import json
import os
from collections import Counter
from random import choice

import discord
from discord.ext.commands.core import check
import psycopg2 as ppg
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv

#Don't steal my token !!!
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

#database = ppg.connect(DATABASE_URL, sslmode='require')
#database.set_session(autocommit=True)
#cursor = database.cursor()
#print(cursor.fetchall())
#cursor.close()

client = commands.Bot(command_prefix='r/', case_insensitive=True) 
#Create client that responds to commands
#slash = SlashCommand(client, sync_commands=True)

#Open helpme.txt and make a string
helpme_text = ""
with open("helpme.txt") as file:
    for line in file:
        helpme_text += line

#Load each commentsn.json file into a list 
#Create a list of comments for each subreddit/all
sr_list = []
subreddit_dict = {}
#subreddit_dict["irl"] = []
subreddit_dict["all"] = []
with open("Data/comments.json") as file:
    file_data = json.load(file)

    for comment in file_data:
        subreddit_dict["all"].append(comment)
        srstr = comment["subreddit"]
        if srstr.lower() in subreddit_dict:
            subreddit_dict[srstr.lower()].append(comment)
        else:
            subreddit_dict[srstr.lower()] = [comment]
        sr_list.append(srstr)
    
sr_chart = dict(sorted(Counter(sr_list).items(), key=lambda a : a[1], reverse=True))

subreddit_dict["top"] = sorted(subreddit_dict["all"], key=lambda a: a["score"], reverse=True)

commands_list = ["r/random", "r/top", "r/helpme", "r/subreddit", "r/find", "r/topsubreddits"]

#Notify when the bot has connected to Discord
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Reddit ● r/helpme"))
    print(f'{client.user} has connected to Discord!')

#Splits message into smaller bits to send through discord
async def send_split(ctx, string):
    size = len(string)
    lower = 0
    while size > 0:
        await ctx.send(string[lower:lower + min(size, 2000)])

        if size > 2000:
            size -= 2000
            lower += 2000
        else:
            break

#General subreddit output command
async def output_subreddit(ctx, subreddit_name, index_choice=0, show_index=True, update_status=True):
    #await print("r/" + subreddit_name + " was executed")
    subreddit_list = subreddit_dict[subreddit_name]
    subreddit_length = len(subreddit_list)

    if index_choice >= 0 and index_choice <= subreddit_length:
        if index_choice == 0:
            index = choice(range(0, subreddit_length))
        else:
            index = index_choice-1

        await send_split(ctx, subreddit_list[index]["body"])
        if show_index:
            await ctx.send(f"**({str(index + 1)}/{str(len(subreddit_list))})**")
        if update_status:
            await client.change_presence(activity=discord.Game(f"Reddit ● r/{subreddit_name}"))
    else: 
        await ctx.send("*Invalid index*")

flag_list = ["--showindex", "-si", "--bold", "-b", "--index", "-i", "--updatestatus", "-us"]
#take in args and determine what they are
async def parse_input(args, *, return_index_change=False, return_bold=False, status_only=False):
    index = 0
    show_index = True
    input_string = ""
    modified_index_args = False
    show_bold = True 
    update_status = True
    
    for num, Input in enumerate(args):
        input = Input.lower()
        try:
            integer = int(input)
        except ValueError:
            pass

        last_arg = args[num-1]
        if input == "false":
            if last_arg == "--showindex" or last_arg == "-si":
                show_index = False
                modified_index_args = True
            elif last_arg == "--bold" or last_arg == "-b":
                show_bold = False
            elif last_arg == "--updatestatus" or last_arg == "-us":
                update_status = False
        elif input == "true": 
            if last_arg == "--showindex" or last_arg == "-si":
                show_index = True
                modified_index_args = True
            elif last_arg == "--bold" or last_arg == "-b":
                show_bold = False
            elif last_arg == "--updatestatus" or last_arg == "-us":
                update_status = True
        elif "integer" in locals() and (last_arg == "--index" or last_arg == "-i"):
            index = integer
            modified_index_args = True
        elif input != "--showindex" and input not in flag_list:
            input_string += " " + Input

    input_string = input_string[1:] #Take out first space

    if status_only:
        return update_status
    elif return_bold and return_index_change:
        return (index, show_index, input_string, modified_index_args, show_bold, update_status)
    elif return_bold and not return_index_change:
        return (index, show_index, input_string, show_bold, update_status)
    elif return_index_change and not return_bold:
        return (index, show_index, input_string, modified_index_args, update_status)
    else:
        return (index, show_index, input_string, update_status)
#Gives a random message when "r/random" is typed
@client.command()
async def random(ctx, *args):
    status = await parse_input(args, status_only=True)
    await output_subreddit(ctx, "all", 0, show_index=False, update_status=status)

#Gives nth ranked message in terms of upvotes
@client.command()
async def top(ctx, *args):
    index, show_index, string, index_changed, update_status = await parse_input(args, return_index_change=True)
    if not index_changed:
        index = 1
    await output_subreddit(ctx, "top", index, show_index, update_status)

#Finds messages containing the user input and gives a random one of those when "r/find" is typed
@client.command()
async def find(ctx, *args):#usermessage, index_choice=0):
    index_choice, show_index, usermessage, bold, update_status = await parse_input(args, return_bold=True)

    search_list = []
    for message in subreddit_dict["all"]:
        if usermessage in message["body"]:
            search_list.append(message)

    search_list_len = len(search_list)

    if search_list_len > 0 and index_choice >= 0 and index_choice <= search_list_len:
        if index_choice == 0:
            list_index = choice(range(0, search_list_len))
        elif index_choice <= search_list_len and index_choice >= 1:
            list_index = index_choice - 1

        mensaje = search_list[list_index]["body"]

        string_index = mensaje.find(usermessage)
        last = string_index + len(usermessage) + 2
        if bold:
            mensaje = mensaje[:string_index] + "**" + mensaje[string_index:]
            mensaje = mensaje[:last] + "**" + mensaje[last:]

        await send_split(ctx, mensaje)
        if show_index:
            await ctx.send(f"**({str(list_index + 1)}/{str(search_list_len)})**")
    elif search_list_len == 0:
        await ctx.send("*Term not found*")
    else:
        await ctx.send("*Invalid index*")

    if update_status:
        await client.change_presence(activity=discord.Game("Reddit ● r/find"))

#Gives a random message from a particular subreddit
@client.command()
async def subreddit(ctx, *args):
    index, show_index, sr_string, update_status = await parse_input(args)

    #Only the first word should be considered as a potential subreddit
    #Otherwise a user accidentally putting something after the command (i.e. an index number w/o flag)
    #will still get the expected output
    sr_string = sr_string.split()[0].lower()

    if sr_string in subreddit_dict:
        await output_subreddit(ctx, sr_string, index, show_index, update_status)
    else:
        await ctx.send("*Subreddit not found*")
        if update_status:
            await client.change_presence(activity=discord.Game("Reddit ● r/subreddit"))

"""
#Add/look at quotes from Alex
@client.command()
async def IRL(ctx, *args):
    if not args:
        await output_subreddit(ctx, subreddit_dict["irl"], "IRL", 0) 
    elif str(args[0]).lower() == "add":
        msg_str = ""
        for i in range(1, len(args)):
            msg_str += args[i] + " "

        msg_str = msg_str[:-1]

        msg_dict = {
            "body": msg_str,
            "score": 0,
            "subreddit": "IRL"
        }
        subreddit_dict["irl"].append(msg_dict)
        await ctx.send(f"*{msg_str} added*")
    elif int(args[0]):
        await output_subreddit(ctx, subreddit_dict["irl"], "IRL", int(args[0])) 
    else:
        await ctx.send("Invalid input!")

    await client.change_presence(activity=discord.Game("Reddit ● r/IRL"))
"""

#Gives the list of subreddits by message counts
@client.command()
async def topsubreddits(ctx, *args):
    dont, care, string, status = await parse_input(args)
    
    try:
        numshown = int(string)
    except ValueError:
        numshown = 10

    output = ""
    for number, key in enumerate(sr_chart):
        output += f"{number+1}. {str(key)}: {str(sr_chart[key])} \n"

        if number + 1 == numshown:
            break

    await ctx.send(output)
    if status:
        await client.change_presence(activity=discord.Game("Reddit ● r/topsubreddits"))

#Gives help message when user requests it
@client.command()
async def helpme(ctx, *args):
    await ctx.send(helpme_text)  
    status = await parse_input(args, status_only=True)
    if status:
        await client.change_presence(activity=discord.Game("Reddit ● r/helpme"))

@client.event
async def on_message(message):
    content = message.content
    first_word = content.split()[0]

    if first_word.lower() not in commands_list and first_word[0:2] == "r/":
        subreddit_name = content[2:]
        message.content = f"r/subreddit {subreddit_name}"

    await client.process_commands(message)
        
client.run(TOKEN)
