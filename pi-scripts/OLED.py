import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

RESET_PIN = digitalio.DigitalInOut(board.D4)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D, reset=RESET_PIN)

oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

offset = 0  # flips between 0 and 32 for double buffering
print(dir(oled))

def print_on_OLED(text):
    draw.rectangle((0, 0, oled.width, oled.height * 2), outline=0, fill=0)
    pretext = "Task:"
    draw.text((0, 0), pretext, font=font, fill=255)
    draw.text((0, 48), text, font=font2, fill=255)
    oled.image(image)
    oled.show()
    time.sleep(1)
    clear_display()


def clear_display():
    oled.fill(0)
    oled.show()