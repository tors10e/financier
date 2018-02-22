from lxml import html
from datetime import datetime, timedelta
import requests

equity_symbols = [
    ['DJIA', 'Dow',''],
    ['ru50', 'Russel top 50', ' measures the performance of the largest companies in the Russell 3000 Index'],
    ['RUA', 'Russell 3000', 'Total stock market index'],
    ['rmcc', 'Russell Midcap', 'Mid cap index'],
    ['rut', 'Russell 2000', 'Small cap index'],
    ['GSPC','',''],
    ['SP500', 'S&P 500', 'Large capitilization stocks']
]
fixed_symbols = [
    ['UST', 'UST',''],
    ['shm', "Barclay's short term municipal bond",''],
    ['VBMFX', ' Vanguard Total Bond Market Index Fund', "Replica of Bloomberg Barclays US Aggregate Bond Index"]
]

index_symbols = [['XIUSA000MC']]
# base_date = datetime.now()
base_date = datetime(2018, 1, 31)


def get_quote(symbol, range='current'):
    """
    Gets the quote given a symbol and a range
    :param symbol: stock quote
    :param range: current, 1m, 6m .1y, 5y, 10y
"""

    # todo: Consider using https://api.iextrading.com/1.0/stock/aapl/batch?types=quote,news,chart&range=1m&last=10
    date = f(range)
    url = 'http://bigcharts.marketwatch.com/historical/default.asp?symb={0}&closeDate={1}%2F{2}%2F{3}' \
        .format(symbol, date.month, date.day, str(date.year)[2:])
    page = requests.get(url)
    tree = html.fromstring(page.content)
    elements = tree.xpath('//table[@id="historicalquote"]/tr/td/text()')
    values = []

    # Extract numeric td elements into new list.
    for e in elements:
        try:
            values.append(float(e.replace(',', '')))
        except:
            pass

    # Get headers
    headings = elements = tree.xpath('//table[@id="historicalquote"]/tr/th/text()')

    # Process both lists simultaneously
    quote = {}
    for h, v in zip(headings, values):
        quote.update({h.replace(':', ''): v})

    return quote


def get_index_quote(symbol, range='current'):
    """
    Gets the quote given a symbol and a range
    :param symbol: stock quote
    :param range: current, 1m, 6m .1y, 5y, 10y
"""

    # todo: Consider using https://api.iextrading.com/1.0/stock/aapl/batch?types=quote,news,chart&range=1m&last=10
    date = f(range)
    url = 'http://performance.morningstar.com/Performance/index-c/performance-return.action?t={0}' \
        .format(symbol)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    elements = tree.xpath('//table[@class="r_table3  width955px print97"]/tbody')
    values = []

    # Extract numeric td elements into new list.
    for e in elements:
        try:
            values.append(float(e.replace(',', '')))
        except:
            pass

    # Get headers
    headings = elements = tree.xpath('//table[@id="historicalquote"]/tr/th/text()')

    # Process both lists simultaneously
    quote = {}
    for h, v in zip(headings, values):
        quote.update({h.replace(':', ''): v})

    return quote


# def get_fixed_quote(symbol, date= ):
#     url = 'https://www.marketwatch.com/investing/future/gcj8/historical'
#


def f(x):
    return {
        'current': base_date,
        '1m': base_date - timedelta(weeks=4),
        '6m': base_date - timedelta(weeks=26),
        '1y': base_date - timedelta(weeks=52),
        '5y': base_date - timedelta(weeks=260),
        '10y': base_date - timedelta(weeks=520),
    }.get(x, base_date)


def get_quote_change(current_quote, compare_quote):
    if current_quote and compare_quote:
        percent_change = (current_quote['Closing Price'] / compare_quote['Closing Price'] - 1) * 100
        return round(percent_change, 2)


print("Using {0} as base date".format(base_date))
for symbol in equity_symbols:
    current_quote = get_quote(symbol[0], 'current')
    price_change_1m = get_quote_change(current_quote, get_quote(symbol[0], '1m'))
    price_change_6m = get_quote_change(current_quote, get_quote(symbol[0], '6m'))
    price_change_1y = get_quote_change(current_quote, get_quote(symbol[0], '1y'))
    price_change_5y = get_quote_change(current_quote, get_quote(symbol[0], '5y'))

    print("******* Equity Benchmark - {0} - {1} *******".format(symbol[1], symbol[2]))
    print('{0}% 1 month change in value'.format(price_change_1m))
    print('{0}% 6 month change in value'.format(price_change_6m))
    print('{0}% 1 year change in value'.format(price_change_1y))
    print('{0}% 5 year change in value'.format(price_change_5y))
    print()

for symbol in fixed_symbols:
    current_quote = get_quote(symbol[0], 'current')
    price_change_1m = get_quote_change(current_quote, get_quote(symbol[0], '1m'))
    price_change_6m = get_quote_change(current_quote, get_quote(symbol[0], '6m'))
    price_change_1y = get_quote_change(current_quote, get_quote(symbol[0], '1y'))
    price_change_5y = get_quote_change(current_quote, get_quote(symbol[0], '5y'))

    print("******* Fixed Income and Commodity Benchmark - {0} - {1} *******".format(symbol[1], symbol[2]))
    print('{0}% 1 month change in value'.format(price_change_1m))
    print('{0}% 6 month change in value'.format(price_change_6m))
    print('{0}% 1 year change in value'.format(price_change_1y))
    print('{0}% 5 year change in value'.format(price_change_5y))
    print()


# for symbol in index_symbols:
#     current_quote = get_quote(symbol[0], 'current')
#     price_change_1m = get_quote_change(current_quote, get_index_quote(symbol[0], '1m'))
#     price_change_6m = get_quote_change(current_quote, get_index_quote(symbol[0], '6m'))
#     price_change_1y = get_quote_change(current_quote, get_index_quote(symbol[0], '1y'))
#     price_change_5y = get_quote_change(current_quote, get_index_quote(symbol[0], '5y'))
#
#     print("******* Fixed Income and Commodity Benchmark - {0} - {1} *******".format(symbol[1], symbol[2]))
#     print('{0}% 1 month change in value'.format(price_change_1m))
#     print('{0}% 6 month change in value'.format(price_change_6m))
#     print('{0}% 1 year change in value'.format(price_change_1y))
#     print('{0}% 5 year change in value'.format(price_change_5y))
#     print()