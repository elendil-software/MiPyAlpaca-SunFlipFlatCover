# Sun Flip Flat Cover MicroPython Alpaca Driver

## Introduction

This driver is based on the original [MiPyAlpaca](https://github.com/RunTJoe/MiPyAlpaca) project.
It allows to control a flap cover...

**TODO:** complete introduction

## Installation

Copy the files from the GitHub repository on your device. Folders *mipyalpaca* and *templates* shall be subfolders of the folder containing the main application (like e.g. the example files).

MiPyAlpaca requires two additional packages:

- Microdot
  (https://github.com/miguelgrinberg/microdot)

- utemplate
  [https://github.com/pfalcon/utemplate](https://github.com/pfalcon/utemplate)

For installation of these packages see the corresponding documentation. If you use the Thonny IDE (https://thonny.org/), you can also use the Tools/Manage packages function. In Thonny, the file system of my installation looks like that:


## Usage

- Edit WLAN credentials in wlancred.py
- If you want to use another discovery port than 32227 (default), or another port for the Alpaca server, edit the port numbers in servercfg.json.
- Edit covercalibrator0.json for your cover configuration
- Start the main program


## Alpaca Management API

### Main Setup Page

The Alpaca server main setup page can be called by

**http://*host*:*port*/setup** 

where *host* is usually the ip address of your device.


### Device Specific Setup Page(s)

The device specific setup pages can be called by

**http://*host*:*port*/setup/v*apiversion_number*/*device_type*/*device_number*/setup**

As this implementation currently supports only API version v1 and device type "switch", the correct URL for switch device 0 is

**http://*host*:*port*/setup/api/v1/switch/0/setup**


# Acknowledgements

Many thanks to Joachim Stehle for the initial [MiPyAlpaca](https://github.com/RunTJoe/MiPyAlpaca) project.

Many thanks to Miguel Grinberg for providing his [Microdot](https://github.com/miguelgrinberg/microdot) framework. He has also provided excellent and fast support to my questions and remarks.

Also many thanks to Peter Simpson from the [ASCOM Driver and Application Development Support Forum](https://ascomtalk.groups.io/g/Developer) for answering all my questions regarding the Alpaca protocol.
