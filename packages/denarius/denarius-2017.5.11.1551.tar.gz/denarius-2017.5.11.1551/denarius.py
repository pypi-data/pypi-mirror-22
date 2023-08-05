# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# denarius                                                                     #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides currency and other utilities.                          #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

from __future__ import division

name    = "denarius"
version = "2017-05-11T1551Z"

import ast
import datetime
import json
import time
import urllib2

import currency_converter
import dataset
import datavision
import numpy
import pandas as pd
import pyprel
import shijian

def value_Bitcoin(
    price    = "last",
    currency = "EUR"
    ):

    return ticker_Bitcoin(
        currency = currency
    )[price]

    if day:
        URL = URL_day
    if hour:
        URL = URL_hour

    # Access a Bitcoin ticker.
    file_URL                = urllib2.urlopen(URL)
    data_string             = file_URL.read()
    # Convert the data from string to dictionary.
    data_dictionary_strings = ast.literal_eval(data_string)
    #
    #    example hour ticker:
    #    {
    #        'ask':       999.31,
    #        'bid':       998.01,
    #        'high':      1000.6,
    #        'last':      999.31,
    #        'low':       996.67,
    #        'open':      990.0,
    #        'timestamp': 1487600377.0,
    #        'volume':    21.11748617,
    #        'vwap':      998.34
    #    }
    #
    #    example day ticker:
    #    {
    #        'ask':       999.31,
    #        'bid':       998.01,
    #        'high':      1004.0,
    #        'last':      999.31,
    #        'low':       985.31,
    #        'open':      990.0,
    #        'timestamp': 1487600340.0,
    #        'volume':    324.21451971,
    #        'vwap':      996.27
    #    }
    #
    # Convert numbers from strings to floats.
    data_dictionary = dict()
    for key in data_dictionary_strings:
        data_dictionary[key] = float(data_dictionary_strings[key])
    if currency != "EUR":
        # Convert currency EUR to requested currency.
        data_dictionary_currency = dict()
        converter_currency = currency_converter.CurrencyConverter()
        for key in data_dictionary:
            if key == "timestamp":
                data_dictionary_currency[key] = data_dictionary[key]
            else:
                data_dictionary_currency[key] =\
                    converter_currency.convert(
                        data_dictionary_strings[key],
                        "EUR",
                        currency
                    )
        return data_dictionary_currency
    return data_dictionary

def fluctuation_value_Bitcoin(
    days                      = 5,
    factor_standard_deviation = 1.6,
    details                   = False
    ):

    data_Bitcoin = data_historical_Bitcoin(
        days        = days,
        return_list = True
    )
    value_current_Bitcoin = value_Bitcoin()
    values_Bitcoin = [float(element[1]) for element in data_Bitcoin]
    mean_Bitcoin               = numpy.array(values_Bitcoin).mean()
    standard_deviation_Bitcoin = numpy.array(values_Bitcoin).std()
    low_Bitcoin  =\
        mean_Bitcoin - factor_standard_deviation * standard_deviation_Bitcoin
    high_Bitcoin =\
        mean_Bitcoin + factor_standard_deviation * standard_deviation_Bitcoin

    if details:
        print("Bitcoin values from last {days} days:\n\n{values}\n".format(
            days   = days,
            values = ", ".join([str(element) for element in values_Bitcoin])
        ))
        print("high bound Bitcoin:    {value}".format(value = high_Bitcoin))
        print("Bitcoin current value: {value}".format(
            value = value_current_Bitcoin
        ))
        print("low bound Bitcoin:     {value}".format(value = low_Bitcoin))

    if low_Bitcoin <= value_current_Bitcoin <= high_Bitcoin:
        return False
    else:
        return True

