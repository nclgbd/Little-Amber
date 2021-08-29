#!/usr/bin/python

import time
import sched
import discord
import json
import re
import os
import random
import asyncio
import TenGiphPy

from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime, timedelta



CHANNEL_NAMES = ["philosophy", "religion", "psychology", "sociology", "economics", "us-politics",
                 "global-politics", "history", "science", "lgbt", "rhetoric", "art-analysis", "miscellaneous", "bot-testing"]

CHANNEL_LIBRARY = [826749300993425419,
                   827467898804502538,
                   828164039874969610,
                   828164009365733406,
                   826749319079002153,
                   828110549489025094,
                   826749445701369886,
                   826751598671167498,
                   826877724449701958,
                   827328040702836736,
                   826749736400584766,
                   826749577344057414,
                   830770149657280532,
                   831716059555692584]


CHANNEL_LINKS = [830772056702058547,
                 830772486903300116,
                 830772094031626268,
                 830772121047007243,
                 830772160401899560,
                 830772337741398067,
                 830772370842058752,
                 830772403059032104,
                 830772431953854465,
                 830772459506106369,
                 830772586701914143,
                 830772625105485874,
                 831728489152512040,
                 831715977020309514]

CHANNEL_MAPPING = dict(zip(CHANNEL_LIBRARY, CHANNEL_LINKS))

LINK_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

with open("config/config.json", "r") as j:
    bot_info = json.load(j)
    
PREFIX = bot_info["prefix"]
TOKEN = bot_info["token"]
CLIENT = commands.Bot(command_prefix = PREFIX)
CLIENT_ID = bot_info["client_id"]
ME = bot_info["me"]
TENOR_API_TOKEN = bot_info["tenor_api_token"]
GIPHY_API_TOKEN = bot_info["giphy_api_token"]
TENOR = TenGiphPy.Tenor(token=TENOR_API_TOKEN)
GIPHY = TenGiphPy.Giphy(token=GIPHY_API_TOKEN)
ALARM_TIME = '23:29'#24hrs

START_TIME = datetime.utcnow()
print(START_TIME)

class BookClub:
    
    def __init__(self, file_path):
        
        self.icon_url = "https://media.discordapp.net/attachments/826743475143311390/870399372603580487/wackydebaters.gif"
        self.file_path = file_path
        with open(self.file_path, "r") as f:
            self.books = dict(json.load(f))
            
        self.current_readings = self.get_current_readings()
        
    
    
    def update_library(self):
        
        with open(self.file_path, "w") as f:
            json.dump(self.books, f)
       
       

    def get_current_readings(self):

        current_readings = dict()
        for book in self.books:
            if self.books[book]["current_reading"]:
                current_readings[book] = self.books[book]["url"]
                
        return current_readings  
    
    
    
    def upload_book(self, attachment, is_current_reading=True):
        
        filename = attachment.filename[:-4]
        url = attachment.url
        self.books[filename] = {"url" : url,
                                "current_reading": is_current_reading}
        
        self.update_library()
      
        
        
    def set_current_reading(self, book_name, is_current_reading=True):
        self.books[book_name]["current_reading"] = is_current_reading
        self.update_library()
        
    
    
    def remove_book(self, book_name):
        del self.books[book_name]
        self.update_library()


book_club = BookClub("media/book_club/books.json")

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print('------')
    
    await CLIENT.change_presence(activity=discord.Game(name='Studying...', type=1))
    
    

@CLIENT.event
async def on_message(message):
    if message.channel.id in CHANNEL_LIBRARY and message.author.id != CLIENT_ID:
        link_id = CHANNEL_MAPPING[message.channel.id]
        links = re.findall(LINK_REGEX, message.content) 
        
        if len(links) > 0 or len(message.attachments) > 0:
            channel = CLIENT.get_channel(link_id)
            if len(message.attachments) > 0:
                await channel.send(message.attachments[0].url + " from: " + str(message.author.display_name))
                
            else:
                await channel.send(message.content + " from: " + str(message.author.display_name))
    
    await CLIENT.process_commands(message)



@CLIENT.command(name='wacky',
                aliases=['wackydebators', 'wacky_debators'],
                description="Wacky Debators HATE her!!! Debatebros in DGG want from 3 to 27 WINS with this ONE WEIRD EMOTE. >>>CLICK HERE<<< TO LEARN MORE")
