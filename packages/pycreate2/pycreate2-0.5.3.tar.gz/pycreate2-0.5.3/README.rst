.. image:: https://raw.githubusercontent.com/walchko/pycreate2/master/pics/create.png
	:align: center

pyCreate2
================

A python library for controlling the [iRobot Create 2](http://www.irobot.com/About-iRobot/STEM/Create-2.aspx).

**Still a work in progress**

Install
------------

pip
~~~~~

The recommended way to install this library is::

	pip install pycreate2

Development
~~~~~~~~~~~~~

If you wish to develop and submit git-pulls, you can do::

	git clone https://github.com/walchko/pycreate2
	cd pycreate2
	pip install -e .

Use
-------------

.. code-block:: python

	from  pycreate2 import Create2
	import time

	# Create a Create2.
	bot = Create2()

	# Start the Create 2
	bot.start()

	# Put the Create2 into 'safe' mode so we can drive it
	# This will still provide some protection
	bot.safe()

	# Tell the Create2 to drive straight forward at a speed of 100 mm/s
	bot.drive_straight(100)
	time.sleep(2)

	# Tell the Create2 to drive straight backward at a speed of 100 mm/s
	bot.drive_straight(-100)
	time.sleep(2)

	# Turn in place
	bot.drive_turn(100, 0)
	time.sleep(2)

	# Turn in place
	bot.drive_turn(-100, 0)
	time.sleep(4)

	# Turn in place
	bot.drive_turn(100, 0)
	time.sleep(2)

	# Stop the bot
	bot.drive_stop()

	# query some sensors
	sensor_pkts = [46, 47, 48, 49, 50, 51]  # ir bump sensors
	ir = bot.query_list(sensor_pkts, 12)

	# Close the connection
	# bot.close()

Documents
------------

Additional notes and documents are in the [docs folder](https://raw.githubusercontent.com/walchko/pycreate2/master/docs/Markdown/)

Modes
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/walchko/pycreate2/master/pics/create_modes.png
	:align: center

Sensor Data
~~~~~~~~~~~~~

Here are some of the more useful sensor packets.

================ =============== =================
Sensor           Range           Packet Numbers
================ =============== =================
ir bumper        [0-127]         45
ir bumper        [0-4095]        46-51
encoder          [-322768-32767] 43,44
current          [-322768-32767] 23
voltage          [0-65535]       22
motor current    [-322768-32767] 54,55
battery charge   [0-65535]       25
battery capacity [0-65535]       26 (doesn't change?)
cliff            [0-1]           9-12
cliff signal     [0-4095]        28-31
overcurrents     [0-29]          14
bump wheeldrops  [0-15]          7
================ =============== =================

Change Log
---------------

========== ======= =============================
2017-05-26 0.5.0   init and published to pypi
========== ======= =============================

The MIT License
==================

**Copyright (c) 2007 Damon Kohler**

**Copyright (c) 2015 Jonathan Le Roux (Modifications for Create 2)**

**Copyright (c) 2015 Brandon Pomeroy**

**Copyright (c) 2017 Kevin Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
