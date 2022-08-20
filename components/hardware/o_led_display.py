import framebuf
from machine import I2C, Pin, SPI
from .SSD1306 import SSD1306_SPI, SSD1306_I2C


class OLedDisplay:
    width = 128
    height = 64

    def __init__(self, display_driver):
        self.display_driver = display_driver

    def show_text(self, text: str, x: int = 0, y: int = 0):
        self.display_driver.text(text, x, y)
        self.display_driver.show()

    def draw_icon(self, icon: bytearray, icon_width: int, icon_height: int, x: int, y: int):
        fb = framebuf.FrameBuffer(icon, icon_width, icon_height, framebuf.MONO_HLSB)
        self.display_driver.blit(fb, x, y)
        self.display_driver.show()

    def clear(self):
        self.display_driver.fill(0)
        self.display_driver.show()

class OLedDisplay_I2C(OLedDisplay):
    width = 128
    height = 64

    def __init__(self, ic2_id: int, sda: int, scl: int, display_driver, i2c_freq: int = 200_000, addr=0x3c):
        i2c = I2C(ic2_id, scl=Pin(scl), sda=Pin(sda), freq=i2c_freq)
        super().__init__(SSD1306_I2C(width=OLedDisplay_I2C.width, height=OLedDisplay_I2C.height, i2c=i2c,
                                          addr=addr))





class OLedDisplay_SPI(OLedDisplay):
    # https://techatronic.com/ssd1306-raspberry-pi-pico/
    width = 128
    height = 64

    def __init__(self, sck: int, mosi: int, dc: int, res, cs, width: int = None, height: int = None):
        # MOSI = SDA

        spi = SPI(0, 100000, mosi=Pin(mosi), sck=Pin(sck))
        super().__init__(SSD1306_SPI(width=width or OLedDisplay_SPI.width, height=height or OLedDisplay_SPI.height,
                           spi=spi, dc=Pin(dc), res=Pin(res), cs=Pin(cs)))

