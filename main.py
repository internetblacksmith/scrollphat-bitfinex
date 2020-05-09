#!/usr/bin/env python

from websocket          import create_connection
import argparse
import json
import logging
import sys
import threading
import time

parser = argparse.ArgumentParser()
parser.add_argument('--type', '-t', type=str, required=True, choices=['phat', 'phathd'], help='type of display')
parser.add_argument('--daemon', '-d', required=False, action='store_true', help='if the script should run as daemon so without prompt' )
args = parser.parse_args()

if args.type == 'phathd':
  from scrollphathd.fonts import font5x7
  import scrollphathd
elif args.type == 'phat':
  import scrollphat


# thread to fetch the data from Bitfinex Websocket API
class GetData(threading.Thread):

  def __init__(self, threadID, currency):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.currency = currency
    self.running = True

  def stop(self):
    self.running = False

  def run(self):
    global current_value
    attempting_connection = True
    while attempting_connection:
      try:
        logging.info("attempt connection")
        ws = create_connection("wss://api-pub.bitfinex.com/ws/2")
        attempting_connection = False
        logging.info("successfull")
      except:
        logging.error("ERROR")
        time.sleep(1)
    ws.send(json.dumps({
      "event": "subscribe",
      "channel": "book",
      "pair": self.currency,
      "prec": "P0"
    }))
    while self.running:
      result_raw = ws.recv()
      result_json = json.loads(result_raw)
      # discriminate from the first data received and frome any subsequent "HeartBeat"
      if (type(result_json) is list) and (type(result_json[1][0]) is float):
        current_value = result_json[1][0]

class Display():

  def __init__(self, threadID, currency, symbol):
    threading.Thread.__init__(self)
    self.currency = currency
    self.symbol = symbol
    self.running = True

  def format_value(self, value):
    return "{:7.2f}".format( round( value,  2 ) ) + self.symbol + " "

# thread to consume the data
class ScrollPhatDisplay(threading.Thread, Display):

  def __init__(self, threadID, currency, symbol):
    Display.__init__(self, threadID, currency, symbol)

  def stop(self):
    scrollphat.clear()
    self.running = False

  def run(self):
    global current_value
    next_value = 0.0
    scrollphat.set_rotate(True)

    while self.running:

      if next_value == 0.0:
        next_value_string = ""
      else:
        next_value_string = self.format_value(current_value)

      if current_value == 0.0:
        curr_value_string = "Loading.."
      else:
        curr_value_string = self.format_value(next_value)
        next_value = current_value

      string_to_display = curr_value_string + next_value_string

      scrollphat.write_string( string_to_display )
      length = scrollphat.buffer_len()

      for i in range(length):
        scrollphat.scroll()
        time.sleep(0.15)


# thread to consume the data
class ScrollPhatHdDisplay(threading.Thread, Display):

  def __init__(self, threadID, currency, symbol):
    Display.__init__(self, threadID, currency, symbol)

  def stop(self):
    scrollphathd.clear()
    self.running = False

  def run(self):
    global current_value
    next_value = 0.0

    scrollphathd.set_font(font5x7)
    scrollphathd.set_brightness(0.2)
    scrollphathd.rotate(degrees=180)

    while self.running:

      if next_value == 0.0:
        next_value_string = ""
      else:
        next_value_string = self.format_value(next_value)

      if current_value == 0.0:
        curr_value_string = "loading.. "
      else:
        curr_value_string = self.format_value(current_value)
        next_value = current_value

      string_to_display = curr_value_string + next_value_string

      scrollphathd.clear()
      str_len = scrollphathd.write_string( string_to_display )
      for _ in range( str_len ):
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(0.05)

# basic configuration
currency = "tBTCUSD"
# optiona available
# tBTCUSD | tETHBTC | tETHUSD | tLTCBTC | tLTCUSD
currency_symbol = 'USD'
current_value = 0.0
# symbol displayed after the value
# led brightness
#scrollphathd.set_font(font5x7)
#scrollphathd.set_brightness(0.2)
#scrollphathd.rotate(degrees=180)
gd = GetData( 1, currency)

if args.type == 'phathd':
  pd = ScrollPhatHdDisplay( 2, currency, currency_symbol )
elif args.type == 'phat':
  pd = ScrollPhatDisplay( 2, currency, currency_symbol )

pd.start()
gd.start()
 
if args.daemon:
  exit()

exit = raw_input("Press enter to exit")
if exit or not exit:
  pd.stop()
  gd.stop()

