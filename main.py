#!/usr/bin/env python

from websocket import create_connection
import json
import scrollphat
import threading
import time

# basic configuration
currency = "BTCUSD"
# optiona available
# BTCUSD | ETHBTC | ETHUSD | LTCBTC | LTCUSD
currency_symbol = "$"
# symbol displayed after the value
scrollphat.set_brightness(7)
# led brightness

# thread to fetch the data from Bitfinex Websocket API
class get_data(threading.Thread):

  def __init__(self, threadID, currency):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.currency = currency

  def run(self):
    global currency_value
    ws = create_connection("wss://api2.bitfinex.com:3000/ws")
    ws.send(json.dumps({
      "event": "subscribe",
      "channel": "book",
      "pair": currency,
      "prec": "P0"
    }))
    while running:
      result_raw = ws.recv()
      result_json = json.loads(result_raw)
      # discriminate from the first data received and frome any subsequent "HeartBeat"
      if (type(result_json) is list) and (type(result_json[1]) is float):
        currency_value = result_json[1]

# thread to consume the data
class print_data(threading.Thread):

  def __init__(self, threadID, currency, symbol):
    threading.Thread.__init__(self)
    self.currency = currency
    self.symbol = symbol
    self.letter_width = {
      32:   3, #  
      33:   2, # !
      34:   4, # "
      35:   6, # #
      36:   6, # $
      37:   4, # %
      38:   5, # &
      39:   2, # '
      40:   3, # (
      41:   3, # )
      42:   4, # *
      43:   4, # +
      44:   3, # , 
      45:   3, # -
      46:   2, # .
      47:   3, # /
      48:   4, # 0
      49:   4, # 1
      50:   4, # 2
      51:   4, # 3
      52:   4, # 4
      53:   4, # 5
      54:   4, # 6
      55:   4, # 7
      56:   4, # 8
      57:   4, # 9
      58:   2, # :
      59:   3, # ;
      60:   3, # <
      61:   4, # =
      62:   3, # >
      63:   4, # ?
      64:   5, # @
      65:   4, # A
      66:   4, # B
      67:   4, # C
      68:   4, # D
      69:   4, # E
      70:   4, # F
      71:   4, # G
      72:   4, # H
      73:   4, # I
      74:   4, # J
      75:   4, # K
      76:   4, # L
      77:   6, # M
      78:   5, # N
      79:   4, # O
      80:   4, # P
      81:   5, # Q
      82:   4, # R
      83:   4, # S
      84:   4, # T
      85:   5, # U
      86:   4, # V
      87:   6, # W
      88:   4, # X
      89:   4, # Y
      90:   4, # Z
      91:   3, # [
      92:   3, # \
      93:   3, # ]
      94:   4, # ^
      95:   4, # _
      96:   3, # `
      97:   4, # a
      98:   4, # b
      99:   3, # c
      100:  4, # d
      101:  4, # e
      102:  3, # f
      103:  4, # g
      104:  4, # h
      105:  2, # i
      106:  3, # j
      107:  4, # k
      108:  2, # l
      109:  6, # m
      110:  4, # n
      111:  4, # o
      112:  4, # p
      113:  4, # q
      114:  3, # r
      115:  3, # s
      116:  3, # t
      117:  4, # u
      118:  4, # v
      119:  6, # w
      120:  4, # x
      121:  4, # y
      122:  4, # z
      123:  4, # {
      124:  2, # |
      125:  4, # }
      126:  5, # ~
      }

  # function to determinate the cloumn/led "width" of a string
  # used to determinate after how many "scroll" the string will be out of the
  # screen
  def count_letters(self, string):
    string_width = 0
    for letter in string:
      string_width += self.letter_width[ord(letter)]
    return string_width

  def run(self):
    global currency_value
    next_value = 0.0
    while running:

      curr_value_string = "{:7.2f}".format( round( next_value,      2 ) ) + self.symbol + " "
      next_value_string = "{:7.2f}".format( round( currency_value,  2 ) ) + self.symbol + " "

      next_value = currency_value

      string_to_display = curr_value_string + next_value_string

      scrollphat.write_string( string_to_display )
      string_length = self.count_letters( curr_value_string )
      for _ in range( string_length ):
        scrollphat.scroll()
        time.sleep(0.1)

currency_value = 0.0

running = True
gd = get_data( 1, currency)
gd.start()

pd = print_data( 2, currency, currency_symbol )
pd.start()

exit = raw_input("Press enter to exit")
if exit or not exit:
  running = False
  scrollphat.clear()