async def wacky_debators(ctx):
    """Wacky Debators HATE her!!! Debatebros in DGG want from 3 to 27 WINS with this ONE WEIRD EMOTE. >>>CLICK HERE<<< TO LEARN MORE"""
    wacky_url = "https://cdn.discordapp.com/attachments/826739157309063179/833257773500203028/wacky-debaters-HATE-her-gif-2.gif"
    await ctx.send(wacky_url)



@CLIENT.command(name='epiphany',
                aliases=["bunny", "epi", "bun"])
async def epiphany(ctx):
    '''For the bunny guy~.'''
    tenor = await TENOR.arandom(tag='bunny')
    await ctx.send(tenor)
    
    

@CLIENT.command(name='neari')
async def neari(ctx):
    '''No flirting, it's banned!'''
    string = "Hey all, just an FYI because I feel like I’m losing my mind.\n\
None of my interactions in here with anyone, SHOULD EVER BE CONSIDERED AS FLIRTING. It is nothing more than me being your friend. I do not find any of you attractive, or want anything more than friendship. Is this weird to say, yes? But it shouldn’t be a problem to any of you."
    await ctx.send(string)



@CLIENT.command(name='soapy',
                aliases=["raccoon"])
async def soapy(ctx):
    '''Posts raccoons for Soapy~.'''
    _, _, file_names = os.walk("media/raccoons").__next__()
    fl = discord.File("media/raccoons/{}".format(random.choice(file_names)))
    tenor = await TENOR.arandom('raccoon')
    giphy = await (GIPHY.arandom(tag="raccoon"))#['data']['images']['downsized_large']['url']
    giphy = giphy['data']['images']['downsized_large']['url']
    gif = random.choice([giphy, tenor])
    file_option = random.choice([fl, tenor, giphy])
    if type(file_option) == discord.file.File:
        await ctx.send(file=file_option)
    else:
        await ctx.send(file_option)
    
    
    
@CLIENT.command(name='kira',
                aliases=["catgirl"])
async def kira(ctx):
    '''Posts a catgirl for catgirl kira~.'''
    await ctx.send(await TENOR.arandom('catgirl'))
    
    
    
@CLIENT.command(name='whistle',
                description=".... I didn't do a damn thing~")
async def whistle(ctx):
    url = "https://github.com/nclgbd/Little-Amber/blob/master/media/AmberWhistle.gif?raw=true"
    await ctx.send(url)
    
    
    
@CLIENT.command(name='readme',
                description="Gives the link to the README.md")
async def read_me(ctx):
    """If the stemlords that actually care about the code, this is your command. Or `!info`"""
    url = "https://github.com/nclgbd/Little-Amber/blob/master/README.md"
    await ctx.send(url)
    


@CLIENT.command(name='bully',
                aliases=["bullied"])
async def bully(ctx):
    """Gonna cry? Gonna piss your pants? Maybe? Maybe shit and cum?… Well then you fucking normie, maybe you should click on
    my username and on my profile you should see three dots to the right of my username. Click those three dots to open a dropdown
    menu reads "Block". Click that option and confirm that you want to block me to avoid seeing my future posts"""
    bully_url = "https://media.discordapp.net/attachments/275435872424296449/830192706030010448/unknown.png"
    await ctx.send(bully_url)



@CLIENT.command(name='info',
                aliases=['botinfo', 'bot_info'])
async def info(ctx):
    '''
    Returns the code for the bot.
    '''
    me = await CLIENT.fetch_user(ME)
    embed = discord.Embed(title="Little Amber", color=0xff0000,
                          description="The source code for Little Amber. Press !help for a list of available commands.")
    
    embed.set_author(name="Creator: " + me.display_name)
    embed.set_footer(text="You have permission to ping me with any questions and/or suggestions for the bot :)")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/831716059555692584/831963479153967115/831420535941890079.png")
    
    embed.add_field(name='GitHub', value='https://github.com/nclgbd/Little-Amber', inline=True)
    embed.add_field(name='Submit an Issue!', value="https://github.com/nclgbd/Little-Amber/issues", inline=True)
    embed.add_field(name='View My Progress', value="https://github.com/nclgbd/Little-Amber/projects/1", inline=True)
    embed.add_field(name='README.md', value="https://github.com/nclgbd/Little-Amber/blob/master/README.md", inline=True)
    
    await ctx.send(embed=embed)



