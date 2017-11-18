from lxml import html
from datetime import datetime, timedelta
import requests

symbols = ['DJIA', 'RUA', 'GSPC', 'SP500']
base_date = datetime(2017, 4, 28)


def get_quote(symbol, date):
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


def get_quote_change(current_quote, compare_quote):
    if current_quote and compare_quote:
        percent_change = (current_quote['Closing Price'] / compare_quote['Closing Price'] - 1) * 100
        return round(percent_change, 2)


for symbol in symbols:
    current_quote = get_quote(symbol, base_date)
    year_quote = get_quote(symbol, base_date - timedelta(weeks=52))
    six_month_quote = get_quote(symbol, base_date - timedelta(weeks=26))
    price_change_6m = get_quote_change(current_quote, six_month_quote)
    price_change_1y = get_quote_change(current_quote, year_quote)
    print(current_quote)
    print(six_month_quote)
    print(year_quote)
    print('{0} - {1}% change in value'.format(symbol, price_change_6m))
    print('{0} - {1}% change in value'.format(symbol, price_change_1y))
