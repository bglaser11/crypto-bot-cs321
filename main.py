import os

import discord
from coinbase.wallet.client import Client
from discord.ext import commands
from dotenv import load_dotenv
from bookmarks import bookmarks

import chartGenerator

load_dotenv()

bot = commands.Bot(command_prefix = '$')
coinbaseClient = Client(os.environ['COINBASE_KEY'], os.environ['COINBASE_SECRET'], api_version='2021-10-25')

@bot.event
async def on_ready():
    print('logged in as {.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong {bot.latency:.0f}')

@bot.command()
async def price(ctx, base):
    try:
        price = coinbaseClient.get_spot_price(currency_pair='{}-USD'.format(base))
        await ctx.send('current price of {} in USD is ${:.2f}'.format(base, float(price.amount)))
    except Exception as e:
        await ctx.send(e)

"""
Command: myBookmarks
returns: list of bookmarks and their price
"""
@bot.command()
async def myBookmarks(ctx):
  try:
    list = bookmarks(ctx.message.author.id)
    currencies = list.getBookmark()
    result = "Bookmarks:"
    for curr in currencies:
      price = coinbaseClient.get_spot_price(currency_pair='{}-USD'.format(curr))
      priceString = "$" + str(price.amount)
      result += "\n" + curr + ": " + priceString

    await ctx.send(result)
  except Exception as e:
        await ctx.send(e)

"""
Command: bookmark
paramters: base (cryptocurrency)
returns: if add was successful
"""
@bot.command()
async def bookmark(ctx, base):
  try:
    list = bookmarks(ctx.message.author.id)
    result = list.addBookmark(str(base))
    await ctx.send(result)
  except Exception as e:
        await ctx.send(e)

"""
Command: removeBookmark
paramters: base (cryptocurrency)
returns: if remove was successful
"""
@bot.command()
async def removeBookmark(ctx, base):
  try:
    list = bookmarks(ctx.message.author.id)
    result = list.removeBookmark(str(base))
    await ctx.send(result)
  except Exception as e:
        await ctx.send(e)



#Generates a chart of the price of a chosen cryptocurrency in a chosen currency using chart.py's generateChart function
#Two args: cryptocurrency's abbreviation and currency's abbreviation
@bot.command()
async def chart(ctx, base, currency='USD'):
    chartGenerator.generateChart(base, currency)
    await ctx.send(file = discord.File('chart.png'))

    os.remove('chart.svg')
    os.remove('chart.png')

    #call "$help chart" on bad input?

# exception handler for incorrect input
@bot.event
async def on_command_error(ctx, err):
  await ctx.send("There is a problem with your command. Please check help for more details.") 

bot.run(os.environ['DISCORD_TOKEN'])
