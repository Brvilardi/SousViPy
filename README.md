# Sous Vide Cheap

## What is Sous Vide?
Sous Vide is a cooking technique that consists in leaving food in a vacuum bag inside 
a water bath with precise control of the temperature.  This way, the food is consistently cooked (ex: no more overcooking your meat)

## Overview of the Project
This is a project to make a cheap, but functional, Sous Vide. The main goal 
is to learn more about electronics so don't expect it to be perfect.


## Components
* [Raspberry Pi Pico](https://www.raspberrypi.org/products/pico-pi/)
* [DS18B20](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf) (Waterproof Temperature Sensor)
* [SRD-05VDS-SL-C](https://www.circuitbasics.com/wp-content/uploads/2015/11/SRD-05VDC-SL-C-Datasheet.pdf) (Relay)
* Rice Cooker

## Diagram

![](docs/diagram.png)


## Logic

The system will implement a simple PID controller to control the 
temperature based on a target temperature. The control will be made
by switching the relay on and off.

The following diagram represents the logic:
![](docs/logic_diagram.drawio.png)