@CLIENT.command(name='irk')
async def irk(ctx):
    """Black Italian."""
    irk_url = "https://media.discordapp.net/attachments/827669718563029012/842144430358003722/unknown.png"
    await ctx.send(irk_url)



@CLIENT.command(name='bible',
                aliases=['bible_study'])
async def bible_study(ctx):
    """:ReadTheBible:"""
    url = "https://media.discordapp.net/attachments/831987127306289233/853751236766203914/unknown.png"
    await ctx.send(url)



@CLIENT.command(name='amber',
                aliases=['bullet'])
async def amber(ctx):
    """We miss you <3"""
    url = "https://media.discordapp.net/attachments/829429908848902164/866413383375650846/unknown.png"
    await ctx.send(url)



@CLIENT.command(name='bonk')
async def bonk(ctx):
    """*Bonk!* Use it to tell someone to knock it off!"""
    url = "https://media.discordapp.net/attachments/826911867166916668/855848987063746620/image0.png?width=583&height=702"
    await ctx.send(url)



@CLIENT.command(name='uptime',
                description='Returns how long the bot has been running for.')
async def uptime(ctx):
    '''
    Source: https://stackoverflow.com/questions/52155265/my-uptime-function-isnt-able-to-go-beyond-24-hours-on-heroku
    '''
    now = datetime.utcnow() # Timestamp of when uptime function is run
    delta = now - START_TIME
    
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
        
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
        
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await ctx.send('{} has been up for {}'.format(CLIENT.user.name, uptime_stamp))



@CLIENT.command(name='hugh')
async def hugh(ctx):
    """HWNBABM"""
    url = "https://images-ext-1.discordapp.net/external/SzMDH8nwVukWzN-UmQjiKKi2l_sSmGaiPMgnBC-KHLc/%3Fwidth%3D1246%26height%3D701/https/media.discordapp.net/attachments/826739157309063179/875121225263902760/HUGHbf.png"
    await ctx.send(url)



@CLIENT.command(name='nico',
                aliases=["niconico", "niconiconii"])
async def nico(ctx):
    """https://youtu.be/-_lb--PWEMU?t=26"""
    url = "https://media.discordapp.net/attachments/838595679994511400/859654492877881354/unknown.png"
    await ctx.send(url)



@CLIENT.command(name='triangle',
                aliases=["hannah"])
async def triangle(ctx):
    """The infamous triangle, used to analyze trans issues, also funny meme."""
    url = "https://media.discordapp.net/attachments/826743475143311390/860315076870668299/hannah_moment_refined.png?width=701&height=701"
    await ctx.send(url)
   
    
    
@CLIENT.command(name='jebaited')
async def jebaited(ctx):
    """Jebaited.... :^)"""
    url = "https://media.discordapp.net/attachments/826739157309063179/859930982186352710/irk_jebaited.png?width=1440&height=156"
    await ctx.send(url)
    
    
    
@CLIENT.command(name='nicole')
async def nicole(ctx):
    """
    https://www.youtube.com/watch?v=87K5Uh3AML0, but with me instead :AmberHappy:
    """    
    f = r"media/nicole_nippon.mp3"
    await ctx.send(file=discord.File(f))
    
    

@CLIENT.command(name='transracialism',
                enabled=False)
async def transracialism(ctx):
    """Transracialism weeb meme made by Amber."""
    f = r"media/Destiny_vs._Hugh_Mungus-_The_Power_of_Transracialism_Explodes.mp4"
    await ctx.send(file=discord.File(f))



@CLIENT.command(name='progress')
async def progress(ctx):
    """"Returns what my board for features I'm currently working on! Feel free to submit any issues on my GitHub for new features!"""
    ret = "Returns what my board for features I'm currently working on! Feel free to submit any issues on my GitHub for new features!\n"
    url = "https://github.com/nclgbd/Little-Amber/projects/1"
    await ctx.send("{} {}".format(ret, url))
    
    