def fluctuation_value_LocalBitcoins(
    days                            = 3,
    factor_standard_deviation       = 1.6,
    details                         = False,
    filename_database_LocalBitcoins = "database_LocalBitcoins.db",
    ):

    datetime_time_start = datetime.datetime.utcnow() - datetime.timedelta(days = days)

    # get last few days of LocalBitcoins values from database
    values_LocalBitcoins = []
    database_LocalBitcoins = access_database(filename = filename_database_LocalBitcoins)
    for row in database_LocalBitcoins["LocalBitcoins"]:
        row_time = datetime.datetime.fromtimestamp(row["time_UNIX"])
        if row_time >= datetime_time_start:
            values_LocalBitcoins.append(ast.literal_eval(row["values_GBP"])[0])
    # reverse order so latest first
    values_LocalBitcoins = values_LocalBitcoins[::-1]

    # current value
    value_current_LocalBitcoins = values_Bitcoin_LocalBitcoin()[0]

    mean_Bitcoin               = numpy.array(values_LocalBitcoins).mean()
    standard_deviation_Bitcoin = numpy.array(values_LocalBitcoins).std()
    low_Bitcoin  =\
        mean_Bitcoin - factor_standard_deviation * standard_deviation_Bitcoin
    high_Bitcoin =\
        mean_Bitcoin + factor_standard_deviation * standard_deviation_Bitcoin
    
    if details:
        print("high bound LocalBitcoins:    {value}".format(value = high_Bitcoin))
        print("LocalBitcoins current value: {value}".format(
            value = value_current_LocalBitcoins
        ))
        print("low bound LocalBitcoins:     {value}".format(value = low_Bitcoin))
    
    if low_Bitcoin <= value_current_LocalBitcoins <= high_Bitcoin:
        return False
    else:
        return True

def value_prediction_linear_Bitcoin(
    days_past   = 5, # past days data from which prediction is made
    days_future = 2, # number of days from now at which to predict value
    currency    = "EUR"
    ):

    data_Bitcoin = data_historical_Bitcoin(
        currency    = currency,
        days        = days_past,
        return_list = True
    )

    values_Bitcoin = [float(element[1]) for element in data_Bitcoin]
    data = [[day, value] for day, value in zip(range(-days_past, 0), values_Bitcoin)]

    model_values = shijian.model_linear(data = data)
    b0 = model_values[0]
    b1 = model_values[1]
    x = days_future
    y = b0 + b1 * x

    return y

def ticker_Bitcoin(
    URL_hour = "https://www.bitstamp.net/api/v2/ticker/btceur",
    URL_day  = "https://www.bitstamp.net/api/v2/ticker_hour/btceur",
    currency = "EUR",
    hour     = True,
    day      = False
    ):

    if day:
        URL = URL_day
    if hour:
        URL = URL_hour

    # Access a Bitcoin ticker.
    file_URL                = urllib2.urlopen(URL)
    data_string             = file_URL.read()
    # Convert the data from string to dictionary.
    data_dictionary_strings = ast.literal_eval(data_string)
    #
    #    example hour ticker:
    #    {
    #        'ask':       999.31,
    #        'bid':       998.01,
    #        'high':      1000.6,
    #        'last':      999.31,
    #        'low':       996.67,
    #        'open':      990.0,
    #        'timestamp': 1487600377.0,
    #        'volume':    21.11748617,
    #        'vwap':      998.34
    #    }
    #
    #    example day ticker:
    #    {
    #        'ask':       999.31,
    #        'bid':       998.01,
    #        'high':      1004.0,
    #        'last':      999.31,
    #        'low':       985.31,
    #        'open':      990.0,
    #        'timestamp': 1487600340.0,
    #        'volume':    324.21451971,
    #        'vwap':      996.27
    #    }
    #
    # Convert numbers from strings to floats.
    data_dictionary = dict()
    for key in data_dictionary_strings:
        data_dictionary[key] = float(data_dictionary_strings[key])
    if currency != "EUR":
        # Convert currency EUR to requested currency.
        data_dictionary_currency = dict()
        converter_currency = currency_converter.CurrencyConverter()
        for key in data_dictionary:
            if key == "timestamp":
                data_dictionary_currency[key] = data_dictionary[key]
            else:
                data_dictionary_currency[key] =\
                    converter_currency.convert(
                        data_dictionary_strings[key],
                        "EUR",
                        currency
                    )
        return data_dictionary_currency
    return data_dictionary

