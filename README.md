# Phatscroll Bitfinex

Python script to get the current value of bitcoin from [bitfenix](https://www.bitfinex.com/)


[![Video](http://img.youtube.com/vi/MUbtMsSK6QE/0.jpg)](https://youtu.be/MUbtMsSK6QE)
[Link](https://youtu.be/MUbtMsSK6QE)

## Hardware
* a Raspberry pi (any raspberry should be good, I prefer the zero W for a neater result)
* a Pimoroni Led display between
  * Scrollphat (retired)
  * [Scrollphat HD](https://shop.pimoroni.com/products/scroll-phat-hd?variant=38472781450)
* Micro SDcard

## Installation
1. crerate a SD from one of the [official](https://www.raspberrypi.org/downloads/) images (tested with raspbian jessie)
2. Setup the Pi headlessy with [this guide](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
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
6. install the python library for your display:
  * [scrollphat](https://github.com/pimoroni/scroll-phat)
  * [scrollphat hd](https://github.com/pimoroni/scroll-phat-hd)
7. clone this repository
8. install the requirements for this project with: ```[sudo] pip install -r ./requirements.txt```
9. run the script based on your display
  * scrollphat: ```./main.py --type phat```
  * scrollphat hd: ```./main.py --type phathd```

## Start the script at boot
1. copy or link the *.service file for your display in ```/lib/systemd/system/```
  * scrollphat: ```scrollphat-bitfinex.service```
  * scrollphat hd: ```scrollphat-bitfinex.service```
2. reload the services: ```sudo systemctl daemon-reload```
3. enable the service at boot: ```sudo systemctl enable scrollphat[hd]-bitfinex.service```
4. reboot the pi with ```sudo reboot``` or start the service manually with: ```sudo systemctl start scrollphat[hd]-bitfinex.service```