@CLIENT.command(name='issues')
async def issues(ctx):   
    """If you ever want to request a command, you can go to my GitHub here and submit an issue. Note that not all issues will be fulfilled, 
    and there's no timeline for when things will be completed. Be sure to keep this in mind when submitting a request."""
    
    string = '''If you ever want to request a command, you can go to my GitHub here and submit an issue. Note that not all issues will be fulfilled, and there's no timeline for when things will be completed. Be sure to keep this in mind when submitting a request.\n'''
    url = "https://github.com/nclgbd/Little-Amber/issues"
    await ctx.send("{} {}".format(string, url))
    
    

@CLIENT.command(name='typing')
async def typing(ctx): 
    '''Amber is typing...'''
    emoji = discord.utils.get(CLIENT.emojis, name="Typing")
    await ctx.send("{} **Amber** is typing...".format(emoji))
    
    
    
@CLIENT.command(name='dimden')
async def dimden(ctx):
    '''Posts dimden.'''
    await ctx.send(await TENOR.arandom('dimden'))
    
    
@CLIENT.command(name='rules')
async def rules(ctx):
    '''Posts the rules of the server. Just kidding.... go to #rules if you want the rules.'''
    url = "https://github.com/nclgbd/Little-Amber/blob/master/media/rules/{}.gif?raw=true".format(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 10]))
    await ctx.send(url)
    
    

### B O O K    C L U B     C O M M A N D S ###

@CLIENT.group(name='bookclub',
              invoke_without_command=True)
async def bookclub(ctx):
    """Book Club is held every Sunday at 1:00PM PST. We typically read books and short stories about history, politics, philosophy, etc. Our reading pace is about 30-50 pages a week, depending on the material. You can sign up for all BC notifications with the "Book Club" role. You can also choose the "Book Club (Waiting)" sign up for notifications only when we are starting a new book or short story. Even if you aren't reading the material, please still feel free to join the Sunday VC sessions just to listen in!"""
    
    string = """Book Club is held **every Sunday at 1:00PM PST**. We typically read books and short stories about history, politics, philosophy, etc. Our reading pace is about 30-50 pages a week, depending on the material. You can sign up for all BC notifications with the "Book Club" role. You can also choose the "Book Club (Waiting)" sign up for notifications only when we are starting a new book or short story. Even if you aren't reading the material, please still feel free to join the Sunday VC sessions just to listen in! For more details about the available commands, use `!help bookclub`"""
    await ctx.send(string)
    


@bookclub.command(name='schedule',
                enabled=False)
async def schedule(ctx):
    pass



@bookclub.command(name='upload')
async def upload(ctx):
    '''Uploads a book to our book club library database. This command is only usable by `Book Club` members.'''
    author_role_names = [ctx.message.author.roles[idx].name for idx in range(len(ctx.message.author.roles))]
    
    try:
        if "Book Club" in author_role_names:
            attachments = ctx.message.attachments[0]
            filename = attachments.filename[:-4]
            url = attachments.url
            book_club.upload_book(attachments)
            
            emoji = discord.utils.get(CLIENT.emojis, name="AmberHappy")
            embed = discord.Embed(title="Upload Successful! {}".format(emoji),
                                  description="Uploading {} was successful, you can download it here:\n{}".format(filename, url),
                                  color=0xff0000,
                                  thumbnail=book_club.icon_url)
            
            await ctx.send(embed=embed)
            
        elif "Book Club" not in author_role_names:
            raise PermissionError()
        
    except PermissionError:
        emoji = discord.utils.get(CLIENT.emojis, name="AmberSad")
        embed = discord.Embed(title="Upload failed. {}".format(emoji),
                            description="Uh oh, the upload failed! Try using `!help upload` for usage instructions.",
                            color=0xff0000,
                            thumbnail=book_club.icon_url)
        
        await ctx.send(embed=embed)
        
    

@bookclub.command(name='reading',
                aliases=["current_reading"])
async def reading(ctx):
    '''Gives the current readings for book club.'''
    
    current_readings = book_club.get_current_readings()
    embed = discord.Embed(title="Current Readings",
                          description="Books we're currently reading for Book Club.",
                          color=0xff0000)
    
    embed.set_thumbnail(url=book_club.icon_url)
    
    for book in current_readings:
        embed.add_field(name=book, value=current_readings[book], inline=False)
        
    await ctx.send(embed=embed)
    
    
    
@bookclub.command(name='toggle',
                aliases=["toggle_reading"])
