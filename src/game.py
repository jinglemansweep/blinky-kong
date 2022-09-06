import time
from utils import build_strip, render_strip_led, render_strip_text, send_wled_udp

WLED_HOST = "10.0.2.86"
WLED_PORT = 21324

STRIP_ENABLED = True
STRIP_UPDATE_DELAY = 0.008
STRIP_LENGTH = 300
STRIP_INVERT = True
MAP_WIDTH = 100
MAP_OFFSET = 20
CHAR_X_START = 1
CHAR_DIRECTION = 1

char_x = CHAR_X_START
char_direction = CHAR_DIRECTION

while True:

    strip = build_strip(
        strip_length=STRIP_LENGTH, 
        strip_invert=STRIP_INVERT, 
        map_width=MAP_WIDTH, 
        map_offset=MAP_OFFSET,
        char_x=char_x
    )

    rendered = render_strip_text(strip)
    led_bytes = render_strip_led(strip)

    #print(rendered)

    char_x += char_direction
    if char_x >= MAP_WIDTH - 1 or char_x <= 1: char_direction = 0 - char_direction

    if STRIP_ENABLED:
        send_wled_udp(WLED_HOST, WLED_PORT, led_bytes, timeout=1)

    time.sleep(STRIP_UPDATE_DELAY)