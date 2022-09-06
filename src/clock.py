import time
from utils.wled import WLEDStrip, WLEDSprite, WLEDPixel, DIRECTION_LEFT, DIRECTION_RIGHT, PIXEL_OFF, PIXEL_RED, PIXEL_GREEN, PIXEL_BLUE, SPRITE_MODE_STOP, SPRITE_MODE_LOOP, SPRITE_MODE_BOUNCE

WLED_HOST = "10.0.2.86"
WLED_PORT = 21324
STRIP_WIDTH = 300
STRIP_INVERT = True

strip = WLEDStrip(host=WLED_HOST, port=WLED_PORT, width=STRIP_WIDTH, invert=STRIP_INVERT)
strip.add_sprite("red_stop", WLEDSprite(PIXEL_RED, 10, True, DIRECTION_RIGHT, 1, SPRITE_MODE_STOP))
strip.add_sprite("green_loop", WLEDSprite(PIXEL_GREEN, 20, True, DIRECTION_RIGHT, 1.1, SPRITE_MODE_LOOP))
strip.add_sprite("blue_bounce", WLEDSprite(PIXEL_BLUE, 30, True, DIRECTION_RIGHT, 1.2, SPRITE_MODE_BOUNCE))

while True:
    strip.tick_sprites()
    strip.update_wled()
    time.sleep(0.02)
