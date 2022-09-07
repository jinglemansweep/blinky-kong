import socket

WLED_PROTOCOL_RGB = 2
WLED_TIMEOUT = 3

def send_wled_udp(host, port, pixels, timeout=WLED_TIMEOUT, protocol=WLED_PROTOCOL_RGB):
    message = [protocol, timeout]
    for pixel in pixels:
        message += pixel.to_list()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytearray(message), (host, port))

class WLEDPixel:
    """WLED LED Pixel"""

    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f'<WLEDPixel R{self.r}G{self.g}B{self.b}>'

    def to_list(self):
        return [self.r, self.g, self.b]


class WLEDSprite:
    """WLED LED Sprite"""

    def __init__(self, pixel, x, visible=True):
        self.pixel = pixel
        self.x = x
        self.visible = visible
        
    def __repr__(self):
        return f'<WLEDSprite pixel={self.pixel} x={self.x} visible={self.visible}>'

    def move(self, strip, position):
        x = self.x + position
        if x < 0: x = 0
        if x > strip.width: x = strip.width
        self.x = x


class WLEDStrip:
    """WLED LED Strip"""

    pixel_off = WLEDPixel(0, 0, 0)

    def __init__(self, width=300, flip=False):
        self.width = width
        self.flip = flip
        self.sprites = list()

    def __repr__(self):
        return f'<WLEDStrip width={width} flip={flip}>'

    def debug(self):
        pass

    def process(self, sprites):
        pixels = [WLEDPixel(0, 0, 0) for i in range(0, self.width)]
        for sprite in sprites:
            pixels[sprite.x] = sprite.pixel if sprite.visible else self.pixel_off
        return pixels[::-1] if self.flip else pixels

    def render_console(self, pixels):
        out = ''
        for pixel in pixels:
            if pixel.r == 0 and pixel.g == 0 and pixel.b == 0:
                out += ' '
            elif pixel.r > 0 and pixel.g == 0 and pixel.b == 0:
                out += '[bold red]*[/bold red]'
            elif pixel.r == 0 and pixel.g > 0 and pixel.b == 0:
                out += '[bold green]*[/bold green]'
            elif pixel.r == 0 and pixel.g == 0 and pixel.b > 0:
                out += '[bold blue]*[/bold blue]'    
        return out