def data_historical_Bitcoin(
    URL               = "https://api.coindesk.com/v1/bpi/historical/close.json",
    currency          = "EUR",
    date_start        = None, # YYYY-MM-DD
    date_stop         = None, # YYYY-MM-DD
    days              = None, # last days (start/stop dates alternative)
    return_list       = False,
    return_UNIX_times = False,
    sort_reverse      = False
    ):

    if days:
        time_current = datetime.datetime.utcnow()
        date_stop    = time_current.strftime("%Y-%m-%d")
        date_start   = (time_current -\
                       datetime.timedelta(days = days)).strftime("%Y-%m-%d")
    # Construct the URL using the API (http://www.coindesk.com/api/).
    URL = URL + "?currency=" + currency
    if date_start is not None and date_stop is not None:
        URL = URL + "&start=" + date_start + "&end=" + date_stop
    # Access the online data.
    file_URL                = urllib2.urlopen(URL)
    data_string             = file_URL.read()
    # Convert the data from string to dictionary.
    data_dictionary_strings = ast.literal_eval(data_string)

    if return_list or return_UNIX_times:
        data_dictionary_list = list()
        for key in data_dictionary_strings["bpi"]:
            if return_UNIX_times:
                date = int(
                    time.mktime(
                        datetime.datetime.strptime(
                            key,
                            "%Y-%m-%d"
                        ).timetuple()
                    )
                )
            else:
                date = key
            data_dictionary_list.append(
                [date, float(data_dictionary_strings["bpi"][key])]
            )
        # sort
        data_dictionary_list_tmp = sorted(
            data_dictionary_list,
            key = lambda data_dictionary_list: (
                      data_dictionary_list[0],
                      data_dictionary_list[1]
                  ),
            reverse = sort_reverse
        )
        data_dictionary_list = data_dictionary_list_tmp
        return data_dictionary_list
    else:
        return data_dictionary_strings

def table_Bitcoin(
    currency   = "EUR",
    date_start = None, # YYYY-MM-DD
    date_stop  = None, # YYYY-MM-DD
    UNIX_times = False
    ):

    # Get Bitcoin value data.
    data = data_historical_Bitcoin(
        currency          = currency,
        date_start        = None, # YYYY-MM-DD
        date_stop         = None, # YYYY-MM-DD
        return_UNIX_times = UNIX_times,
        return_list       = True
    )
    
    # Return a table of the Bitcoin value data.
    table_contents = [[
                         "time",
                         "Bitcoin value ({currency})".format(
                             currency = currency
                         )
                     ]]
    table_contents.extend(data)
    table = pyprel.Table(
                contents = table_contents
            )
    return table

def save_graph_Bitcoin(
    currency   = "EUR",
    filename   = None,
    directory  = ".",
    overwrite  = True,
    date_start = None, # YYYY-MM-DD
    date_stop  = None, # YYYY-MM-DD
    days       = None  # last days (start/stop dates alternative)
    ):

    if filename is None:
        filename = "Bitcoin_value_{currency}_versus_time.png".format(
            currency = currency
        )

    data = data_historical_Bitcoin(
        currency          = currency,
        date_start        = date_start, # YYYY-MM-DD
        date_stop         = date_stop,  # YYYY-MM-DD
        days              = days,
        return_UNIX_times = True
    )

    datavision.save_graph_matplotlib(
        values       = data,
        title_axis_x = "time",
        title_axis_y = "value ({currency})".format(
                           currency = currency
                       ),
        filename     = filename,
        directory    = directory,
        overwrite    = overwrite,
        line         = True,
        line_width   = 0.5,
        time_axis_x  = True
    )

