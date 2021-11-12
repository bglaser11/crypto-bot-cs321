import os
import datetime
import re
import pygal
from pygal.style import NeonStyle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject
from dotenv import load_dotenv
load_dotenv()

coinbaseClient = Client(os.environ['COINBASE_KEY'], os.environ['COINBASE_SECRET'], api_version='2021-10-25')

#Generates a chart of the price of a chosen cryptocurrency in a chosen currency
#Two args: cryptocurrency's abbreviation and currency's abbreviation
def generateChart(base, currency='USD'):
    historicalPricesObject = coinbaseClient._make_api_object(coinbaseClient._get('v2', 'prices', '{}-{}'.format(base,currency), 'historic'), APIObject)
    historicalPrices, times = [float(n.price) for n in historicalPricesObject.prices], [n.time for n in historicalPricesObject.prices]

    datetimes = []
    for s in times:
        values = [int(n) for n in re.split(r'\D',s) if n] #chops date values into list using non-numbers
        datetimes.insert(0, datetime.datetime(values[0],values[1],values[2],(values[3]),values[4],values[5]))#Y,M,D,H,M,S

    chart = pygal.Line(style = NeonStyle, x_labels_major_every = 50, show_minor_x_labels = False, truncate_label = -1, show_legend = False)
    chart.title = 'Price of {} in {} over the past hour (in UTC)'.format(base,currency)
    chart.x_labels = [d.strftime('%I:%M:%S %p') for d in datetimes]
    chart.add('', [n for n in historicalPrices], show_dots = False)
    chart.render_to_file('chart.svg')
    drawing = svg2rlg('chart.svg')
    renderPM.drawToFile(drawing, 'chart.png', fmt='PNG')
