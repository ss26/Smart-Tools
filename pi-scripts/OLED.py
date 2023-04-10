import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

RESET_PIN = digitalio.DigitalInOut(board.D4)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D, reset=RESET_PIN)

# oled.rotate(2)
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

offset = 0  # flips between 0 and 32 for double buffering

def print_on_OLED(text, y_axis=14):
    draw.rectangle((0, 0, oled.width, oled.height * 2), outline=0, fill=0)
    # pretext = "Task:"
    # draw.text((0, 0), pretext, font=font, fill=255)
    draw.text((0, y_axis), text, font=font2, fill=255)
    
    # time.sleep(10)
    # clear_display()

def OLED_show():
    oled.image(image)
    oled.show()

def clear_display():
    oled.rotate(2)
    oled.fill(0)
    oled.show()