def save_graph_LocalBitcoins(
    filename          = None,
    directory         = ".",
    overwrite         = True,
    filename_database = "database_LocalBitcoins.db"
    ):

    if filename is None:
        filename = "LocalBitcoins_Bitcoin_lowest_price_GBP_versus_time.png"

    database = access_database(filename = filename_database)

    data = []
    for row in database["LocalBitcoins"]:
        data.append([row["time_UNIX"], ast.literal_eval(row["values_GBP"])[0]])

    datavision.save_graph_matplotlib(
        values       = data,
        title_axis_x = "time",
        title_axis_y = "LBC low (GBP)",
        filename     = filename,
        directory    = directory,
        overwrite    = overwrite,
        line         = True,
        line_width   = 0.5,
        time_axis_x  = True,
        time_style   = "%Y-%m-%dT%H%MZ", # e.g. "%Y-%m-%d", "%Y-%m-%dT%H%MZ",
        font_size    = 8
    )

def save_graph_Bitcoin_LocalBitcoins(
    filename                        = "Bitcoin_LocalBitcoins_lowest_price_GBP.png",
    directory                       = ".",
    overwrite                       = True,
    filename_database_Bitcoin       = "database_Bitcoin_GBP.db",
    filename_database_LocalBitcoins = "database_LocalBitcoins.db",
    time_start                      = "2017-03-08T1436Z" # YYYY-MM-DDTHHMMZ
    ):

    """
    Save a graph of Bitcoin GBP values versus LocalBitcoins lowest GBP values.
    """

    x_Bitcoin       = []
    y_Bitcoin       = []
    x_LocalBitcoins = []
    y_LocalBitcoins = []

    database_Bitcoin       = access_database(filename = filename_database_Bitcoin)
    database_LocalBitcoins = access_database(filename = filename_database_LocalBitcoins)

    datetime_time_start = datetime.datetime.strptime(time_start, "%Y-%m-%dT%H%MZ")

    for row in database_Bitcoin["Bitcoin"]:
        row_time = datetime.datetime.fromtimestamp(row["time"]) + datetime.timedelta(hours = 24)
        if row_time >= datetime_time_start:
            x_Bitcoin.append(row_time)
            y_Bitcoin.append(row["value"])

    for row in database_LocalBitcoins["LocalBitcoins"]:
        row_time = datetime.datetime.fromtimestamp(row["time_UNIX"])
        if row_time >= datetime_time_start:
            x_LocalBitcoins.append(row_time)
            y_LocalBitcoins.append(ast.literal_eval(row["values_GBP"])[0])

    datavision.save_multigraph_2D_matplotlib(
        variables_x      = [x_Bitcoin, x_LocalBitcoins],
        variables_y      = [y_Bitcoin, y_LocalBitcoins],
        variables_names  = ["Bitcoin", "LocalBitcoins"],
        title            = "Bitcoin values versus LocalBitcoins lowest price",
        title_axis_x     = "time",
        title_axis_y     = "Bitcoin value (GBP)",
        filename         = filename,
        directory        = directory,
        overwrite        = overwrite,
        LaTeX            = False,
        markers          = False,
        marker_size      = 0.8,
        line             = True,
        line_width       = 0.5,
        palette_name     = "palette1",
        time_axis_x      = True,
        time_style       = "%Y-%m-%d",
        font_size        = 10
    )

