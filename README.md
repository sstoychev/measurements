# measurements
Environment measurements with RaspberryPi, Pimoroni breakouts and Python

Used breakouts:

[st77989 - 1.3" screen](https://shop.pimoroni.com/products/1-3-spi-colour-lcd-240x240-breakout)

[bme680 - temperature, humidity, air pressure, air quality](https://shop.pimoroni.com/products/bme680-breakout)

[pa1010d - gps](https://shop.pimoroni.com/products/pa1010d-gps-breakout)

[ltr559 - light and proximity](https://shop.pimoroni.com/products/ltr-559-light-proximity-sensor-breakout) - will be replaced probably with

## Install:
1. Go to measurements folder

    `cd measurements`

1. Create venv:

    `python3 -m venv .venv`

1. Activate the venv:

    `source .venv/bin/activate`

1. Install the necessary packages

    `pip install -r /path/to/requirements.txt`
    * you may need to install `sudo apt install libatlas-base-dev` in order for numpy to work
