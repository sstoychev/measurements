import subprocess
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7789
import bme680
import ltr559

from measurements_db import Measurements_db

db = Measurements_db()

######## light sensor
light_sensor = ltr559.LTR559()
light_sensor.update_sensor()

#### settings for bme680
try:
    env_sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    env_sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

env_sensor.set_humidity_oversample(bme680.OS_2X)
env_sensor.set_pressure_oversample(bme680.OS_4X)
env_sensor.set_temperature_oversample(bme680.OS_8X)
env_sensor.set_filter(bme680.FILTER_SIZE_3)
env_sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

env_sensor.set_gas_heater_temperature(320)
env_sensor.set_gas_heater_duration(150)
env_sensor.select_gas_heater_profile(0)

TEMP_FACTOR = 0.95

#### end of bme680

MESSAGE = "192.158.5.149"

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000
)

output = subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout
ip = output.split(" ")[0]

output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True).stdout
cpu_temp = float(output[output.index('=') + 1:output.rindex("'")])

temperature = ''
pressure  = ''
humidity = ''
gas_resistance =  ''

for _ in range(5):
    if env_sensor.get_sensor_data():
        temperature = env_sensor.data.temperature
        pressure  = env_sensor.data.pressure
        humidity = env_sensor.data.humidity

        if env_sensor.data.heat_stable:
            gas_resistance = env_sensor.data.gas_resistance
            break
    time.sleep(1)
# print(gas_resistance)

env_temp = ((cpu_temp - temperature) / TEMP_FACTOR)


######## light sensor
light_sensor.update_sensor()
lux = light_sensor.get_lux()
prox = light_sensor.get_proximity()

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height


img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

draw = ImageDraw.Draw(img)

font22 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
font30 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

size_x, size_y = draw.textsize(MESSAGE, font30)

draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))

text_x = disp.width
text_y = ((80 - size_y) // 2) +4

draw.text((0, 0), ip, font=font30, fill=(255, 255, 255))
draw.text((0, text_y*1), f'{env_temp:.1f}C {pressure:3.0f}hPa', font=font30, fill=(255, 255, 255))
draw.text((0, text_y*2), f'{humidity:2.0f}%', font=font30, fill=(255, 255, 255))
draw.text((0, text_y*3), time.strftime('%x %X'), font=font22, fill=(255, 255, 255))
draw.text((0, text_y*4), f'Lux: {lux:06.2f}', font=font30, fill=(255, 255, 255))
draw.text((0, text_y*5), f'Prox: {prox:04d}', font=font30, fill=(255, 255, 255))
draw.text((0, text_y*6), f'{gas_resistance:6.0f}', font=font30, fill=(255, 255, 255))

print(f'{env_temp:.1f}C {cpu_temp} {temperature} {pressure:3.0f}hPa {humidity:2.0f}% Lux: {lux:06.2f} {gas_resistance:6.0f}')
disp.display(img)