def save_graphs_Bitcoin_LocalBitcoins(
    filename                        = "Bitcoin_LocalBitcoins_prices_GBP.png",
    directory                       = ".",
    overwrite                       = True,
    filename_database_Bitcoin       = "database_Bitcoin_GBP.db",
    filename_database_LocalBitcoins = "database_LocalBitcoins.db",
    time_start                      = "2017-03-08T1436Z" # YYYY-MM-DDTHHMMZ
    ):

    """
    Save a graph of the LocalBitcoins 5 lowest GBP values and Bitcoin value.
    """

    x_Bitcoin         = []
    y_Bitcoin         = []

    x_LocalBitcoins_1 = []
    y_LocalBitcoins_1 = []

    x_LocalBitcoins_2 = []
    y_LocalBitcoins_2 = []

    x_LocalBitcoins_3 = []
    y_LocalBitcoins_3 = []

    x_LocalBitcoins_4 = []
    y_LocalBitcoins_4 = []

    x_LocalBitcoins_5 = []
    y_LocalBitcoins_5 = []

    database_Bitcoin       = access_database(filename = filename_database_Bitcoin)
    database_LocalBitcoins = access_database(filename = filename_database_LocalBitcoins)

    datetime_time_start = datetime.datetime.strptime(time_start, "%Y-%m-%dT%H%MZ")

    for row in database_Bitcoin["Bitcoin"]:
        row_time = datetime.datetime.fromtimestamp(row["time"]) + datetime.timedelta(hours = 24)
        if row_time >= datetime_time_start:
            x_Bitcoin.append(row_time)
            y_Bitcoin.append(row["value"])

    for row in database_LocalBitcoins["LocalBitcoins"]:
        row_time = datetime.datetime.fromtimestamp(row["time_UNIX"])
        if row_time >= datetime_time_start:
            x_LocalBitcoins_1.append(row_time)
            y_LocalBitcoins_1.append(ast.literal_eval(row["values_GBP"])[0])

    for row in database_LocalBitcoins["LocalBitcoins"]:
        row_time = datetime.datetime.fromtimestamp(row["time_UNIX"])
        if row_time >= datetime_time_start:
            x_LocalBitcoins_2.append(row_time)
            y_LocalBitcoins_2.append(ast.literal_eval(row["values_GBP"])[1])

    for row in database_LocalBitcoins["LocalBitcoins"]:
        row_time = datetime.datetime.fromtimestamp(row["time_UNIX"])
        if row_time >= datetime_time_start:
            x_LocalBitcoins_3.append(row_time)
            y_LocalBitcoins_3.append(ast.literal_eval(row["values_GBP"])[2])

    for row in database_LocalBitcoins["LocalBitcoins"]:
        row_time = datetime.datetime.fromtimestamp(row["time_UNIX"])
        if row_time >= datetime_time_start:
            x_LocalBitcoins_4.append(row_time)
            y_LocalBitcoins_4.append(ast.literal_eval(row["values_GBP"])[3])

    for row in database_LocalBitcoins["LocalBitcoins"]:
        row_time = datetime.datetime.fromtimestamp(row["time_UNIX"])
        if row_time >= datetime_time_start:
            x_LocalBitcoins_5.append(row_time)
            y_LocalBitcoins_5.append(ast.literal_eval(row["values_GBP"])[4])

    datavision.save_multigraph_2D_matplotlib(
        variables_x      = [
                           x_Bitcoin,
                           x_LocalBitcoins_1,
                           x_LocalBitcoins_2,
                           x_LocalBitcoins_3,
                           x_LocalBitcoins_4,
                           x_LocalBitcoins_5
                           ],
        variables_y      = [
                           y_Bitcoin,
                           y_LocalBitcoins_1,
                           y_LocalBitcoins_2,
                           y_LocalBitcoins_3,
                           y_LocalBitcoins_4,
                           y_LocalBitcoins_5
                           ],
        variables_names  = [
                           "Bitcoin",
                           "LocalBitcoins 1",
                           "LocalBitcoins 2",
                           "LocalBitcoins 3",
                           "LocalBitcoins 4",
                           "LocalBitcoins 5"
                           ],
        title            = "Bitcoin value versus LocalBitcoins lowest prices",
        title_axis_x     = "time",
        title_axis_y     = "Bitcoin value (GBP)",
        filename         = filename,
        directory        = directory,
        overwrite        = overwrite,
        LaTeX            = False,
        markers          = False,
        marker_size      = 0.8,
        line             = True,
        line_width       = 0.3,
        palette_name     = "palette1",
        time_axis_x      = True,
        time_style       = "%Y-%m-%d",
        font_size        = 10
    )

