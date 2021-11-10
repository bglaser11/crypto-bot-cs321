import os
import discord
from discord.ext import commands, context
from coinbase.wallet.client import Client
from dotenv import load_dotenv
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

#Generates a chart of the price of a chosen cryptocurrency in a chosen currency using chart.py's generateChart function
#Two args: cryptocurrency's abbreviation and currency's abbreviation
@bot.command()
async def chart(ctx, base, currency='USD'):
    chartGenerator.generateChart(base, currency)
    await ctx.send(file = discord.File('chart.png'))

    os.remove('chart.svg')
    os.remove('chart.png')

    #call "$help chart" on bad input?

bot.run(os.environ['DISCORD_TOKEN'])
