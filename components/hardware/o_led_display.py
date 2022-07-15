import framebuf
from machine import I2C, Pin
from .SSD1306 import SSD1306_I2C


class OLedDisplay:
    width = 128
    height = 64

    def __init__(self, ic2_id: int = 1, sda: int = 26, scl: int = 27, i2c_freq: int = 200_000):
        i2c = I2C(ic2_id, scl=Pin(scl), sda=Pin(sda), freq=i2c_freq)
        self.display_driver = SSD1306_I2C(width=OLedDisplay.width, height=OLedDisplay.height, i2c=i2c, addr=0x3c)


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