def save_graph_LocalBitcoins_days(
    filename          = None,
    directory         = ".",
    overwrite         = True,
    filename_database = "database_LocalBitcoins.db"
    ):

    if filename is None:
        filename = "LocalBitcoins_Bitcoin_lowest_price_GBP_days.png"

    database = access_database(filename = filename_database)

    data_datetime         = []
    data_time_through_day = []
    data_value            = []
    for row in database["LocalBitcoins"]:
        time_row = datetime.datetime.fromtimestamp(row["time_UNIX"])
        time_through_day =\
            time_row -\
            datetime.datetime.combine(time_row.date(), datetime.time())
        data_datetime.append(time_row)
        data_time_through_day.append((time_through_day.seconds / 86400) * 24)
        data_value.append(ast.literal_eval(row["values_GBP"])[0])

    data                         = pd.DataFrame()
    data["value"]                = data_value
    data["time_through_day"]     = data_time_through_day
    data.index                   = data_datetime
    data.index.name              = "datetime"
    data["value_day_normalized"] = data["value"].div(data.resample("D")["value"].transform("sum"))

    # trim
    data_plot = []
    for data_time_through_day, data_value in zip(data["time_through_day"], data["value_day_normalized"]):
        if data_value < 0.025:
            data_plot.append([data_time_through_day, data_value])

    #data_plot = [[data_time_through_day, data_value] for data_time_through_day, data_value in zip(data["time_through_day"], data["value_day_normalized"])]

    datavision.save_graph_matplotlib(
        values       = data_plot,
        title_axis_x = "time (hours)",
        title_axis_y = "LBC low (GBP, normalised to unity)",
        filename     = filename,
        directory    = directory,
        overwrite    = overwrite,
        line         = False,
        line_width   = 0.5,
        #time_axis_x  = True,
        #time_style   = "%H%MZ", # e.g. "%Y-%m-%d", "%Y-%m-%dT%H%MZ",
        font_size    = 8,
        marker_size  = 2
    )

def graph_TTY_Bitcoin(
    currency   = "EUR",
    date_start = None, # YYYY-MM-DD
    date_stop  = None, # YYYY-MM-DD
    days       = None  # last days (start/stop dates alternative)
    ):

    data = data_historical_Bitcoin(
        currency          = currency,
        date_start        = date_start, # YYYY-MM-DD
        date_stop         = date_stop,  # YYYY-MM-DD
        days              = days,
        return_UNIX_times = True
    )
    x = [element[0] for element in data]
    y = [element[1] for element in data]
    plot = datavision.TTYFigure()
    tmp = plot.plot(
        x,
        y,
        marker = "_o",
        plot_slope = False
    )
    return tmp

def create_database(
    filename = None
    ):

    os.system(
        "sqlite3 " + \
        filename + \
        " \"create table aTable(field1 int); drop table aTable;\""
    )

def access_database(
    filename = "database.db"
    ):

    database = dataset.connect("sqlite:///" + str(filename))
    return database

def save_database_Bitcoin(
    filename   = "database_Bitcoin.db",
    currency   = "EUR",
    date_start = "2010-07-17",
    date_stop  = None
    ):

    if date_stop is None:
        date_stop = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    data = data_historical_Bitcoin(
        currency          = currency,
        date_start        = date_start,
        date_stop         = date_stop,
        return_list       = True,
        return_UNIX_times = True
    )
    database = access_database(filename = filename)
    table    = database["Bitcoin"]
    progress = shijian.Progress()
    progress.engage_quick_calculation_mode()
    number_of_entries = len(data)
    for index, element in enumerate(data):
        table.insert(dict(
            time      = element[0],
            value     = element[1]
        ))
        print(progress.add_datum(fraction = index / number_of_entries))

