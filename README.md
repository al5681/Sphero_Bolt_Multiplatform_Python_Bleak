# Sphero_Bolt_Multiplatform_Python_Bleak

This code allows you to control the Sphero Bolt programmatically using Python. Utilises the Bleak Library (https://github.com/hbldh/bleak) in order to use Bluetooth LE, should work
on Windows, Linux and MacOS.

## Commands supported 

* Set the colour of both main LEDs
* Set the colour of a single LED
* Set the colour of the matrix LED
* Write a character to the matrix LED of a specified colour 
* Roll the ball at a specified direction and speed

View 'Test' directory for example uses.

## Installation
1. Clone the repo 
2. "python -m pip install -r requirements.txt"

The code was written and tested in Python 3.8

## Inspirations 
The code drew heavily from the following repos: 

* https://github.com/trflorian/sphero_mini_win 
* https://github.com/alonks1234/SpheroPyLib
* https://github.com/Tineyo/BoltAPP
