# Phatscroll Bitfinex

Python script to get the current value of bitcoin from [bitfenix](https://www.bitfinex.com/)


[![Video](http://img.youtube.com/vi/MUbtMsSK6QE/0.jpg)](https://youtu.be/MUbtMsSK6QE)
[Link](https://youtu.be/MUbtMsSK6QE)

## Hardware
* Raspberry pi (any raspberry should be good)
* [Pimoroni Scrollphat](https://shop.pimoroni.com/collections/raspberry-pi-zero/products/scroll-phat)
* WiFi dongle / USB Ethernet adapter
* Micro SDcard

## Installation
1. crerate a SD from one of the [official](https://www.raspberrypi.org/downloads/) images (tested with raspbian jessie)
2. if you're gonna use a WiFi dongle
    1. mount/open the SD card
    2. edit the file ```etc/wpa_supplicant/wpa_supplicant.conf``` appending at the end:
        ```
        network={
          ssid="YOUR_SSID_NAME"
          psk="YOUR_SSID_PASSWORD"
        }
        ```
3. Boot the pi
4. ssh into it with the default credential
    ```
    user: pi
    password: raspberry
    ```
5. update
    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```
6. install scrollphat library from: ```https://github.com/pimoroni/scroll-phat```
7. clone this repository
8. install the requirements for this project with: ```[sudo] pip install -r ./requirements.txt```
9. run the scripte with ```./main.py```

## Workflow
the script create two thread one to retrive the data from the websocket and store it in a variable the second thread displays the data, to do that it create a string with 2  different value, this is to prevent the change of the while on screen, the string is composed with
```[Value1][currency_symbol] [Value2][currency_symbol]```
and it start to scroll until ```[Value1][currency_symbol] ```  is complitly out of the screen thaen a new string is created and displayed
```[Value2][currency_symbol] [Value3][currency_symbol]``` and scrolled until