def table_database(
    filename           = "database.db",
    name_table         = "Bitcoin",
    include_attributes = None,
    rows_limit         = None
    ):

    database = access_database(filename = filename)

    return pyprel.Table(
        contents = pyprel.table_dataset_database_table(
            table              = database[name_table],
            include_attributes = include_attributes,
            rows_limit         = rows_limit
        )
    )

def values_Bitcoin_LocalBitcoin(
    URL = "https://localbitcoins.com/buy-bitcoins-online/"
          "GB/united-kingdom/national-bank-transfer/.json"
    ):

    file_URL    = urllib2.urlopen(URL)
    data_string = file_URL.read()
    data_JSON   = json.loads(data_string)

    advertisements = data_JSON["data"]["ad_list"]
    advertisement_prices = []
    for advertisement in advertisements:
        advertisement_prices.append(float(advertisement["data"]["temp_price"]))
    advertisement_prices.sort()
    return advertisement_prices

def save_current_values_LocalBitcoins_to_database(
    filename   = "database_LocalBitcoins.db"
    ):

    # Data saved to the database is a UTC datetime timestamp, a UTC UNIX,
    # timestamp, the LocalBitcoins API string returned (JSON) and a list of the
    # current prices in GBP.

    timestamp      = datetime.datetime.utcnow()
    timestamp_UNIX = (timestamp -\
                     datetime.datetime.utcfromtimestamp(0)).total_seconds()

    # buying prices

    URL = "https://localbitcoins.com/buy-bitcoins-online/"\
          "GB/united-kingdom/national-bank-transfer/.json"

    file_URL    = urllib2.urlopen(URL)
    data_string = file_URL.read()
    data_JSON   = json.loads(data_string)

    advertisements = data_JSON["data"]["ad_list"]
    advertisement_prices = []
    for advertisement in advertisements:
        advertisement_prices.append(float(advertisement["data"]["temp_price"]))
    advertisement_prices.sort()

    # selling prices

    URL = "https://localbitcoins.com/sell-bitcoins-online/"\
        "GB/united-kingdom/national-bank-transfer/.json"

    file_URL_sell    = urllib2.urlopen(URL)
    data_string_sell = file_URL_sell.read()
    data_JSON_sell   = json.loads(data_string_sell)

    advertisements_sell = data_JSON_sell["data"]["ad_list"]
    advertisement_prices_sell = []
    for advertisement_sell in advertisements_sell:
        advertisement_prices_sell.append(float(advertisement_sell["data"]["temp_price"]))
    advertisement_prices_sell.sort()

    # save to database

    database = access_database(filename = filename)
    table    = database["LocalBitcoins"]

    table.insert(dict(
        time             = timestamp,
        time_UNIX        = timestamp_UNIX,
        JSON_GB_NBT      = str(data_string),
        JSON_GB_NBT_sell = str(data_string_sell),
        values_GBP       = str(advertisement_prices),
        values_GBP_sell  = str(advertisement_prices_sell)
    ))

def loop_save_current_values_LocalBitcoins_to_database(
    filename    = "database_LocalBitcoins.db",
    time_period = 1800, # seconds (30 minutes)
    verbose     = True
    ):

    while True:
        if verbose:
            print(
                "{time} save LocalBitcoins current data to database "\
                "{filename} (next save in {seconds} s)".format(
                    time     = datetime.datetime.utcnow(),
                    filename = filename,
                    seconds  = time_period
                )
            )
        save_current_values_LocalBitcoins_to_database(
            filename = filename
        )
        time.sleep(time_period)

def table_database_LocalBitcoins(
    filename           = "database_LocalBitcoins.db",
    name_table         = "LocalBitcoins",
    include_attributes = ["time", "time_UNIX", "values_GBP"],
    rows_limit         = None
    ):

    return table_database(
        filename           = filename,
        name_table         = name_table,
        include_attributes = include_attributes,
        rows_limit         = rows_limit
    )
