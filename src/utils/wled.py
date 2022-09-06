import socket

WLED_PROTOCOL_RGB = 2
WLED_TIMEOUT_SECS = 3

DIRECTION_LEFT = -1
DIRECTION_STOPPED = 0
DIRECTION_RIGHT = 1

SPRITE_SPEED_DEFAULT = 1
SPRITE_MODE_STOP = 1
SPRITE_MODE_LOOP = 2
SPRITE_MODE_BOUNCE = 3

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

PIXEL_OFF = WLEDPixel(0, 0, 0)
PIXEL_RED = WLEDPixel(255, 0, 0)
PIXEL_GREEN = WLEDPixel(0, 255, 0)
PIXEL_BLUE = WLEDPixel(0, 0, 255)
PIXEL_WHITE = WLEDPixel(255, 255, 255)

class WLEDSprite:
    """WLED LED Sprite"""

    def __init__(self, pixel, x, visible=True, direction=DIRECTION_RIGHT, speed=SPRITE_SPEED_DEFAULT, mode=SPRITE_MODE_LOOP):
        self.pixel = pixel
        self.x = x
        self.visible = visible
        self.direction = direction
        self.speed = speed
        self.mode = mode
    
    def __repr__(self):
        return f'<WLEDSprite pixel={self.pixel} x={self.x} visible={self.visible} direction={self.direction} speed={self.speed} mode={self.mode}>'

class WLEDStrip:
    """WLED LED Strip"""

    def __init__(self, host="localhost", port=21324, width=300, invert=False, protocol=WLED_PROTOCOL_RGB, timeout=WLED_TIMEOUT_SECS):
        self.host = host
        self.port = port
        self.width = width
        self.invert = invert
        self.protocol = protocol
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sprites = dict()
        self.clear()

    def __repr__(self):
        return f'<WLEDStrip host={self.host} port={self.port} invert={self.invert} protocol={self.protocol} timeout={self.timeout}>'

    def debug(self):
        print(self.pixels)

    def _get_absolute_x(self, x):
        return (self.width - x if self.invert else x) - 1

    def clear(self):
        self.pixels = [PIXEL_OFF for i in range(0, self.width)]

    def add_sprite(self, name, sprite):
        self.sprites[name] = sprite

    def tick_sprites(self):
        self.clear()
        for name, sprite in self.sprites.items():
            x = sprite.x + (sprite.direction * sprite.speed)
            direction = sprite.direction
            if sprite.mode == SPRITE_MODE_STOP:
                if x <= 0 or x >= self.width:
                    direction = DIRECTION_STOPPED
            elif sprite.mode == SPRITE_MODE_LOOP:
                if x <= 0: x = self.width
                if x >= self.width: x = 0
            elif sprite.mode == SPRITE_MODE_BOUNCE:
                if x <= 0: direction = DIRECTION_RIGHT
                if x >= self.width: direction = DIRECTION_LEFT
            self.sprites[name].x = x
            self.sprites[name].direction = direction
            self.draw_abs_pixel(x, sprite.pixel if sprite.visible else PIXEL_OFF)

    def draw_abs_pixel(self, x, pixel):
        self.pixels[self._get_absolute_x(int(x))] = pixel

    def update_wled(self):
        message = [self.protocol, self.timeout]
        for pixel in self.pixels:
            message += pixel.to_list()
        self.sock.sendto(bytearray(message), (self.host, self.port))
