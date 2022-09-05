from .utils import build_strip, render_strip_led, render_strip_text, send_wled_udp

WLED_HOST = "10.0.2.86"
WLED_PORT = 21324

STRIP_LENGTH = 300
STRIP_INVERT = True
MAP_WIDTH = 100
MAP_OFFSET = 20

strip = build_strip(
    strip_length=STRIP_LENGTH, 
    strip_invert=STRIP_INVERT, 
    map_width=MAP_WIDTH, 
    map_offset=MAP_OFFSET
)

rendered = render_strip_text(strip)
led_bytes = render_strip_led(strip)

print("TEXT")
print(rendered)
#print("LED BYTES")
#print(led_bytes)

send_wled_udp(WLED_HOST, WLED_PORT, led_bytes)