async def toggle_reading(ctx):
    '''Removes a book from the current reading list. This command is only usable by Café Maids members.'''
    author_role_names = [ctx.message.author.roles[idx].name for idx in range(len(ctx.message.author.roles))]
    book_name = ctx.message.content.split()[2]
    
    try:
        if "Café Maid" in author_role_names:
            
            current_book = book_club.books[book_name]
            book_club.set_current_reading(book_name, is_current_reading=not current_book["current_reading"])
            
            emoji = discord.utils.get(CLIENT.emojis, name="AmberHappy")
            embed = discord.Embed(title="Toggle Successful! {}".format(emoji),
                                  description="Toggle of `{}` was successful, currently set to `{}`!".format(book_name, 
                                                                                                         book_club.books[book_name]["current_reading"]),
                                  color=0xff0000,
                                  thumbnail=book_club.icon_url)
            embed.set_thumbnail(url=book_club.icon_url)
            
            await ctx.send(embed=embed)
            
        elif "Café Maid" not in author_role_names:
            
            emoji = discord.utils.get(CLIENT.emojis, name="AmberSad")
            embed = discord.Embed(title="Toggle failed. {}".format(emoji),
                                description="Uh oh, the toggling of `{}` failed! Try using `!help toggle` for usage instructions.".format(book_name),
                                color=0xff0000,
                                thumbnail=book_club.icon_url)
            embed.set_thumbnail(url=book_club.icon_url)
            
            await ctx.send(embed=embed)
        
        
    except discord.ext.commands.errors.CommandInvokeError:
        
        emoji = discord.utils.get(CLIENT.emojis, name="AmberSad")
        embed = discord.Embed(title="Toggle failed. {}".format(emoji),
                            description="Uh oh, the toggling of `{}` failed! Try using `!help toggle` for usage instructions.".format(book_name),
                            color=0xff0000,
                            thumbnail=book_club.icon_url)
        embed.set_thumbnail(url=book_club.icon_url)
        
        await ctx.send(embed=embed)



@bookclub.command(name='delete',
                aliases=["delete_reading"])
async def delete_reading(ctx):
    '''Removes a book to our book club library database. This command is only usable by Café Maids members.'''
    author_role_names = [ctx.message.author.roles[idx].name for idx in range(len(ctx.message.author.roles))]
    book_name = ctx.message.content.split()[2]
    
    try:
        if "Café Maid" in author_role_names:
            
            book_club.remove_book(book_name)
            
            emoji = discord.utils.get(CLIENT.emojis, name="AmberHappy")
            embed = discord.Embed(title="Deletion Successful! {}".format(emoji),
                                  description="Deletion of `{}` was successful!".format(book_name),
                                  color=0xff0000,
                                  thumbnail=book_club.icon_url)
            embed.set_thumbnail(url=book_club.icon_url)
            
            await ctx.send(embed=embed)
            
        elif "Café Maid" not in author_role_names:
            raise PermissionError()
        
        
    except PermissionError:
        emoji = discord.utils.get(CLIENT.emojis, name="AmberSad")
        embed = discord.Embed(title="Deletion failed. {}".format(emoji),
                            description="Uh oh, the deletion of `{}` failed! Try using `!help delete` for usage instructions.".format(book_name),
                            color=0xff0000,
                            thumbnail=book_club.icon_url)
        
        await ctx.send(embed=embed)
    
             
CLIENT.run(TOKEN)



# async def time_check():
#     await CLIENT.wait_until_ready()
#     while not CLIENT.is_closed:
#         channel = CLIENT.get_channel(CHANNEL_MAPPING["bot-testing"])
#         messages = ('Test')
#         f = '%H:%M'

#         now = datetime.strftime(datetime.now(), f)
#         # get the difference between the alarm time and now
#         diff = (datetime.strptime(ALARM_TIME, f) - datetime.strptime(now, f)).total_seconds()

#         # create a scheduler
#         s = sched.scheduler(time.perf_counter, time.sleep)
#         # arguments being passed to the function being called in s.enter
#         args = (CLIENT.send_message(channel, message), )
#         # enter the command and arguments into the scheduler
#         s.enter(seconds, 1, CLIENT.loop.create_task, args)
#         s.run() # run the scheduler, will block the event loop


# CLIENT.loop.create_task(time_check())
